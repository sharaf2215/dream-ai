import os
import re
import textwrap
from typing import Callable, List, Optional, Tuple

class SmartDeveloper:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.skills_path = os.path.join(self.base_dir, "skills")
        self.memory_path = os.path.join(self.base_dir, "memory", "global_memory.txt")
        self.status_path = os.path.join(self.base_dir, "status", "mode.txt")

        if not os.path.exists(self.skills_path):
            os.makedirs(self.skills_path)
        if not os.path.dirname(self.memory_path):
            os.makedirs(os.path.dirname(self.memory_path))
        if not os.path.dirname(self.status_path):
            os.makedirs(os.path.dirname(self.status_path))
        if not os.path.exists(self.memory_path):
            with open(self.memory_path, "w", encoding="utf-8") as f:
                f.write("System initialized.\n")

        # Default HUD state
        self.update_dashboard("💤 IDLE")

        # Map task keywords to script generators
        self._strategies: List[Tuple[str, Callable[[str], str]]] = [
            ("disk space", self._script_disk_usage),
            ("list files", self._script_list_files),
            ("memory usage", self._script_memory_usage),
            ("say hello", self._script_say_hello),
            ("hello", self._script_say_hello),
            ("remember", self._script_remember_fact),
            ("name is", self._script_remember_fact),
        ]

    def update_dashboard(self, mode_text):
        """Write current mode to HUD file."""
        try:
            with open(self.status_path, "w", encoding="utf-8") as f:
                f.write(mode_text)
        except Exception:
            pass

    def read_memory(self) -> str:
        try:
            with open(self.memory_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return ""

    def task_to_filename(self, task):
        clean_name = re.sub(r'[^a-z0-9]', '_', task.lower()).strip('_')
        return clean_name + ".py"

    def _match_strategy(self, task: str) -> Optional[Callable[[str], str]]:
        """Find a matching strategy for the task."""
        lowered = task.lower()
        for keyword, func in self._strategies:
            if keyword in lowered:
                return func
        return None

    # Script generators --------------------------------------------------
    def _script_disk_usage(self, task: str) -> str:
        return textwrap.dedent("""
            import shutil
            total, used, free = shutil.disk_usage(".")
            gb = 1024 ** 3
            print(f"Disk -> total: {total/gb:.2f}GB, used: {used/gb:.2f}GB, free: {free/gb:.2f}GB")
        """).strip() + "\n"

    def _script_list_files(self, task: str) -> str:
        return textwrap.dedent("""
            import os
            items = sorted(os.listdir("."))
            for entry in items:
                print(entry)
        """).strip() + "\n"

    def _script_memory_usage(self, task: str) -> str:
        return textwrap.dedent("""
            def read_meminfo():
                try:
                    with open("/proc/meminfo", "r") as f:
                        for line in f:
                            if "MemTotal" in line or "MemFree" in line:
                                print(line.strip())
                except:
                    print("Memory info unavailable on this system")
            read_meminfo()
        """).strip() + "\n"

    def _script_say_hello(self, task: str) -> str:
        return "print('Hello! I am Dream AI. How can I assist you?')\n"

    def _script_remember_fact(self, task: str) -> str:
        fact = task.strip().rstrip(".")
        return textwrap.dedent(f"""
            from datetime import datetime
            memory_path = r"{self.memory_path}"
            timestamp = datetime.utcnow().isoformat() + "Z"
            with open(memory_path, "a", encoding="utf-8") as f:
                f.write(f"\\n[FACT] {{timestamp}} :: {fact}")
            print("Saved to memory.")
        """).strip() + "\n"

    def _script_fallback(self, task: str) -> str:
        return f"print('Task: {task}\\nNo specific handler available.')\n"

    def generate_solution(self, task):
        filename = self.task_to_filename(task)
        skill_file = os.path.join(self.skills_path, filename)

        # 1. Check memory
        if os.path.exists(skill_file):
            print(f"🧠 MEMORY: I remember this task.")
            return skill_file

        # 2. Determine mode and update HUD
        self.update_dashboard("🧠 THINKING...")
        print(f"🔨 DEVELOPER: Generating code for: '{task}'...")

        # 3. Match strategy or fallback
        builder = self._match_strategy(task)
        if builder:
            code = builder(task)
        else:
            code = self._script_fallback(task)

        # 4. Update HUD based on code type
        if "memory" in code:
            self.update_dashboard("🟣 LEARNING MODE")
        elif "shutil" in code or "os.listdir" in code or "open(" in code:
            self.update_dashboard("🟢 SYSTEM MODE")
        else:
            self.update_dashboard("🔴 CHAT MODE")

        # 5. Save the code
        with open(skill_file, "w", encoding="utf-8") as f:
            f.write(code)

        print(f"💾 SAVED: Code written to {filename}")
        return skill_file