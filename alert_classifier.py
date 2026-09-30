import re

LOG_FILE = "alerts.log"

info_count = 0
warning_count = 0
critical_count = 0

print("AIOps Alert Classifier")
print("----------------------------")

try:
    with open(LOG_FILE, "r") as file:
        lines = file.readlines()

        for line in lines:
            matches = re.findall(r"([\d.]+)%", line)

            if len(matches) >= 2:
                cpu = float(matches[0])
                ram = float(matches[1])

                if cpu >= 90 or ram >= 90:
                    severity = "CRITICAL"
                elif cpu >= 80 or ram >= 80:
                    severity = "WARNING"
                else:
                    severity = "INFO"

                if severity == "INFO":
                    info_count += 1
                elif severity == "WARNING":
                    warning_count += 1
                elif severity == "CRITICAL":
                    critical_count += 1

                print(
                    f"CPU: {cpu:.1f}% | RAM: {ram:.1f}% | "
                    f"Severity: {severity}"
                )

    print("---------------------------------")
    print(f"INFO: {info_count}")
    print(f"WARNING: {warning_count}")
    print(f"CRITICAL: {critical_count}")

except FileNotFoundError:
    print("alerts.log not found.")
