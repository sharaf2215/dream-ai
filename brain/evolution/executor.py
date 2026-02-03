import os
import subprocess
import sys
from typing import Optional

def execute_code(file_path: str, *, timeout_seconds: int = 10, cwd: Optional[str] = None) -> str:
    """
    Runs a Python script and returns the output or error.
    """
    print(f"⚡ EXECUTOR: Running {file_path}...")

    if not os.path.exists(file_path):
        return f"❌ Error: File '{file_path}' not found."

    try:
        result = subprocess.run(
            [sys.executable, file_path],
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            cwd=cwd,
        )

        # Check if there were errors
        stdout = (result.stdout or "").strip()
        stderr = (result.stderr or "").strip()

        if result.returncode == 0:
            output = stdout if stdout else "Done (No Output)"
            print(f"✅ SUCCESS:\n{output}")
            return output

        error = stderr if stderr else stdout
        error = error.strip() if error else "Unknown error"
        print(f"❌ EXECUTION ERROR:\n{error}")
        return f"Error: {error}"

    except subprocess.TimeoutExpired:
        return f"❌ SYSTEM ERROR: Timed out after {timeout_seconds}s"
    except Exception as e:
        return f"❌ SYSTEM ERROR: {str(e)}"

# --- Manual Test (Optional) ---
if __name__ == "__main__":
    # Test with the file your AI just made
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sample = os.path.join(base_dir, "skills", "say_hello_to_the_world.py")
    print(execute_code(sample, cwd=os.path.dirname(sample)))