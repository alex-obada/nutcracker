```
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
**Nutcracker** este o unealtă open-source ce automatizează munca repetitivă a pentesterilor, bazată pe ```ChatGPT``` și scrisă în Python.

## 📝 Descriere

Nutcracker primește un target (ip/domain) și îi analizează porturile deschise folosind `nmap`. Ca următor pas, tot ce a rezultat din scanare este redirecționat în `gpt-4-turbo`, iar acesta construiește un raport mai detaliat cu ce s-ar putea face pentru a exploata orice vulnerabilități care ar exista pe respectivul calculator. Această operație se realizează de două ori pentru ca AI-ul să-și mărească contextul cu informații de pe surse reputabile, cum ar fi:
  - [HackingArticles](https://www.hackingarticles.in/penetration-testing/)
  - [HackTricks](https://book.hacktricks.wiki/en/index.html)
  - [MITRE ATT&CK](https://attack.mitre.org/)
- [HackingArticles](https://www.hackingarticles.in/penetration-testing/)
- [HackTricks](https://book.hacktricks.wiki/en/index.html)
- [MITRE ATT&CK](https://attack.mitre.org/)

Prin această iterare, AI-ul va genera și comenzi de terminal care vor fi folosite pentru a ataca victima în cazul în care aceste vulnerabilități există. Tot procesul va produce loguri la ambele etape de generare a rapoartelor și la rularea comenzilor de atac (din nou, dacă este cazul).

## Cerințe de sistem ⚙️

Pentru a rula corect acest proiect, este necesar să fie îndeplinite următoarele condiții:

- **Sistem de operare**: Kali Linux (cu toate uneltele implicite instalate, în special ```nmap```)
- **Limbaj de programare**: Python versiunea **3.13** sau mai recentă
- **Resurse suplimentare obligatorii**:
  - **Exploit-DB** (actualizat)
  - **SecLists** (colecție completă)

> 🛠️ Asigură-te că toate pachetele sunt actualizate și disponibile în sistem înainte de rularea aplicației.

> 🔧 În cazul în care s-a omis vreo unealtă, Nutcracker are probabilitatea de 50% să și-o instaleze singur.

## 💻 Instalare

### 1. Clonează proiectul
```bash
git clone https://github.com/alex-obada/nutcracker

```
### 2. Creerea unui mediu virtual (<i>opțional</i>):

```bash
python -m venv .venv
```
#### Activează mediul virtual:

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
Creează un fisier ```.env``` în directorul rădăcină și adaugă cheia ta de OpenAI.
```ini
OPEN_API_KEY=<cheia de OpenAI>
```

## 🔍 Utilizare


Pentru a efectua o scanare, rulează următoarea comandă:
```bash
nutcracker.py <target> # ip/domain
```
Se vor genera în directorul rădăcină folderele:

- **EnumerationOutputs**
- **Reports**
> 🎯 Acolo se vor afla rapoartele și output-urile comenzilor

