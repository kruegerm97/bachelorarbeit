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
Ich habe eine Excel Datei mit dem Namen 'Fallzahlen&HZ 2014-2023.xlsx'. Hier sind die Daten des Sheets zur Orientierung: {df}
Erstelle mir ein Python Skript, das folgende Schritte befolgt:
1. Die Daten des Sheets 'Fallzahlen_2023' auslesen
2. Die Daten in einem Pandas Dataframe speichern
3. Das Dataframe auf die notwendigen Spalten reduzieren: 'Bezeichnung (Bezirksregion)' und 'Raub'
4. Unnötige Zeilen entfernen: Die letzten zwei Zeilen der Tabelle sind Gesamtwerte und sollen entfernt werden.
5. Die Oberbezirke in der Spalte 'Bezeichnung (Bezirksregion)' identifizieren. Die Oberbezirke sind die Zeilen mit folgenden Werten in der Spalte 'Bezeichnung (Bezirksregion)': Mitte, Friedrichshain-Kreuzberg, Pankow, Charlottenburg-Wilmersdorf, Spandau, Steglitz-Zehlendorf, Tempelhof-Schöneberg, Neukölln, Treptow-Köpenick, Marzahn-Hellersdorf, Lichtenberg, Reinickendorf.
6. Für jeden Oberbezirk den Unterbezirk mit dem höchsten Wert in der Spalte 'Raub' identifizieren. Die Unterbezirke sind jeweils die unter den Oberbezirken liegenden Zeilen, bis zum nächsten Oberbezirk.
7. Die Ergebnisse in einem neuen Dataframe speichern, das folgende Spalten enthält: 'Oberbezirk', 'Unterbezirk', 'Raub'
8. Das finale Dataframe ausgeben.
"""

# Anfrage an die OpenAI Chat-API
response = client.chat.completions.create(model="o1-mini", 
messages=[
{"role": "user", "content": prompt}
],)

response_file = path+"testcases/testcase5/prompt3/exec5/response.txt"
os.makedirs(os.path.dirname(response_file), exist_ok=True)
# Ausgabe des generierten Skripts
with open(response_file, "w") as file:
    file.write(response.choices[0].message.content)

print(f"Response wurde in {response_file} gespeichert.")