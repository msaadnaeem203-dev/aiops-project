import re

LOG_FILE = "alerts.log"

print("AIOps Alert Classifier")
print("----------------------")

try:
    with open(LOG_FILE, "r") as file:
        lines = file.readlines()

    if not lines:
        print("No alerts found.")
    else:
        for line in lines[-10:]:
            cpu_match = re.search(r"CPU:\s*([\d.]+)%", line)
            ram_match = re.search(r"RAM:\s*([\d.]+)%", line)

            if cpu_match and ram_match:
                cpu = float(cpu_match.group(1))
                ram = float(ram_match.group(1))

                if cpu >= 90 or ram >= 90:
                    severity = "CRITICAL"
                elif cpu >= 80 or ram >= 80:
                    severity = "WARNING"
                else:
                    severity = "INFO"

                print(
                    f"CPU: {cpu:.1f}% | RAM: {ram:.1f}% | "
                    f"Severity: {severity}"
                )

except FileNotFoundError:
    print("alerts.log not found.")
