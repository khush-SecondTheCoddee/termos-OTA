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
        """Dynamically imports a module from the local modules folder."""
        path = f"modules/{name}.py"
        if not os.path.exists(path):
            print(f"{R}[!] Module {name} not found locally.{W}")
            return None
        try:
            spec = importlib.util.spec_from_file_location(name, path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod
        except Exception as e:
            print(f"{R}[!] Error loading {name}: {e}{W}")
            return None

    def banner(self):
        os.system('clear')
        print(f"{C}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓{W}")
        print(f"{C}┃  TermuxPro Modular Shell v2.0      ┃{W}")
        print(f"{C}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{W}")
        print(f"User: {G}{self.user}{W} | Host: {Y}{self.host}{W} | Ver: {B}9.0{W}")

    def run_shell(self):
        self.banner()
        while self.running:
            try:
                t = datetime.datetime.now().strftime("%H:%M")
                # Professional Powerline Prompt
                prompt = f"\n{B}{W} {G}{self.user}@{self.host}{W} {B}{W} {t}\n{C}» {W}"
                
                inp = input(prompt).strip().split()
                if not inp: continue
                
                cmd = inp[0].lower()
                args = inp[1:]

                # --- 1. CORE SYSTEM COMMANDS ---
                if cmd == "exit":
                    print(f"{Y}Exiting Shell...{W}")
                    self.running = False
                
                elif cmd == "clear":
                    self.banner()

                elif cmd == "sys":
                    print(f"{B}Kernel Version:{W} 9.0 (Delta Engine)")
                    print(f"{B}Platform:      {W} {platform.system()} {platform.release()}")
                    print(f"{B}Architecture:  {W} {platform.machine()}")

                # --- 2. SECURITY COMMANDS ---
                elif cmd == "lock":
                    auth = self.load_mod("auth")
                    if auth and hasattr(auth, 'main'):
                        if not auth.main(): self.running = False

                # --- 3. HARDWARE COMMANDS (via tools.py) ---
                elif cmd in ["speak", "vibrate", "batt"]:
                    tools = self.load_mod("tools")
                    if tools:
                        t_obj = tools.SystemTools()
                        if cmd == "speak": t_obj.play_tts(" ".join(args))
                        elif cmd == "vibrate": t_obj.haptic_feedback()
                        elif cmd == "batt": t_obj.get_battery()

                # --- 4. APP STORE (via store.py) ---
                elif cmd == "store":
                    store = self.load_mod("store")
                    if store and hasattr(store, 'main'):
                        store.main()

                # --- 5. EXECUTE DOWNLOADED APPS ---
                elif cmd == "run":
                    if not args:
                        print(f"{Y}Usage: run <app_name.py>{W}")
                    else:
                        app_name = args[0].replace(".py", "")
                        app = self.load_mod(app_name)
                        if app and hasattr(app, 'main'):
                            app.main()

                # --- 6. FILE SYSTEM ---
                elif cmd == "ls":
                    files = os.listdir("modules")
                    print(f"{B}Installed Modules/Apps:{W}")
                    for f in files:
                        if f.endswith(".py"):
                            print(f" {G}•{W} {f}")

                elif cmd == "help":
                    print(f"{Y}SYSTEM: {W}clear, sys, lock, exit")
                    print(f"{Y}APPS:   {W}store, ls, run <app>")
                    print(f"{Y}TOOLS:  {W}speak, vibrate, batt")

                else:
                    print(f"{R}Unknown command: {cmd}{W}")

            except KeyboardInterrupt:
                print(f"\n{Y}[!] Use 'exit' to logout safely.{W}")
            except Exception as e:
                print(f"{R}[!] Shell Error: {e}{W}")

def main():
    shell = TermuxShell()
    shell.run_shell()

if __name__ == "__main__":
    main()
