from argparser import parse_arguments
from ai_engine import decide_initial_command
import subprocess
import sys


def main():

    # dat context la ai
    # inclusiv templateurile cu comenzile tre sa apara aici
    args = parse_arguments()
    

    target_input = args.target  
    context = args.context
    learn = args.learn


    # if not target_input:
    #     print("[-] Eroare: Target invalid sau nerezolvabil.")
    #     sys.exit(1)

    # target_ip = resolve_target(target_input)
    # if not target_ip:
    #     print("[-] Eroare: Nu am putut rezolva domeniul/target-ul.")
    #     sys.exit(1)

    # if not is_target_reachable(target_ip):
    #     print("[-] Target-ul nu este accesibil (ping failed).")
    #     sys.exit(1)


    # scanarea initiala cu nmap
    # provocata de ai la care ii dam acces la shell
    
    command = decide_initial_command(target_input, context, learn)
    if not command:
        print("[-] AI-ul nu a returnat o comandă validă.")
        sys.exit(1)

    # bucla de self-promptint si rulare continua pana nu ii zice utilizator sa se opreasca
    
    '''
    comanda initiala (rularea)
    
    while(true)
        ai ul ia decizie ce comanda sa foloseasca in functie de inputul utilizatorului
        
        ai-ul ruleaza comanda
        
        in functie de ce a gasit iti arata in format condensat si te intreaba ce vrei sa faci (aicea ii si punctu in care utilizatorul poate sa opreasca executia)
        
        if(ii gata)
            ultimul prompt al ai ului va fi un raport cu tot ce s-a gasit 
        
        
    
    '''
    


if __name__ == '__main__':
    main()
    