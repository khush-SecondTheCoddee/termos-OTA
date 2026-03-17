import os
import requests
import json

# UI COLORS
G = '\033[92m' ; R = '\033[91m' ; B = '\033[94m' 
Y = '\033[93m' ; C = '\033[96m' ; W = '\033[0m'

class SystemTools:
    def __init__(self):
        self.vfs_file = "drive.json"

    def get_battery(self):
        """Fetches live battery data from Android."""
        print(f"{B}[*] Accessing Power Management...{W}")
        os.system("termux-battery-status")

    def play_tts(self, message):
        """Makes the OS speak."""
        if not message:
            print(f"{R}Error: Speak command needs a message.{W}")
            return
        print(f"{G}[🎤] Speaking: {message}{W}")
        os.system(f"termux-tts-speak '{message}'")

    def haptic_feedback(self, duration=500):
        """Vibrates the phone."""
        print(f"{C}[!] Haptic Pulse Sent.{W}")
        os.system(f"termux-vibrate -d {duration}")

    def fetch_web_data(self, url):
        """A mini-downloader tool for the OS."""
        try:
            print(f"{Y}[~] Downloading from: {url}{W}")
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                print(f"{G}✔ Data Received ({len(res.text)} bytes){W}")
                return res.text
            else:
                print(f"{R}❌ Error: {res.status_code}{W}")
        except Exception as e:
            print(f"{R}Network Error: {e}{W}")

def main():
    """Tools usually act as a library for the Shell, but can be run directly."""
    tools = SystemTools()
    print(f"{C}--- TermuxPro Tools Library ---{W}")
    print("This module provides hardware hooks for the Kernel.")

if __name__ == "__main__":
    main()
