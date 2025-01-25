from openai import OpenAI
import os

# OpenAI API Key
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# CSV-Datei öffnen und Inhalt in Variable speichern
csv_file = "FZ_2023.csv"
with open(csv_file, "r", encoding="utf-8") as file:
    csv_content = file.read()

# Prompt erstellen: CSV-Daten einbetten + Anweisung
prompt = f"""
Ich habe eine Excel Datei mit dem Namen 'Fallzahlen&HZ2014-2023.xlsx', mit mehreren Sheets. Hier ist der Inhalt des Sheets 'Fallzahlen_2023': {csv_content}, bitte analysiere die Daten und erstelle mir ein Python Skript, das das Sheet 'Fallzahlen_2023' der Excel Datei nach der Anzahl der Straftaten insgesamt eines Bezirks in 2023 sortiert.
"""

# Anfrage an die OpenAI Chat-API
response = client.chat.completions.create(model="o1-mini", 
messages=[
    {"role": "user", "content": prompt}
],)

# Ausgabe des generierten Skripts
print(response.choices[0].message.content)
