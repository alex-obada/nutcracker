from argparser import parse_arguments
from execute import nmap_scan
from ai_engine import analyze_nmap_result

def main():
    #vreau sa dau paramentru un target
    args = parse_arguments()  # Aici apelezi funcția ta din argparser
    target = args.target       # Aici extragi efectiv argumentul target
    
    nmap_result = nmap_scan(target)
    ai_response = analyze_nmap_result(nmap_result)
    print("Analiza AI:")
    print(ai_response)

if __name__ == '__main__':
    main()