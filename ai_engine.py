from openai import OpenAI
import json
from dotenv import load_dotenv
import os
import re

load_dotenv()
api_key = os.getenv("OPEN_API_KEY")

client = OpenAI(api_key=api_key)

def decide_initial_strategy(target, context, learn):
    prompt = f"""
Ținta este: {target}.
Nivelul de adâncime dorit pentru scanare este: top 1000 porturi + vulnerabilități.
Context suplimentar: {context}.

Alege:
- Tool-ul de scanare (ex: nmap, masscan, amass)
- Target-ul (IP sau domeniu)
- Argumentele optime pentru acel tool

Formatul răspunsului trebuie să fie STRICT JSON:
{{
  "tool": "nmap",
  "target": "{target}",
  "arguments": "-sS -T4 -p21,23 -sV --script vuln"{', "explanation": "Explicația alegerii." if learn else ''}
}}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Ești un expert în cybersecurity. Răspunde în format strict JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=800
        )

        content = response.choices[0].message.content
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            json_data = match.group(0)
            strategy = json.loads(json_data)
            if all(k in strategy for k in ("tool", "target", "arguments")):
                return strategy
            else:
                print("[-] JSON-ul nu conține toate cheile necesare.")
                return None
        else:
            print("[-] Nu am găsit JSON valid în răspunsul AI.")
            return None

    except Exception as e:
        print(f"[-] Eroare în decide_initial_strategy: {e}")
        return None