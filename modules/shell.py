import os
import datetime
import platform
import socket

# UI COLORS
G = '\033[92m' ; R = '\033[91m' ; B = '\033[94m' 
Y = '\033[93m' ; C = '\033[96m' ; W = '\033[0m'

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except: return "127.0.0.1"

def main():
    """This is the entry point called by kernel.py"""
    running = True
    username = "admin" # This can be linked to auth.py later
    
    os.system('clear')
    print(f"{C}--- TermuxPro Shell Module v1.0 ---{W}")
    print(f"Type {Y}'help'{W} for a list of available commands.")

    while running:
        try:
            ip = get_ip()
            t = datetime.datetime.now().strftime("%H:%M")
            
            # Professional Powerline Prompt
            prompt = f"\n{B}{W} {G}{username}@{ip}{W} {B}{W} {t}\n{C}» {W}"
            
            inp = input(prompt).strip().split()
            if not inp: continue
            
            cmd = inp[0].lower()
            args = inp[1:]

            if cmd == "exit":
                print(f"{Y}Shutting down shell...{W}")
                running = False
            
            elif cmd == "clear":
                os.system('clear')
                
            elif cmd == "sys":
                print(f"{B}OS Version:{W} 8.5 (Delta Kernel)")
                print(f"{B}Node:      {W} {platform.node()}")
                print(f"{B}Arch:      {W} {platform.machine()}")
                
            elif cmd == "ls":
                # Lists real files in the current Termux directory
                files = os.listdir('.')
                for f in files:
                    color = G if os.path.isdir(f) else W
                    print(f"{color}{f}{W}", end="  ")
                print()

            elif cmd == "help":
                print(f"{Y}Available Commands:{W}")
                print("  ls      - List current directory files")
                print("  sys     - Show system hardware info")
                print("  clear   - Clear terminal screen")
                print("  update  - (Handled by Kernel on reboot)")
                print("  exit    - Close the OS")

            else:
                print(f"{R}Error: Command '{cmd}' not recognized.{W}")

        except KeyboardInterrupt:
            print(f"\n{Y}Use 'exit' to close the system.{W}")
        except Exception as e:
            print(f"{R}Shell Error: {e}{W}")

if __name__ == "__main__":
    main()
