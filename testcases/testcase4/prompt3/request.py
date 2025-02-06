from openai import OpenAI
import os
import pandas as pd

path=os.getenv("THESIS_PATH")

# OpenAI API Key
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Excel-Datei einlesen und als Dataframe speichern
file = path+"/testcases/Fallzahlen.xlsx"
df = pd.read_excel(file, sheet_name='Fallzahlen_2023')

# Prompt erstellen: CSV-Daten einbetten + Anweisung
prompt = f"""
Ich habe eine Excel-Datei mit dem Namen 'Fallzahlen.xlsx'. Diese Datei enthält mehrere Sheets, die nach dem Muster 'Fallzahlen_2014', 'Fallzahlen_2015', usw. benannt sind. Jedes Sheet enthält Daten, darunter eine Spalte namens 'Straftaten_insgesamt'. Erstelle mir ein Python Skript mit den folgenen Schritten:
1. Lese alle Sheets der Excel-Datei ein und speichere jedes Sheet in einem separaten Pandas DataFrame.
2. Extrahiere den Wert der Spalte 'Straftaten_insgesamt' für die Zeile 'Berlin (PKS gesamt)' aus jedem DataFrame.
3. Berechne die prozentuale Veränderung des Werts 'Straftaten_insgesamt' zum jeweiligen Vorjahr.
4. Speichere die Ergebnisse in einem neuen Pandas DataFrame, das die Jahre und die prozentuale Veränderung enthält.
Hier sind die Daten eines der Sheets als Beispiel: {df}
"""

# Anfrage an die OpenAI Chat-API
response = client.chat.completions.create(model="o1-mini", 
messages=[
{"role": "user", "content": prompt}
],)

response_file = path+"testcases/testcase4/prompt3/exec5/response.txt"
os.makedirs(os.path.dirname(response_file), exist_ok=True)
# Ausgabe des generierten Skripts
with open(response_file, "w") as file:
    file.write(response.choices[0].message.content)

print(f"Response wurde in {response_file} gespeichert.")