from datetime import datetime

HISTORY_FILE = "health_history.log"

def save_health(status, cpu, ram):
    with open(HISTORY_FILE, "a") as file:
        file.write(
            f"{datetime.now()} | {status} | CPU: {cpu}% | RAM: {ram}% \n"
        )

def show_history():
    try:
        with open(HISTORY_FILE, "r") as file:
            print(file.read())
    except FileNotFoundError:
        print("No health history found.")

show_history()
