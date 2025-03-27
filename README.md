# Keylogger

## Description
This is a simple keylogger script written in Python that records keystrokes and sends them via email. It captures keystrokes, saves them to a file, and periodically emails the log data.

## Features
- Records keystrokes in real-time
- Supports special characters and key combinations (Shift, AltGr)
- Logs public IP, local IP, and MAC address
- Sends captured data via email
- Can be added to system startup

## Prerequisites
Before running the script, ensure you have the following Python libraries installed:
```sh
pip install requests pynput winshell threading
```

## How to Use
1. Edit the script and replace the email credentials (`SENDER_EMAIL`, `APP_PASWORD`, `RECEIVER_EMAIL`) with your own.
2. Run the script:
```sh
python KLogger.py
```
3. To stop the script, manually terminate it in the terminal.

## Converting to an Executable
To convert the script into an executable file:
```sh
pyinstaller --onefile --noconsole keylogger.py
```

## Adding to Startup
This script can be added to startup by placing a shortcut in the `shell:startup` folder on Windows.

## Disclaimer
This script is for educational purposes only. Unauthorized use of keyloggers is illegal and unethical. The author is not responsible for any misuse of this code.

