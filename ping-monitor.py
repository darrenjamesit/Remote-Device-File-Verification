import subprocess
import time
import platform
import os
import sys
from pathlib import Path

#oh wait you will actually need to install plyer first
try:
    from plyer import notification
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "plyer"])
    from plyer import notification

#so here you can either manually paste in the path to the target file everytime you start the script
username_path = str(input("paste the path where your targets.txt file wil be or just press enter if you have hardcoded the path"))

if username:
    TARGET_FILE = f'''{username_path}/targets.txt'''
else:
    #or you can modify the script directly to hardcode the path and just delete the above if statement
    TARGET_FILE = "C:/Users/DarrenSmart/targets.txt"

#loads the target devices from the .txt file
def load_targets():
    path = Path(TARGET_FILE)
    path.touch(exist_ok=True)
    targets = {}
    with open(path, "r") as f:
        for line in f:
            if line.strip():
                parts = line.strip().split(",")
                if len(parts) == 2:
                    name, ip = parts
                    targets[name.strip()] = ip.strip()
    return targets


#pings the devices
def is_online(host):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        subprocess.check_output(["ping", param, "1", host], stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False


#this part makes the windows hello notification
def send_notification(title, message):
    notification.notify(title=title, message=message, timeout=5)


#main function that actually does all the stuff
def run_monitor():
    print("Monitoring started. Press Ctrl+C to stop.")
    targets = load_targets()
    status = {name: False for name in targets}

    while True:
        targets = load_targets()
        for name, ip in targets.items():
            online = is_online(ip)
            if online and not status.get(name, False):
                message = f"{name} ({ip}) is ONLINE!"
                print(f"[+] {message}")
                send_notification("Host Online", message)
            status[name] = online
        time.sleep(5)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "add":
        add_target_interactively()
    else:
        run_monitor()
