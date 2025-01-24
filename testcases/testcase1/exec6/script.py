import pandas as pd

# Pfad zur Excel-Datei
excel_file = 'Fallzahlen&HZ2014-2023.xlsx'

# Lesen des Sheets 'Fallzahlen_2023', Überspringen der ersten 4 Zeilen
df = pd.read_excel(excel_file, sheet_name='Fallzahlen_2023', skiprows=4)

# Umbenennen der Spalten für einfacheren Zugriff (optional)
df.columns = [
    "LOR-Schlüssel", "Bezeichnung", "Straftaten_gesamt", "Raub",
    "Strassenraub_Handtaschenraub", "Koerper_verletzungen_gesamt",
    "Gefaehrliche_schwere_Koerper_verletzung",
    "Freiheitsberaubung_Noetigung_Bedrohung_Nachstellung",
    "Diebstahl_gesamt", "Diebstahl_Kraftwagen",
    "Diebstahl_Kfz", "Fahrraddiebstahl", "Wohnraumeinbruch",
    "Branddelikte_gesamt", "Brandstiftung",
    "Sachbeschadigung_gesamt", "Sachbeschadigung_Graffiti",
    "Rauschgiftdelikte", "Kieztaten"
]

# Entfernen von möglichen Fußzeilen oder nicht relevanten Zeilen
df = df[~df["LOR-Schlüssel"].isin(["", "Gesamt", "Total"])]

# Entfernen von Anführungszeichen und Konvertieren der Zahlen
numeric_cols = [
    "Straftaten_gesamt", "Raub", "Strassenraub_Handtaschenraub",
    "Koerper_verletzungen_gesamt", "Gefaehrliche_schwere_Koerper_verletzung",
    "Freiheitsberaubung_Noetigung_Bedrohung_Nachstellung", "Diebstahl_gesamt",
    "Diebstahl_Kraftwagen", "Diebstahl_Kfz", "Fahrraddiebstahl",
    "Wohnraumeinbruch", "Branddelikte_gesamt", "Brandstiftung",
    "Sachbeschadigung_gesamt", "Sachbeschadigung_Graffiti",
    "Rauschgiftdelikte", "Kieztaten"
]

for col in numeric_cols:
    # Entfernen von Anführungszeichen und Tausendertrennzeichen
    df[col] = df[col].astype(str).str.replace('"', '').str.replace(',', '').str.replace('.', '')
    # Konvertieren zu numerischen Datentypen
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Sortieren nach 'Straftaten_gesamt' in absteigender Reihenfolge
df_sorted = df.sort_values(by='Straftaten_gesamt', ascending=False)

# Optional: Zurücksetzen des Indexes
df_sorted.reset_index(drop=True, inplace=True)

# Ausgabe der sortierten Daten
print(df_sorted[['LOR-Schlüssel', 'Bezeichnung', 'Straftaten_gesamt']])

# Optional: Speichern der sortierten Daten in eine neue Excel-Datei
output_file = 'Fallzahlen_2023_sortiert.xlsx'
df_sorted.to_excel(output_file, sheet_name='Sortiert', index=False)
print(f"Die sortierten Daten wurden in '{output_file}' gespeichert.")