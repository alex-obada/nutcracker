from argparser import parse_arguments
from execute import nmap_scan

def main():
    #vreau sa dau paramentru un target
    args = parse_arguments()  # Aici apelezi funcția ta din argparser
    target = args.target       # Aici extragi efectiv argumentul target
    
    nmap_scan(target)


if __name__ == '__main__':
    main()