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
Ich habe eine Excel Datei mit dem Namen 'Fallzahlen.xlsx'. Der Inhalt dieses Sheets ist als pandas DataFrame {df} gegeben. Bitte erstelle mir ein Python-Skript, das die folgenden Schritte ausführt:
1. Lies die Daten des Sheets 'Fallzahlen_2023' der Excel-Datei 'Fallzahlen.xlsx' ein.
2. Sortiere die Daten nach der Spalte 'Straftaten_insgesamt' absteigend. Zur Sortierung sollen die Zeilen mit den LOR-Schlüsseln 999900 und 999999 nicht beachtet werden, da es sich bei diesen nicht um Bezirke handelt. Sie sollen aber am Ende des Dataframes stehen bleiben.
3. Speichere das Ergebnis der Sortierung in einem Pandas Dataframe ab.
Achte darauf, dass das Skript robust ist und potentielle Fehler, wie fehlende Spalten berücksichtigt.
"""

# Anfrage an die OpenAI Chat-API
response = client.chat.completions.create(model="o1-mini", 
messages=[
{"role": "user", "content": prompt}
],)

response_file = path+"testcases/testcase1/prompt3/exec5/response.txt"
os.makedirs(os.path.dirname(response_file), exist_ok=True)
# Ausgabe des generierten Skripts
with open(response_file, "w") as file:
    file.write(response.choices[0].message.content)

print(f"Response wurde in {response_file} gespeichert.")