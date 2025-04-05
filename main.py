from argparser import parse_arguments
from ai_engine import decide_initial_strategy
from execute import execute_strategy
import sys

def main():
    args = parse_arguments()

    target_input = args.target
    context = args.context
    learn = args.learn

    strategy = decide_initial_strategy(target_input, context, learn)
    if not strategy:
        print("[-] AI-ul nu a returnat o strategie validă.")
        sys.exit(1)

    execute_strategy(strategy)
    print("[+] Scanarea a fost executată cu succes.")

if __name__ == '__main__':
    main()