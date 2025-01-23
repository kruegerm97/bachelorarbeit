from openai import OpenAI

# OpenAI API Key
client = OpenAI(api_key="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")

# 2. CSV-Datei öffnen und Inhalt in Variable speichern
csv_file_path = "/home/mauke/Documents/Uni/bachelorarbeittests/testcases/HZ_2023.csv"
with open(csv_file_path, "r", encoding="utf-8") as file:
    csv_content = file.read()

# 3. Prompt erstellen: CSV-Daten einbetten + Anweisung
prompt = f"""
Hier ist meine CSV-Datei mit dem Namen 'HZ_2023.csv': {csv_content}, bitte analysiere diese Daten und erstelle mir ein Python Skript, das nach der Anzahl der Straftaten insgesamt eines Bezirks in 2023 sortiert.
"""

# 4. Anfrage an die OpenAI Chat-API
response = client.chat.completions.create(model="o1-mini", 
messages=[
    {"role": "user", "content": prompt}
],)

# 5. Ausgabe des generierten Skripts
print(response.choices[0].message.content)
