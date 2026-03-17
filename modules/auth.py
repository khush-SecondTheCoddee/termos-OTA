import os
import hashlib
import getpass
import time

# UI COLORS
G = '\033[92m' ; R = '\033[91m' ; B = '\033[94m' 
Y = '\033[93m' ; C = '\033[96m' ; W = '\033[0m'

class AuthSystem:
    def __init__(self):
        self.pass_file = ".sys_auth"
        self.recovery_key = "TERMUX-1234-SAFE" # Change this for your own security

    def hash_password(self, password):
        """Creates a secure SHA-256 hash."""
        return hashlib.sha256(password.encode()).hexdigest()

    def setup(self):
        """Runs if no password file is found."""
        print(f"{Y}[!] Initial Security Setup{W}")
        p1 = getpass.getpass("Create New System PIN: ")
        p2 = getpass.getpass("Confirm PIN: ")
        
        if p1 == p2 and len(p1) >= 4:
            with open(self.pass_file, "w") as f:
                f.write(self.hash_password(p1))
            print(f"{G}✔ PIN encrypted and saved.{W}")
            return True
        else:
            print(f"{R}❌ PINs do not match or too short (min 4).{W}")
            return False

    def authenticate(self):
        """The main login loop."""
        if not os.path.exists(self.pass_file):
            if not self.setup(): return False

        attempts = 0
        while attempts < 3:
            print(f"\n{B}🔒 SYSTEM LOCKED{W}")
            entered = getpass.getpass("ENTER PIN: ")

            # Check for Recovery Key Bypass
            if entered == self.recovery_key:
                print(f"{C}[!] Recovery Key Accepted. Wiping old PIN...{W}")
                os.remove(self.pass_file)
                return self.setup()

            # Check against saved Hash
            with open(self.pass_file, "r") as f:
                saved_hash = f.read()

            if self.hash_password(entered) == saved_hash:
                print(f"{G}✔ Access Granted.{W}")
                time.sleep(0.5)
                return True
            else:
                attempts += 1
                print(f"{R}❌ Access Denied. ({3-attempts} left){W}")
        
        print(f"{R}Too many failed attempts. Locking process.{W}")
        return False

def main():
    """This allows the kernel to check auth before loading the shell."""
    auth = AuthSystem()
    return auth.authenticate()

if __name__ == "__main__":
    main()
