import time
import os
import sys
from datetime import datetime

# --- UI COLORS ---
C = '\033[96m'  # Cyan
Y = '\033[93m'  # Yellow
G = '\033[92m'  # Green
W = '\033[0m'   # Reset
HIDE = '\033[?25l' # Hide Cursor
SHOW = '\033[?25h' # Show Cursor

def main():
    os.system('clear')
    print(HIDE) # Hide the cursor for a cleaner look
    try:
        while True:
            # Get current time and date
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            current_date = now.strftime("%A, %d %B %Y")
            
            # Use \r (carriage return) to overwrite the same line
            # or clear screen for a centered box effect
            sys.stdout.write("\033[H") # Move cursor to top-left
            
            print(f"\n\n")
            print(f"   {C}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓{W}")
            print(f"   ┃{W}         SYSTEM DIGITAL CLOCK       {C}┃{W}")
            print(f"   ┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫{W}")
            print(f"   ┃{W}                                    {C}┃{W}")
            print(f"   ┃{Y}           {current_time}             {C}┃{W}")
            print(f"   ┃{G}      {current_date.center(26)}      {C}┃{W}")
            print(f"   ┃{W}                                    {C}┃{W}")
            print(f"   ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{W}")
            print(f"\n    {Y}Press Ctrl+C to return to Shell{W}")
            
            sys.stdout.flush()
            time.sleep(1)
            
    except KeyboardInterrupt:
        print(SHOW) # Restore cursor before exiting
        os.system('clear')
        print(f"{G}Exited Clock Service.{W}")

if __name__ == "__main__":
    main()
