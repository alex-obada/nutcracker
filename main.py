from argparser import parse_arguments
from execute import nmap_scan, extract_enumeration_commands, execute_command
from ai_engine import analyze_nmap_result
from reporter import generate_ai_report
import os

def main():
    #vreau sa dau paramentru un target
    args = parse_arguments()  # Aici apelezi funcția ta din argparser
    target = args.target       # Aici extragi efectiv argumentul target
    
    nmap_result = nmap_scan(target)
    first_json = analyze_nmap_result(nmap_result)
    if first_json:
        generate_ai_report(first_json)

        # Extragem comenzile
        commands = extract_enumeration_commands(first_json, target)

        # Folder pentru outputs
        os.makedirs("EnumerationOutputs", exist_ok=True)
        output_file_path = os.path.join("EnumerationOutputs", "combined_output.txt")

        # Executăm fiecare comandă și adunăm output-ul
        with open(output_file_path, "w", encoding="utf-8") as f:
            for idx, cmd in enumerate(commands):
                print(f"[+] Executăm comanda {idx+1}: {cmd}")
                output = execute_command(cmd)
                if output:
                    f.write(f"==================== Comanda {idx+1}: {cmd} ====================\n")
                    f.write(output)
                    f.write("\n\n")

        # Citim toate output-urile combinate
        
        
    
    else:
        print("[-] Nu s-a putut genera raportul inițial.")
    

    
if __name__ == '__main__':
    main()