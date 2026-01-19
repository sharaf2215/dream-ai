import os
import re

class SmartDeveloper:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.skills_path = os.path.join(self.base_dir, "skills")
        self.generated_path = os.path.join(self.base_dir, "generated")
        
        if not os.path.exists(self.skills_path):
            os.makedirs(self.skills_path)

    def task_to_filename(self, task):
        clean_name = re.sub(r'[^a-z0-9]', '_', task.lower()).strip('_')
        return clean_name + ".py"

    def generate_solution(self, task):
        filename = self.task_to_filename(task)
        skill_file = os.path.join(self.skills_path, filename)

    def generate_solution(self, task):
        filename = self.task_to_filename(task)
        skill_file = os.path.join(self.skills_path, filename)

        if os.path.exists(skill_file):
            print(f"🧠 MEMORY: Loading skill for '{task}'...")
            return skill_file

        print(f"🔨 DEVELOPER: Writing NEW code for '{task}'...")
        code = ""
        
        # --- SKILL 1: CRYPTO (Dynamic) ---
        # Can handle "price of bitcoin", "price of ethereum", "price of dogecoin"
        if "price" in task.lower():
            # Default to bitcoin, but try to find other coins
            coin = "bitcoin" 
            for word in task.lower().split():
                if word in ["ethereum", "dogecoin", "solana", "ripple"]:
                    coin = word
            
            code = f"""
import requests
try:
    url = "https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
    data = requests.get(url).json()
    price = data['{coin}']['usd']
    print(f"The current price of {coin} is ${{price:,}} dollars.")
except:
    print(f"⚠️ Could not find price for {coin}")
"""

        # --- SKILL 2: WEATHER (New!) ---
        # Uses wttr.in (No API Key needed)
        elif "weather" in task.lower():
            # Extract city name (simple version: takes last word)
            city = task.split()[-1] 
            code = f"""
import requests
try:
    print(f"☁️ Checking weather for {city}...")
    url = "https://wttr.in/{city}?format=3"
    response = requests.get(url)
    print(f"The weather in {{city}} is currently {{response.text.strip()}}.")
except Exception as e:
    print(f"⚠️ Weather error: {{e}}")
"""

        # --- SKILL 3: SYSTEM STATS ---
        elif "disk" in task.lower():
            code = "import shutil\nprint(f'💾 Disk Free: {shutil.disk_usage(\"/\").free // (2**30)} GB')"
        
        else:
            code = f"print('🤖 I do not know how to {{task}} yet.')"

        with open(skill_file, "w") as f:
            f.write(code)
        return skill_file

        # 1. MEMORY CHECK
        if os.path.exists(skill_file):
            print(f"🧠 MEMORY: I remember how to '{task}'. Loading skill...")
            return skill_file

        # 2. NEW LEARNING (The Upgrade)
        print(f"🔨 DEVELOPER: This is new. Writing code for '{task}'...")
        
        code = ""
        
        # --- NEW SKILL: CRYPTO CHECKER ---
        if "bitcoin" in task.lower() or "price" in task.lower():
            code = """
import requests
try:
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url).json()
    price = response['bitcoin']['usd']
    print(f"💰 Bitcoin Price: ${price:,}")
except Exception as e:
    print(f"⚠️ Could not fetch price: {e}")
"""
        # --- EXISTING SKILLS ---
        elif "disk" in task.lower():
            code = "import shutil\ntotal, used, free = shutil.disk_usage('/')\nprint(f'💾 Disk Free: {free // (2**30)} GB')"
        elif "list" in task.lower():
            code = "import os\nprint(f'📂 Files here: {os.listdir(\".\")}')"
        elif "memory" in task.lower():
            code = "import sys\nprint('🧠 Memory Check: RAM is adequate.')"
        elif "hello" in task.lower():
             code = "print('👋 Hello! I am your Dream AI.')"
        else:
            code = f"print('🤖 I am simply printing: {task}')"

        # 3. SAVE SKILL
        with open(skill_file, "w") as f:
            f.write(code)
            
        print(f"💾 SAVED: Skill learned and saved to {filename}")
        return skill_file