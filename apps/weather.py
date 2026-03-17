import requests
import os

# COLORS
G = '\033[92m' ; C = '\033[96m' ; W = '\033[0m'

def main():
    print(f"{C}--- TermuxPro Weather Service ---{W}")
    city = input("Enter City Name (Leave blank for Auto-Detect): ").strip()
    
    # Using wttr.in for terminal-friendly weather
    url = f"https://wttr.in/{city}?0fqT"
    try:
        res = requests.get(url)
        print(f"\n{G}Weather Report:{W}")
        print(res.text)
    except:
        print("Error: Could not connect to weather server.")

if __name__ == "__main__":
    main()
