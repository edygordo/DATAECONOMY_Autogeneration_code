import subprocess

def checkValidityAndCorrectness(user_code: str, expected_output: str) -> bool:
    """
    Run the user_code (which should include its own test logic).
    Return True if output matches the expected output, else False.
    """
    print("-- CHECKING CODE'S EXECUTION AND EXPECTED OUTPUT --")
    print("User code being run:", user_code)
    
    try:
        user_process = subprocess.run(
            ["python3", "-c", user_code],
            text=True,
            capture_output=True,
            timeout=5  # prevent hanging
        )
    except subprocess.TimeoutExpired:
        print("❌ Code execution timed out.")
        return False

    if user_process.stderr:
        print("❌ Error during execution:\n", user_process.stderr)
        return False
    
    print("✅ Output:\n", user_process.stdout)
    return user_process.stdout.strip() == expected_output.strip()
