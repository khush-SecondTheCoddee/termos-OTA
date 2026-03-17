import os
import datetime
import platform
import socket
import time
import importlib.util

# --- UI COLORS ---
G = '\033[92m' ; R = '\033[91m' ; B = '\033[94m' 
Y = '\033[93m' ; C = '\033[96m' ; W = '\033[0m'

class TermuxShell:
    def __init__(self):
        self.user = "admin"
        self.host = self.get_ip()
        self.running = True

    def get_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 1))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except: return "127.0.0.1"

    def load_mod(self, name):
        """Helper to dynamically link other modules."""
        path = f"modules/{name}.py"
        if not os.path.exists(path):
            print(f"{R}[!] Module {name} not found.{W}")
            return None
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def banner(self):
        os.system('clear')
        print(f"{C}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓{W}")
        print(f"{C}┃  TermuxPro Modular Shell v1.5      ┃{W}")
        print(f"{C}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{W}")
        print(f"Connected as: {G}{self.user}{W} | IP: {Y}{self.host}{W}")

    def run(self):
        self.banner()
        while self.running:
            try:
                t = datetime.datetime.now().strftime("%H:%M")
                # Powerline Style Prompt
                prompt = f"\n{B}{W} {G}{self.user}@{self.host}{W} {B}{W} {t}\n{C}» {W}"
                
                inp = input(prompt).strip().split()
                if not inp: continue
                
                cmd = inp[0].lower()
                args = inp[1:]

                # --- SYSTEM COMMANDS ---
                if cmd == "exit":
                    print(f"{Y}Returning control to Kernel...{W}")
                    self.running = False
                
                elif cmd == "clear":
                    os.system('clear')
                    self.banner()

                elif cmd == "sys":
                    print(f"{B}Kernel Version:{W} 9.0 (Delta)")
                    print(f"{B}Architecture: {W} {platform.machine()}")
                    print(f"{B}Python:       {W} {platform.python_version()}")

                # --- HARDWARE (Links to tools.py) ---
                elif cmd in ["speak", "vibrate", "batt"]:
                    tools = self.load_mod("tools")
                    if tools:
                        t_obj = tools.SystemTools()
                        if cmd == "speak": t_obj.play_tts(" ".join(args))
                        elif cmd == "vibrate": t_obj.haptic_feedback()
                        elif cmd == "batt": t_obj.get_battery()

                # --- APP STORE (Links to store.py) ---
                elif cmd == "store":
                    store = self.load_mod("store")
                    if store: store.main()

                # --- SECURITY (Links to auth.py) ---
                elif cmd == "lock":
                    auth = self.load_mod("auth")
                    if auth: 
                        if not auth.main(): self.running = False

                elif cmd == "help":
                    print(f"{Y}SYSTEM: {W}clear, sys, lock, exit")
                    print(f"{Y}FILES:  {W}ls, cat, edit")
                    print(f"{Y}TOOLS:  {W}speak, vibrate, batt, store")

                else:
                    print(f"{R}Unknown command: {cmd}{W}")

            except KeyboardInterrupt:
                print(f"\n{Y}Interrupted. Type 'exit' to shutdown.{W}")
            except Exception as e:
                print(f"{R}Shell Logic Error: {e}{W}")

def main():
    shell = TermuxShell()
    shell.run()

if __name__ == "__main__":
    main()
