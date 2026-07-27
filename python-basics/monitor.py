import requests
import datetime
import os
import subprocess

SERVICES_FILE = "services.txt"
LOG_FILE = "monitor.log"

def log_message(service, status, message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as log:
        log.write(f"[{timestamp}] {service}: {status} - {message}\n")

def check_http_service(url, timeout=5):
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code >= 500:
            return "ERROR", f"HTTP {response.status_code}"
        elif response.status_code >= 400:
            return "WARNING", f"HTTP {response.status_code}"
        else:
            return "OK", f"HTTP {response.status_code}"
    except requests.exceptions.Timeout:
        return "ERROR", "Timeout"
    except requests.exceptions.ConnectionError:
        return "ERROR", "Connection failed"
    except Exception as e:
        return "ERROR", str(e)

def ping_host(hostname):
    try:
        result = subprocess.run(
            ["ping", "-c", "5", "-W", "2", hostname],
            capture_output=True,
            timeout=6
        )
        if result.returncode == 0:
            return "OK", "Ping successful"
        else:
            return "ERROR", "Ping failed"
    except subprocess.TimeoutExpired:
        return "ERROR", "Ping timeout"
    except Exception as e:
        return "ERROR", str(e)

services = []
if os.path.exists(SERVICES_FILE):
    with open(SERVICES_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                services.append(line)
else:
    print(f"Creating {SERVICES_FILE}...")
    with open(SERVICES_FILE, "w") as f:
        f.write("https://google.com\n")
        f.write("https://github.com\n")
    services = ["https://google.com", "https://github.com"]

print(f"Checking {len(services)} services...")

for url in services:
    status, message = check_http_service(url)
    log_message(url, status, message)
    print(f"{url}: {status} ({message})")

ping_targets = ["8.8.8.8", "1.1.1.1"]

print("\nChecking ping targets...")
for host in ping_targets:
    status, message = ping_host(host)
    log_message(host, status, message)
    print(f"{host}: {status} ({message})")

print(f"\nResults written to {LOG_FILE}")
