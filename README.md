
```bash
 __    __              __                                             __                           
/  \  /  |            /  |                                           /  |                          
$$  \ $$ | __    __  _$$ |_     _______   ______   ______    _______ $$ |   __   ______    ______  
$$$  \$$ |/  |  /  |/ $$   |   /       | /      \ /      \  /       |$$ |  /  | /      \  /      \ 
$$$$  $$ |$$ |  $$ |$$$$$$/   /$$$$$$$/ /$$$$$$  |$$$$$$  |/$$$$$$$/ $$ |_/$$/ /$$$$$$  |/$$$$$$  |
$$ $$ $$ |$$ |  $$ |  $$ | __ $$ |      $$ |  $$/ /    $$ |$$ |      $$   $$<  $$    $$ |$$ |  $$/ 
$$ |$$$$ |$$ \__$$ |  $$ |/  |$$ \_____ $$ |     /$$$$$$$ |$$ \_____ $$$$$$  \ $$$$$$$$/ $$ |      
$$ | $$$ |$$    $$/   $$  $$/ $$       |$$ |     $$    $$ |$$       |$$ | $$  |$$       |$$ |      
$$/   $$/  $$$$$$/     $$$$/   $$$$$$$/ $$/       $$$$$$$/  $$$$$$$/ $$/   $$/  $$$$$$$/ $$/       
```


**Nutcracker** este o unealta open-source ce automatizeaza munca repetitiva a pentesterilor bazat pe ```ChatGPT``` si scris in Python.



## 📝 Descriere

Nutcracker primeste un target (ip/domain) si ii analizeaza porturile deschise folosind `nmap`. Ca urmator pas tot ce a rezultat din scanare este redirectionat in `gpt-4-turbo`, iar acesta construieste un raport mai detaliat cu ce s-ar putea face pentru a se exploata orice vulnerabilitati care ar exista pe respectivul calculator. Aceasta operatie se realizeaza de doua ori pentru ca AI-ul sa-si mareasca contextul cu informatii de pe surse reputabile cum ar fi:
- https://www.hackingarticles.in/penetration-testing/
- https://book.hacktricks.wiki/en/index.html
- https://attack.mitre.org/

Prin aceasta iterare AI-ul va genera si comenzi de terminal care vor fi folosite pentru a ataca victima in cazul in care aceste vulnerabilitati exista. Tot procesul va produce loguri la ambele etape de generare a rapoartelor si la rularea comenzilor de atac (din nou daca este cazul).

## Cerințe de sistem ⚙️

Pentru a rula corect acest proiect, este necesar să fie îndeplinite următoarele condiții:

- **Sistem de operare**: Kali Linux (cu toate uneltele implicite instalate, in special ```nmap```)
- **Limbaj de programare**: Python versiunea **3.13** sau mai recentă
- **Resurse suplimentare obligatorii**:
  - **Exploit-DB** (actualizat)
  - **SecLists** (colecție completă)

> 🛠️ Asigură-te că toate pachetele sunt actualizate și disponibile în sistem înainte de rularea aplicației.
> 🔧 In cazul in care s-a omis vreo unealta Nutcracker poate sa si le instaleze singur  



## 💻 Instalare

### 1. Clonează proiectul
```bash
git clone https://github.com/alex-obada/nutcracker
```
### 2. Creerea unui mediu virtual (<i>optional</i>):

```bash
python -m venv .venv
```
#### Activeaza mediul virtual:

- Pe Linux/macOS
```bash
source .venv/bin/activate
```
- Pe Windows
```cmd
.venv\Scripts\activate
```

### 3. Instalează dependențele
```bash
pip install -r requirements.txt
```
### 4.Configurarea variabilelor de mediu:
Creeaza un fisier ```.env``` în directorul rădăcină și adaugă cheia ta de OpenAI
```ini
OPEN_API_KEY=your_openai_api_key
```

## 🔍 Utilizare


Pentru a efectua o scanare, rulează următoarea comandă:
```bash
nutcracker.py <target> # ip/domain
```
Se vor genera in directorul radacina folderele: 
- **EnumerationOutputs**
- **Reports**


