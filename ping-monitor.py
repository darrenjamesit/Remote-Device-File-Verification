import subprocess
import time
import platform
import os
import sys
from pathlib import Path
import smtplib, ssl

#oh wait you will actually need to install plyer first
try:
    from plyer import notification
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "plyer"])
    from plyer import notification

#boilerplate for setting up email server
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
#i made another email here that I didn't mind giving the password for to my colleagues
sender_email = "sender_email@gamil.com"
#i made the password part be an input rather than hardcoded so I don't put the password here in plaintext
password = input("Type your password and press enter: ")
#put your email address here where you want to receive the notification that the device is online:
receiver_email = "receiver_email@gmail.com"

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
    except Exception as e:
        print(f"error: {e}")
        return False


#this part makes the windows hello notification
def send_notification(title, message):
    notification.notify(title=title, message=message, timeout=5)


#main function that actually does all the stuff, it also opens the email server and closes it after sending the message
def run_monitor():
    timey_whimey = datetime.datetime.now().replace(microsecond=0)
    print(f'\nMonitoring started at {timey_whimey}.')
    targets = load_targets()
    status = {name: False for name in targets}
    print("\nAttempting to connect to:\n")
    i = 1
    for key, value in targets.items():
        print(f'{i}.  {key}:  {value} (is not online)')
        i += 1
    # i = len(targets)
    while True:
        targets = load_targets()
        for name, ip in targets.items():
            online = is_online(ip)
            if online and not status.get(name, False):
                msg = f"{name} ({ip}) is ONLINE!"
                current_time = datetime.datetime.now()
                time_str = current_time.strftime("%H:%M")
                print(f"\n[+] {msg} at {time_str}\n")

                #here the email server connection opens
                #you can customise this message however you want, the email will have no subject when you receive it but for some reason you cannot delete the "Subject" part
                message = f"""\
                From: {sender_email}
                To: {receiver_email}
                Subject: Device {name} Online!
            
                --------------------------------------------------------------------------------
            
                Guten tag!
            
                The device {name} is online now at {time_str}.
                    
                Hostname: {ip}
            
                Sent from Python :)"""
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receiver_email, message)
                    #closes the email server

                #invokes windows hello
                send_notification("Host Online", msg)
            status[name] = 'online'
        time.sleep(5)




if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "add":
        add_target_interactively()
    else:
        run_monitor()
