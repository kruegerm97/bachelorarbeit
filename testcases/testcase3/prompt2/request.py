from openai import OpenAI
import os
import pandas as pd

path=os.getenv("THESIS_PATH")

# OpenAI API Key
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Excel-Datei einlesen und als Dataframe speichern
file = path+"/testcases/Fallzahlen.xlsx"
sheet_name = "Fallzahlen_2023"
df = pd.read_excel(file, sheet_name=sheet_name)

# Prompt erstellen: CSV-Daten einbetten + Anweisung
prompt = f"""
Ich habe eine Excel Datei mit dem Namen 'Fallzahlen.xlsx'. Erstelle mir ein Python Skript, welches den prozentualen Anteil der einzelnen Bezirke von ganz Berlin für die Spalte 'Straftaten_insgesamt' berechnet. Jede Zeile der Tabelle ist ein einzelner Bezirk und 'Berlin (PKS gesamt)' ist die Gesamtanzahl von ganz Berlin. Hier ist der Inhalt des Sheets 'Fallzahlen_2023': {df}
"""

# Anfrage an die OpenAI Chat-API
response = client.chat.completions.create(model="o1-mini", 
messages=[
{"role": "user", "content": prompt}
],)

response_file = path+"testcases/testcase3/prompt2/exec5/response.txt"
os.makedirs(os.path.dirname(response_file), exist_ok=True)
# Ausgabe des generierten Skripts
with open(response_file, "w") as file:
    file.write(response.choices[0].message.content)

print(f"Response wurde in {response_file} gespeichert.")