import re

LOG_FILE = "alerts.log"

info_count = 0
warning_count = 0
critical_count = 0
invalid_count = 0

print("AIOps Alert Classifier")
print("=" * 45)

try:
    with open(LOG_FILE, "r") as file:
        for line in file:
            cpu_match = re.search(r"CPU: \s*([\d.]+)%", line, re.IGNORECASE
            )
            ram_match = re.search(r"RAM: \s*([\d.]+)%", line, re.IGNORECASE
            )
            disk_match = re.search(r"DISK:\s*([\d.]+)%", line, re.IGNORECASE
            )

            if not cpu_match or not ram_match:
                invalid_count += 1
                continue

            try:
                cpu = float(cpu_match.group(1))
                ram = float(ram_match.group(1))
                disk =( float(disk_match.group(1))
                    if disk_match
                    else None
                )

                value = [cpu, ram]
                if disk is not None:
                    value.append(disk)

                if any(value < 0 or value > 100 for value in value):
                    invalid_count += 1
                    continue

            except ValueError:
                invalid_count += 1
                continue

            if cpu >= 90 or ram >= 90:
                severity = "CRITICAL"
            elif disk is not None and disk >= 90:
                severity = "CRITICAL"
            elif cpu >= 80 or ram >= 80:
                severity = "WARNING"
            elif disk is not None and disk >= 80:
                severity = "WARNING"
            else:
                severity = "INFO"

            if severity == "INFO":
                info_count += 1
            elif severity == "WARNING":
                warning_count += 1
            else:
                critical_count += 1

            output = (
                f"CPU: {cpu:.1f}% | RAM: {ram:.1f}%"
            )

            if disk is not None:
                output += f" | DISK: {disk:.1f}%"

            print(f"{output} | Severity: {severity}")

    print("=" * 45)
    print(f"INFO alerts: {info_count}")
    print(f"WARNING alerts: {warning_count}")
    print(f"CRITICAL alerts: {critical_count}")
    print(f"Invalid entries: {invalid_count}")

except FileNotFoundError:
    print(f"Error: {LOG_FILE} was not found.")
