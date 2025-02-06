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
Ich habe eine Excel Datei mit dem Namen 'Fallzahlen.xlsx'. Erstelle mir ein Python Skript, das die Daten der einzelnen Bezirke (Zeilen) aller Sheets mit einem Join zusammenfügt, sie nach der akkumulierten Spalte "Straftaten_insgesamt" pro Bezirk sortiert und in einem Pandas DataFrame speichert. Die Zeilen mit den LOR-Schlüsseln 999900 und 999999 sollen bei der Sortierung nicht beachtet werden, da es sich hierbei nicht um Bezirke handelt. Hier sind die Daten eines der Sheets als Beispiel: {df}
"""

# Anfrage an die OpenAI Chat-API
response = client.chat.completions.create(model="o1-mini", 
messages=[
{"role": "user", "content": prompt}
],)

response_file = path+"testcases/testcase2/prompt2/exec5/response.txt"
os.makedirs(os.path.dirname(response_file), exist_ok=True)
# Ausgabe des generierten Skripts
with open(response_file, "w") as file:
    file.write(response.choices[0].message.content)

print(f"Response wurde in {response_file} gespeichert.")