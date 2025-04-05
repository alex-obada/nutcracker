import os
import argparser
import execute
import ai_engine
import reporter

def main():
    args = argparser.parse_arguments()
    target = args.target

    # Pasul 1: Scanare Nmap
    nmap_result = execute.nmap_scan(target)
    first_json = ai_engine.analyze_nmap_result(nmap_result)

    if first_json:
        reporter.generate_ai_report(first_json)

        # Pasul 2: Extragem comenzile de recon
        recon_commands = execute.extract_enumeration_commands(first_json, target)

        # Creăm folder pentru output-urile de enumerare
        os.makedirs("EnumerationOutputs", exist_ok=True)
        output_file_path = os.path.join("EnumerationOutputs", "combined_output.txt")

        # Executăm comenzile de recon și salvăm output-ul
        with open(output_file_path, "w", encoding="utf-8") as f:
            for idx, cmd in enumerate(recon_commands, 1):
                print(f"[+] Executăm comanda de recon {idx}: {cmd}")
                output = execute.execute_command(cmd, allow_install=True)
                if output:
                    f.write(f"==================== Comanda {idx}: {cmd} ====================\n")
                    f.write(output)
                    f.write("\n\n")

        # Pasul 3: Analizăm output-ul de enumerare
        with open(output_file_path, "r", encoding="utf-8") as f:
            all_outputs = f.read()
        
        second_json = ai_engine.analyze_enumeration_outputs(all_outputs)
        if second_json:
            reporter.display_findings_report(second_json)

            # Pasul 4: Extragem comenzi de atac
            attack_commands = execute.extract_attack_commands(second_json)
            print(second_json)
            if attack_commands:
                os.makedirs("Reports/Attack", exist_ok=True)

                for idx, cmd in enumerate(attack_commands, 1):
                    print(f"[+] Executăm comanda de atac {idx}: {cmd}")
                    output = execute.execute_command(cmd, allow_install=False)

                    # Salvăm fiecare output într-un fișier separat
                    attack_output_file = f"Reports/Attack/attack_{idx}.txt"
                    with open(attack_output_file, "w", encoding="utf-8") as f:
                        f.write(f"Comandă executată: {cmd}\n\n")
                        f.write(output)

                    print(f"[+] Output salvat în {attack_output_file}")
            else:
                print("[-] Nu au fost generate comenzi de atac suplimentare.")
        else:
            print("[-] Nu s-au putut analiza output-urile de enumerare.")
    else:
        print("[-] Nu s-a putut genera raportul inițial.")

if __name__ == '__main__':
    main()
