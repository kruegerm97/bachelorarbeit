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
Ich habe eine Excel Datei mit dem Namen 'Fallzahlen.xlsx'. Erstelle mir ein Python Skript, das folgende Anforderungen erfüllen soll:
1. Die Excel-Datei einlesen und die Sheets als DataFrames speichern.
2. Die DateFrames der einzelnen Sheets zusammen joinen, sodass pro Zeile (jede Zeile ist ein eigener Bezirk) der akkumulierte Wert der einzelnen Straftaten steht.
3. Das neue gejointe DataFrame nach der Spalte "Straftaten_insgesamt" sortieren. Für die Sortierung sollen die Zeilen mit den LOR-Schlüsseln 999900 und 999999 nicht beachtet werden, da es sich hierbei nicht um Bezirke handelt. Sie sollen aber am Ende des DataFrames stehen bleiben.
4. Das sortierte Pandas DataFrame zurückgeben.

Hier ist der Inhalt eines der Sheets als Beispiel: {df}
"""

# Anfrage an die OpenAI Chat-API
response = client.chat.completions.create(model="o1-mini", 
messages=[
{"role": "user", "content": prompt}
],)

response_file = path+"testcases/testcase2/prompt3/exec5/response.txt"
os.makedirs(os.path.dirname(response_file), exist_ok=True)
# Ausgabe des generierten Skripts
with open(response_file, "w") as file:
    file.write(response.choices[0].message.content)

print(f"Response wurde in {response_file} gespeichert.")