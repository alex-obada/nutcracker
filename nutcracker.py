#!/usr/bin/env python3
import modules.argparser as argparser
import modules.execute as execute
import modules.ai_engine as ai_engine
import modules.reporter as reporter
import os
import time

def main():
    banner = r"""
  _   _       _                      _             
 | \ | |     | |                    | |            
 |  \| |_   _| |_ ___ _ __ __ _  ___| | _____ _ __ 
 | . ` | | | | __/ __| '__/ _` |/ __| |/ / _ \ '__|
 | |\  | |_| | || (__| | | (_| | (__|   <  __/ |   
 |_| \_|\__,_|\__\___|_|  \__,_|\___|_|\_\___|_|   
                                                  
                                                  
    """
    print(banner)
    print("⚠️  WARNING: This tool is for educational purposes only. Use responsibly and ethically.\n")
   
    time.sleep(4)

    # 1. Parsăm argumentele
    args = argparser.parse_arguments()
    target = args.target

    # 2. Scanăm cu Nmap
    nmap_output = execute.nmap_scan(target)

    # 3. Analizăm rezultatul cu AI
    strategy = ai_engine.analyze_nmap_result(nmap_output)
    if not strategy:
        print("[-] Eroare: nu s-a putut analiza scanarea Nmap.")
        return

    # 4. Generăm raport AI pentru Recon
    reporter.generate_ai_report(strategy)

    # 5. Extragem comenzile de recon
    recon_commands = execute.extract_enumeration_commands(strategy, target)

    # 6. Executăm comenzile de recon și salvăm output-urile
    os.makedirs("EnumerationOutputs", exist_ok=True)
    enumeration_output_file = "EnumerationOutputs/combined_output.txt"

    with open(enumeration_output_file, "w", encoding="utf-8") as f:
        for idx, cmd in enumerate(recon_commands, 1):
            print(f"[+] Executăm comanda de recon {idx}: {cmd}")
            output = execute.execute_command(cmd, allow_install=True)
            f.write(f"==================== Comanda {idx}: {cmd} ====================\n")
            f.write(output + "\n\n")

    # 7. Analizăm rezultatul recon-ului cu AI
    with open(enumeration_output_file, "r", encoding="utf-8") as f:
        combined_output = f.read()

    findings = ai_engine.analyze_enumeration_outputs(combined_output)

    if not findings:
        print("[-] Nu s-au identificat vulnerabilități suplimentare.")
        return

    # 8. Generăm raport AI pentru findings
    reporter.display_findings_report(findings)

    reporter.generate_final_markdown_report(strategy, findings)

    message = """
\033[92m
╔════════════════════════════════════════════════════════════════════════════════════╗
║  Dacă aveți nevoie de ajutor suplimentar în soluționarea problemelor dumneavoastră ║
║  echipa Nutcracker vă recomandă să îi contactați pe experții de la Zerotak.        ║
║                                                                                    ║
║  📧 Email de contact: collaboration@zerotak.com                                    ║
╚════════════════════════════════════════════════════════════════════════════════════╝
\033[0m
"""
    print(message)


if __name__ == "__main__":
    main()
