import pandas as pd

# Pfad zur Excel-Datei
dateipfad = 'Fallzahlen.xlsx'

# Name des Sheets
sheet_name = 'Fallzahlen_2023'

# Einlesen der Excel-Datei
df = pd.read_excel(dateipfad, sheet_name=sheet_name)

# Anzeigen der ersten Zeilen zur Überprüfung (optional)
#print(df.head())

# Filtere die Bezirke heraus, indem die unerwünschten LOR-Schlüssel ausgeschlossen werden
ausgeschlossene_lor = [999900, 999999]
bezirke_df = df[~df['LOR-Schlüssel'].isin(ausgeschlossene_lor)]

# Sortiere die Bezirke nach 'Straftaten_insgesamt' in absteigender Reihenfolge
bezirke_sortiert = bezirke_df.sort_values(by='Straftaten_insgesamt', ascending=False)

# Optional: Zurücksetzen des Indexes nach dem Sortieren
bezirke_sortiert.reset_index(drop=True, inplace=True)

# Anzeigen des sortierten DataFrames (optional)
print(bezirke_sortiert)

# Wenn Sie den sortierten DataFrame weiter verwenden möchten, steht er als 'bezirke_sortiert' zur Verfügung