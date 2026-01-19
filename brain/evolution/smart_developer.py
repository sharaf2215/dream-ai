import os
import re
import ollama  # <--- The new Local Brain library

class SmartDeveloper:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.skills_path = os.path.join(self.base_dir, "skills")
        if not os.path.exists(self.skills_path):
            os.makedirs(self.skills_path)

    def task_to_filename(self, task):
        clean_name = re.sub(r'[^a-z0-9]', '_', task.lower()).strip('_')
        return clean_name + ".py"

    def generate_solution(self, task):
        filename = self.task_to_filename(task)
        skill_file = os.path.join(self.skills_path, filename)
        
        # 1. MEMORY CHECK
        if os.path.exists(skill_file):
            print(f"🧠 MEMORY: I remember this.")
            return skill_file

        print(f"🔨 DEVELOPER: Asking Ollama to write code for: '{task}'...")

        # 2. ASK THE LOCAL AI (Ollama)
        try:
            # We tell the AI to behave like a Python Coder
            prompt = f"""
            You are a Python Expert. Write a Python script to do this: {task}.
            RULES:
            1. Output ONLY raw python code.
            2. Do not use Markdown (no ```python blocks).
            3. Do not write explanations. Just code.
            """
            
            response = ollama.chat(model='qwen2.5-coder:1.5b', messages=[
                {'role': 'user', 'content': prompt},
            ])
            
            # Get the code from the AI
            code = response['message']['content']
            
            # Clean up potential markdown mistakes
            code = code.replace("```python", "").replace("```", "").strip()

        except Exception as e:
            print(f"❌ OLLAMA ERROR: {e}")
            code = "print('I tried to write code, but my local brain is not responding.')"

        # 3. SAVE THE CODE
        with open(skill_file, "w") as f:
            f.write(code)
            
        print(f"💾 SAVED: Code written and saved to {filename}")
        return skill_file