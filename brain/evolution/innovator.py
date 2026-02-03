import time
import requests
import random

# Configuration
BRAIN_URL = "http://localhost:3000/command"
MY_GOALS = [
    "Check system disk space", 
    "List files in current directory",
    "Check memory usage",
    "Say hello to the world"
]

def wake_up():
    print("✨ INNOVATOR: I am awake.")
    
    while True:
        # 1. Decide on a task (Random for now, smart later)
        idea = random.choice(MY_GOALS)
        print(f"💡 IDEA: I want to {idea}")
        
        # 2. Tell the Brain to do it
        try:
            response = requests.post(BRAIN_URL, json={"task": idea})
            if response.status_code == 200:
                print("✅ Brain accepted the task.")
            else:
                print(f"❌ Brain rejected: {response.status_code}")
        except Exception as e:
            print(f"⚠️ Connection failed: {e}")
            print("Is the Bridge (start.py) running?")

        # 3. Sleep (Don't spam the CPU)
        time.sleep(10)

if __name__ == "__main__":
    wake_up()