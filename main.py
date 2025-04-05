import argparse

def main():

    # dat context la ai
    # inclusiv templateurile cu comenzile tre sa apara aici
    
    
    parser = argparse.ArgumentParser(description="Exemplu cu argparse")
    parser.add_argument("target", help="domain-ul sau ip-ul masinii")
    parser.add_argument("--learning", help="",) # pentru sfaturi


    args = parser.parse_args()
    
    # scanarea initiala cu nmap
    # provocata de ai la care ii dam acces la shell
    
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
    