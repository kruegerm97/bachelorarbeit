from openai import OpenAI
import os

# OpenAI API Key
api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
# CSV-Dateien öffnen und Inhalte in Variablen speichern
jahre = range(2014, 2024)  # Von 2014 bis 2023
csv_contents = []

for jahr in jahre:
    dateiname = f"FZ_{jahr}.csv"
    with open(dateiname, "r", encoding="utf-8") as file:
        csv_contents.append(file.read())  # Füge den Inhalt der Datei zur Liste hinzu

# Prompt erstellen: CSV-Daten einbetten + Anweisung
prompt = f"""
Ich habe eine Execl Datei mit dem Namen "Fallzahlen&HZ2014-2023.xlsx", hier sind die Inhalte von den Sheets Fallzahlen_2014 bis Fallzaheln_2023, jedes Jahr hat ein eigenes Sheet mit der gleichen Namenskonvention: {csv_contents}. Die anderen Sheets, die nicht dieser Konvention folgen, sollen ignoriert werden. Erstelle mir ein Python Skript, mit welchem die Tabellen der relevanten Sheets der Excel Datei durch einen Join zusammengeführt werden und der Bezirk mit den meisten Straftaten von allen Jahren kombiniert zurückgegeben wird.
"""

# Anfrage an die OpenAI Chat-API
response = client.chat.completions.create(model="o1-mini", 
messages=[
    {"role": "user", "content": prompt}
],)

# Ausgabe des generierten Skripts
print(response.choices[0].message.content)