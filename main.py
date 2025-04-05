from argparser import parse_arguments
from execute import nmap_scan
from ai_engine import analyze_nmap_result
from reporter import generate_ai_report

def main():
    #vreau sa dau paramentru un target
    args = parse_arguments()  # Aici apelezi funcția ta din argparser
    target = args.target       # Aici extragi efectiv argumentul target
    
    nmap_result = nmap_scan(target)
    first_json = analyze_nmap_result(nmap_result)
    if first_json:
        generate_ai_report(first_json)
    else:
        print("[-] Nu s-a putut genera raportul.")
    
if __name__ == '__main__':
    main()