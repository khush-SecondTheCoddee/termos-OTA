import os
import requests
import json
import time

# UI COLORS
G = '\033[92m' ; R = '\033[91m' ; B = '\033[94m' 
Y = '\033[93m' ; C = '\033[96m' ; W = '\033[0m'

class AppStore:
    def __init__(self):
        # You can create a second file on GitHub called 'catalog.json' for the store
        self.repo_raw = "https://raw.githubusercontent.com/khush-SecondTheCoddee/termos-OTA/main/"
        self.catalog_url = self.repo_raw + "catalog.json"
        self.module_dir = "modules"
        self.local_manifest = ".sys_manifest.json"

    def get_catalog(self):
        try:
            print(f"{B}[-] Fetching App Catalog...{W}")
            res = requests.get(self.catalog_url, timeout=5)
            if res.status_code == 200:
                return res.json()
            return None
        except:
            print(f"{R}[!] Store Offline.{W}")
            return None

        # Update inside store.py
def install_app(self, app_name, app_info):
    # Use the specific path defined in catalog.json
    download_url = self.repo_raw + app_info["path"]
    res = requests.get(download_url)
    # Still saves into the phone's modules/ folder for easy execution
    with open(os.path.join(self.module_dir, app_name), "w") as f:
        f.write(res.text)

                
                # Update local manifest so the Kernel recognizes it
                if os.path.exists(self.local_manifest):
                    with open(self.local_manifest, "r") as f:
                        data = json.load(f)
                    data["files"][app_name] = {"ver": app_info["ver"]}
                    with open(self.local_manifest, "w") as f:
                        json.dump(data, f)
                
                print(f"{G}✔ {app_name} installed successfully!{W}")
            else:
                print(f"{R}[!] Download failed.{W}")
        except Exception as e:
            print(f"{R}[!] Error: {e}{W}")

    def menu(self):
        catalog = self.get_catalog()
        if not catalog: return

        print(f"\n{C}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓{W}")
        print(f"{C}┃   TermuxPro App Store        ┃{W}")
        print(f"{C}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{W}")
        
        apps = list(catalog["apps"].keys())
        for i, app in enumerate(apps):
            desc = catalog["apps"][app]["desc"]
            print(f"{Y}{i+1}.{W} {G}{app}{W} - {desc}")
        
        print(f"\n{B}Type the number to install or 'q' to exit.{W}")
        choice = input(f"{C}store » {W}").strip()
        
        if choice.isdigit() and int(choice) <= len(apps):
            selected = apps[int(choice)-1]
            self.install_app(selected, catalog["apps"][selected])
        elif choice.lower() == 'q':
            return

def main():
    store = AppStore()
    store.menu()

if __name__ == "__main__":
    main()
