Advance Keylogger with Email Logger and Auto-Startup (Educational Use Only)
What this project does:
1.	 Records all keystrokes typed on your computer
2.	 Logs active window title with timestamp
3.	 Saves logs to a hidden folder in your system
4.	 Sends logs to your email every 2 minutes
5.	 Adds itself to Startup (auto-runs after restart)
6.	 Runs silently in background (no console window shown)
________________________________________
🔧 Technologies Used:
•	Python
•	pynput – to capture keyboard input
•	schedule – to send emails on time
•	win32gui, win32com.client – to get active window and create shortcut
•	smtplib, email – to send email
•	ctypes – to hide the window
________________________________________
 Setup Instructions:
1.	 Install required Python libraries:
                      pip install pynput schedule pywin32
2.	 Edit these 3 lines in the script with your Gmail:
                       SENDER_EMAIL = "your_email@gmail.com"
                       SENDER_PASSWORD = "your_gmail_app_password"
                        RECEIVER_EMAIL = "your_email@gmail.com"
 If Gmail blocks access:
•	Go to: https://myaccount.google.com/apppasswords
•	Generate an App Password
•	Use that instead of your real password
________________________________________
How to Run the Script:
python your_script_name.py
 It will:
•	Start recording keys
•	Run in background (no window)
•	Send logs to email every 2 minutes
•	Add itself to startup folder
________________________________________
 How to Stop the Keylogger:
1.	Press Ctrl + Shift + Esc to open Task Manager
2.	Find systemprocess.exe under Background Processes
3.	Right-click → End Task
________________________________________
 How to Fully Remove:
1.	Delete file from:
C:\Users\<your_name>\AppData\Roaming\SystemLogs\systemprocess.exe
2.	Delete shortcut from:
C:\Users\<your_name>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\systemprocess.lnk
3.	Also delete:
keystrokes.txt
________________________________________
 Legal Warning (Must Read):
 This software is only for educational and ethical testing on your own computer.
Using it on someone else's device without permission is illegal and punishable under IT Act (India) 
