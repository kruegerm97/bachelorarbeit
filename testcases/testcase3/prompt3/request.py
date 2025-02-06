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
Ich habe eine Excel Datei mit dem Namen 'Fallzahlen.xlsx'. Erstelle mir ein Python Skript, welches folgende Anforderungen erfüllt:
1. Die Excel-Datei einlesen
2. Die Tabelle als Pandas DataFrame speichert
3. Überprüfen, ob die notwendigen Spalten 'Bezirke' und 'Straftaten_insgesamt' vorhanden sind
4. Finde die Gesamtzahl der Straftaten für ganz Berlin in der Zeile mit dem Bezirk 'Berlin (PKS gesamt)'
5. Berechne den prozentualen Anteil der einzelnen Bezirke von ganz Berlin für die Spalte 'Straftaten_insgesamt'
6. Das Ergebnis als DataFrame zurückgeben

Hier ist der Inhalt des Sheets 'Fallzahlen_2023': {df}
"""

# Anfrage an die OpenAI Chat-API
response = client.chat.completions.create(model="o1-mini", 
messages=[
{"role": "user", "content": prompt}
],)

response_file = path+"testcases/testcase3/prompt3/exec5/response.txt"
os.makedirs(os.path.dirname(response_file), exist_ok=True)
# Ausgabe des generierten Skripts
with open(response_file, "w") as file:
    file.write(response.choices[0].message.content)

print(f"Response wurde in {response_file} gespeichert.")