from openai import OpenAI
import os
import pandas as pd

path=os.getenv("THESIS_PATH")

# OpenAI API Key
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Excel-Datei einlesen und als Dataframe speichern
file = path+"/testcases/Fallzahlen&HZ 2014-2023.xlsx"
df = pd.read_excel(file, sheet_name='Fallzahlen_2023')

# Prompt erstellen: CSV-Daten einbetten + Anweisung
prompt = f"""
Ich habe eine Excel Datei mit dem Namen 'Fallzahlen&HZ 2014-2023.xlsx'. Erstelle mir ein Python Skript, das die Daten des Sheets 'Fallzahlen_2023' ausliest und für jeden Oberbezirk den Unterbezirk mit den meisten Raubdelikten (Spaltenname:Raub) ausgibt.
Hier sind die Daten des Sheets zur Orientierung: {df}
Die Oberbezirke sind die Zeilen mit folgendem in der Spalte 'Bezeichnung (Bezirksregion)': Mitte, Friedrichshain-Kreuzberg, Pankow, Charlottenburg-Wilmersdorf, Spandau, Steglitz-Zehlendorf, Tempelhof-Schöneberg, Neukölln, Treptow-Köpenick, Marzahn-Hellersdorf, Lichtenberg, Reinickendorf. Die Unterbezirke sind jeweils die darunterliegenden Zeilen, bis zum nächsten Oberbezirk. Die letzten zwei Zeilen der Tabelle sind Gesamtwerte und sollen ignoriert werden.
"""

# Anfrage an die OpenAI Chat-API
response = client.chat.completions.create(model="o1-mini", 
messages=[
{"role": "user", "content": prompt}
],)

response_file = path+"testcases/testcase5/prompt2/exec5/response.txt"
os.makedirs(os.path.dirname(response_file), exist_ok=True)
# Ausgabe des generierten Skripts
with open(response_file, "w") as file:
    file.write(response.choices[0].message.content)

print(f"Response wurde in {response_file} gespeichert.")