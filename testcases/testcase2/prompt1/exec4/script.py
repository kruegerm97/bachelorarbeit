import pandas as pd

# Pfad zur Excel-Datei
excel_file = 'Fallzahlen.xlsx'

# Schritt 1: Alle Sheets der Excel-Datei einlesen
# Das Argument sheet_name=None liest alle Sheets und gibt ein Dictionary zurück
all_sheets = pd.read_excel(excel_file, sheet_name=None)

# Schritt 2: Daten aus allen Sheets zusammenführen
# Wir gehen davon aus, dass alle Sheets die gleiche Struktur haben
# Daher können wir sie einfach mit pd.concat zusammenfügen
combined_df = pd.concat(all_sheets.values(), ignore_index=True)

# Schritt 3: Daten nach 'Bezirke' gruppieren und 'Straftaten_insgesamt' summieren
# Dies aggregiert die Straftaten pro Bezirk über alle Sheets hinweg
grouped_df = combined_df.groupby('Bezirke')['Straftaten_insgesamt'].sum().reset_index()

# Schritt 4: Die aggregierten Daten nach 'Straftaten_insgesamt' sortieren (absteigend)
sorted_df = grouped_df.sort_values(by='Straftaten_insgesamt', ascending=False).reset_index(drop=True)

# Optional: Anzeigen des sortierten DataFrames
print(sorted_df)

# Optional: Den sortierten DataFrame in eine neue Excel-Datei speichern
sorted_df.to_excel('Aggregierte_Straftaten_pro_Bezirk.xlsx', index=False)