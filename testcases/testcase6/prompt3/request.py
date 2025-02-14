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
Ich habe eine Excel-Datei mit dem Namen 'Fallzahlen&HZ 2014-2023.xlsx'. Diese Datei enthält unter anderem die Sheets 'Fallzahlen_2014' bis 'Fallzahlen_2023'. 
Erstelle ein Python-Skript, das die folgenden Schritte ausführt:
1. Lese alle Sheets der Excel-Datei ein und speichere jedes Sheet in einem separaten Pandas DataFrame.
2. Füge alle DataFrames zu einem einzigen zusammen, sodass ein einheitlicher DataFrame entsteht, der alle Jahre umfasst.
3. Identifiziere die Oberbezirke anhand der folgenden Werte in der Spalte 'Bezeichnung (Bezirksregion)': 
   Mitte, Friedrichshain-Kreuzberg, Pankow, Charlottenburg-Wilmersdorf, Spandau, Steglitz-Zehlendorf, Tempelhof-Schöneberg, Neukölln, Treptow-Köpenick, Marzahn-Hellersdorf, Lichtenberg, Reinickendorf.
4. Entferne alle Zeilen, die Oberbezirke, Berlin (PKS gesamt) oder Stadt Berlin nicht zuzuordnende Einträge enthalten, sodass nur Unterbezirke übrig bleiben.
5. Summiere für jeden Unterbezirk die Werte der Spalte 'Straftaten \n-insgesamt-' über alle Jahre hinweg auf.
6. Sortiere die Unterbezirke absteigend nach der aggregierten Anzahl an Straftaten.
7. Wähle die 10 Unterbezirke mit den höchsten Gesamtstraftaten aus.
8. Erstelle einen neuen DataFrame, der nur die Spalten 'Bezeichnung (Bezirksregion)' (Unterbezirke) und die aggregierte Anzahl der Spalte 'Straftaten \n-insgesamt-' enthält.
9. Gib den finalen DataFrame aus.

Achte bei der Umsetzung genau auf die genannten Schritte, Spaltennamen und Sheetnamen.
Hier sind die Daten des Sheets 'Fallzahlen_2023' zur Orientierung:
{df}
"""

# Anfrage an die OpenAI Chat-API
response = client.chat.completions.create(model="o1-mini", 
messages=[
{"role": "user", "content": prompt}
],)

response_file = path+"testcases/testcase6/prompt3/exec5/response.txt"
os.makedirs(os.path.dirname(response_file), exist_ok=True)
# Ausgabe des generierten Skripts
with open(response_file, "w") as file:
    file.write(response.choices[0].message.content)

print(f"Response wurde in {response_file} gespeichert.")