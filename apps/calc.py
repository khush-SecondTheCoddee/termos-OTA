import math

Y = '\033[93m' ; W = '\033[0m' ; R = '\033[91m'

def main():
    print(f"{Y}--- TermuxPro Advanced Calc ---{W}")
    print("Example: 2 + 2, math.sqrt(16), math.sin(90)")
    
    while True:
        expr = input("calc » ").strip()
        if expr.lower() in ['q', 'exit']: break
        try:
            # Dangerous in real OS, but fine for a private Python project
            result = eval(expr)
            print(f"Result: {Y}{result}{W}")
        except Exception as e:
            print(f"{R}Error: {e}{W}")

if __name__ == "__main__":
    main()
