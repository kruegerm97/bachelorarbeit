from openai import OpenAI

# OpenAI API Key
client = OpenAI(api_key="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")

# CSV-Datei öffnen und Inhalt in Variable speichern
csv_file = "FZ_2023.csv"
with open(csv_file, "r", encoding="utf-8") as file:
    csv_content = file.read()

# Prompt erstellen: CSV-Daten einbetten + Anweisung
prompt = f"""
Ich habe eine Excel Datei mit dem Namen 'Fallzahlen&HZ2014-2023', mit mehreren Sheets. Hier ist der Inhalt des Sheets 'FZ_2023.csv': {csv_content}, bitte analysiere diese Daten und erstelle mir ein Python Skript, das nach der Anzahl der Straftaten insgesamt eines Bezirks in 2023 sortiert.
"""

# Anfrage an die OpenAI Chat-API
response = client.chat.completions.create(model="o1-mini", 
messages=[
    {"role": "user", "content": prompt}
],)

# Ausgabe des generierten Skripts
print(response.choices[0].message.content)
