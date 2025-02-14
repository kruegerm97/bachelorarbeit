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

# Prompt
prompt = f"""
Ich habe eine Excel-Datei mit dem Namen 'Fallzahlen&HZ 2014-2023.xlsx', die die Sheets Fallzahlen_2014 bis Fallzahlen_2023 enthält. Erstelle ein Python-Skript, das diese Daten ausliest und in einem einheitlichen Pandas DataFrame zusammenführt.
Anschließend sollen nur die Unterbezirke berücksichtigt und alle Oberbezirke sowie nicht zugeordneten Zeilen entfernt werden. Die Oberbezirke lassen sich anhand folgender Werte in der Spalte 'Bezeichnung (Bezirksregion)' identifizieren: Mitte, Friedrichshain-Kreuzberg, Pankow, Charlottenburg-Wilmersdorf, Spandau, Steglitz-Zehlendorf, Tempelhof-Schöneberg, Neukölln, Treptow-Köpenick, Marzahn-Hellersdorf, Lichtenberg, Reinickendorf.
Für die verbleibenden Unterbezirke soll die Gesamtanzahl der Spalte 'Straftaten \n-insgesamt-' über alle Jahre hinweg aufsummiert und anschließend die Top 10 Unterbezirke mit den meisten Straftaten ermittelt werden. Der finale DataFrame soll nur die Spalten 'Bezeichnung (Bezirksregion)' (Unterbezirke) und die aggregierte Anzahl der Spalte 'Straftaten \n-insgesamt-' enthalten.
Hier sind die Daten des Sheets Fallzahlen_2023 zur Orientierung: {df}
"""

# Anfrage an die OpenAI Chat-API
response = client.chat.completions.create(model="o1-mini", 
messages=[
{"role": "user", "content": prompt}
],)

response_file = path+"testcases/testcase6/prompt2/exec5/response.txt"
os.makedirs(os.path.dirname(response_file), exist_ok=True)
# Ausgabe des generierten Skripts
with open(response_file, "w") as file:
    file.write(response.choices[0].message.content)

print(f"Response wurde in {response_file} gespeichert.")