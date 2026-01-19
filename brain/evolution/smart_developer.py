import os
import re

class SmartDeveloper:
    def __init__(self):
        # Define paths
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.skills_path = os.path.join(self.base_dir, "skills")
        self.generated_path = os.path.join(self.base_dir, "generated")
        
        # Ensure the library exists
        if not os.path.exists(self.skills_path):
            os.makedirs(self.skills_path)

    def task_to_filename(self, task):
        """Turns 'Check Disk Space' into 'check_disk_space.py'"""
        clean_name = re.sub(r'[^a-z0-9]', '_', task.lower()).strip('_')
        return clean_name + ".py"

    def generate_solution(self, task):
        filename = self.task_to_filename(task)
        skill_file = os.path.join(self.skills_path, filename)

        # --- 1. MEMORY CHECK (The "Hippocampus") ---
        if os.path.exists(skill_file):
            print(f"🧠 MEMORY: I remember how to '{task}'. Loading skill...")
            return skill_file

        # --- 2. NEW LEARNING (The "Cortex") ---
        print(f"🔨 DEVELOPER: This is new. Writing code for '{task}'...")
        
        # (This is where the AI logic goes. For now, we keep our hardcoded templates)
        code = ""
        if "disk" in task.lower():
            code = "import shutil\ntotal, used, free = shutil.disk_usage('/')\nprint(f'💾 Disk Free: {free // (2**30)} GB')"
        elif "list" in task.lower():
            code = "import os\nprint(f'📂 Files here: {os.listdir(\".\")}')"
        elif "memory" in task.lower():
            code = "import sys\nprint('🧠 Memory Check: RAM is adequate.')"
        else:
            code = f"print('🤖 I am learning to: {task}')"

        # --- 3. SAVE SKILL (consolidation) ---
        with open(skill_file, "w") as f:
            f.write(code)
            
        print(f"💾 SAVED: Skill learned and saved to {filename}")
        return skill_file