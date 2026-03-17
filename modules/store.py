import os
import requests
import json
import time
import importlib.util

# --- UI COLORS ---
G = '\033[92m' ; R = '\033[91m' ; B = '\033[94m' 
Y = '\033[93m' ; C = '\033[96m' ; W = '\033[0m'

class AppStore:
    def __init__(self):
        self.repo_owner = "khush-SecondTheCoddee"
        self.repo_name = "termos-OTA"
        self.raw_url = f"https://raw.githubusercontent.com/{self.repo_owner}/{self.repo_name}/main/"
        self.catalog_url = self.raw_url + "catalog.json"
        self.module_dir = "modules"
        self.local_manifest_path = ".sys_manifest.json"

    def get_catalog(self):
        try:
            print(f"{B}[-] Fetching App Catalog...{W}")
            res = requests.get(self.catalog_url, timeout=5)
            if res.status_code == 200:
                return res.json()
            return None
        except Exception as e:
            print(f"{R}[!] Store Offline: {e}{W}")
            return None

    def install_app(self, app_filename, app_info):
        try:
            # Construct the download URL from the 'path' in catalog.json
            download_url = self.raw_url + app_info["path"]
            
            print(f"{Y}[*] Downloading {app_filename}...{W}")
            res = requests.get(download_url, timeout=10)
            
            if res.status_code == 200:
                # Save into the local modules folder
                local_path = os.path.join(self.module_dir, app_filename)
                with open(local_path, "w") as f:
                    f.write(res.text)
                
                # Update local manifest so the Kernel tracks this new file
                if os.path.exists(self.local_manifest_path):
                    with open(self.local_manifest_path, "r") as f:
                        data = json.load(f)
                    
                    data["files"][app_filename] = {"ver": app_info["ver"]}
                    
                    with open(self.local_manifest_path, "w") as f:
                        json.dump(data, f)
                
                print(f"{G}✔ {app_filename} installed successfully!{W}")
                time.sleep(1)
            else:
                print(f"{R}[!] Download failed (HTTP {res.status_code}).{W}")
        except Exception as e:
            print(f"{R}[!] Installation Error: {e}{W}")

    def menu(self):
        os.system('clear')
        catalog = self.get_catalog()
        if not catalog: 
            print(f"{R}Could not load catalog. Check your internet.{W}")
            time.sleep(2)
            return

        print(f"{C}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓{W}")
        print(f"{C}┃        TERMUX-PRO OFFICIAL STORE       ┃{W}")
        print(f"{C}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{W}")
        
        apps_list = list(catalog["apps"].keys())
        
        for i, app_name in enumerate(apps_list):
            info = catalog["apps"][app_name]
            print(f"{Y}{i+1}.{W} {G}{app_name:15}{W} | {info['desc']}")
        
        print(f"\n{B}Enter number to install, or 'q' to go back.{W}")
        choice = input(f"{C}store » {W}").strip()
        
        if choice.lower() == 'q':
            return
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(apps_list):
                selected_app = apps_list[idx]
                self.install_app(selected_app, catalog["apps"][selected_app])
            else:
                print(f"{R}Invalid selection.{W}")
                time.sleep(1)
        else:
            print(f"{R}Invalid input.{W}")
            time.sleep(1)

def main():
    store = AppStore()
    store.menu()

if __name__ == "__main__":
    main()
