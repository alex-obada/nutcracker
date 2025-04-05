# ai_engine.py

import openai
import json
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def decide_initial_command(target, context, learn):
    # Construim prompt-ul pe baza inputului de la user
    prompt = f"""
Ținta este: {target}.
Nivelul de adâncime dorit pentru scanare este: sa scanam cele top 1000 de porturi plus vulnerabilități.
Context suplimentar oferit de utilizator: {context}.

Te rog să alegi:
- Tool-ul de scanare potrivit (ex: nmap, masscan, amass, etc.)
- Argumentele optime pentru acel tool

Dacă contextul menționează servicii sau protocoale (ex: Telnet, FTP, SMB, HTTP), prioritizează acele porturi.

Răspunde STRICT în format JSON astfel:
{{
  "tool": "nmap",
  "arguments": "-sS -T4 -p21,23 -sV --script vuln"
  {" ,\"explanation\": \"Explică pe scurt de ce ai ales tool-ul și argumentele.\" " if learn else ""}
}}

Dacă utilizatorul a cerut explicații (--learn), adaugă cheia \"explanation\".
"""
    try:
        # Trimitem cererea la OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Ești un expert în cybersecurity. Răspunde clar și strict conform instrucțiunilor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,  # stabil pentru răspunsuri consistente
            max_tokens=800
        )

        content = response['choices'][0]['message']['content']

        # Încercăm să parsăm răspunsul ca JSON
        strategy = json.loads(content)
        return strategy

    except json.JSONDecodeError:
        print("[-] Eroare: Răspunsul AI nu a fost în format JSON valid.")
        return None
    except Exception as e:
        print(f"[-] Eroare la comunicarea cu OpenAI: {str(e)}")
        return None
