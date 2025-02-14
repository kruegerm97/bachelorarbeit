from openai import OpenAI
import os
import pandas as pd

path=os.getenv("THESIS_PATH")

# Excel-Datei einlesen und als Dataframe speichern
file = path+"/testcases/Fallzahlen&HZ 2014-2023.xlsx"
df = pd.read_excel(file, sheet_name='Fallzahlen_2023')

# Prompt erstellen: CSV-Daten einbetten + Anweisung
print(df)