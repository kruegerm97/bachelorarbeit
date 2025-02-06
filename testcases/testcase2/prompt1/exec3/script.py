import pandas as pd

# Pfad zur Excel-Datei
excel_datei = 'Fallzahlen.xlsx'

# Alle Sheet-Namen aus der Excel-Datei auslesen
xls = pd.ExcelFile(excel_datei)
sheet_namen = xls.sheet_names

# Liste zur Speicherung der DataFrames aller Sheets
daten_frames = []

# Iteriere über jedes Sheet und lese die Daten ein
for sheet in sheet_namen:
    df = pd.read_excel(excel_datei, sheet_name=sheet)
    daten_frames.append(df)

# Alle DataFrames zu einem einzigen DataFrame zusammenführen
kombiniert_df = pd.concat(daten_frames, ignore_index=True)

# Optional: Duplikate entfernen, falls Bezirke in mehreren Sheets vorkommen
# kombiniertes_df = kombiniert_df.drop_duplicates(subset=['Bezirke'])

# Gruppieren nach 'Bezirke' und Summieren der 'Straftaten_insgesamt'
aggregiert_df = kombiniert_df.groupby('Bezirke', as_index=False)['Straftaten_insgesamt'].sum()

# Sortieren nach der Anzahl der Straftaten in absteigender Reihenfolge
sortiert_df = aggregiert_df.sort_values(by='Straftaten_insgesamt', ascending=False)

# Optional: Index zurücksetzen
sortiert_df = sortiert_df.reset_index(drop=True)

# Ergebnis anzeigen
print(sortiert_df)

# Optional: Das sortierte Ergebnis in eine neue Excel- oder CSV-Datei speichern
# sortiert_df.to_excel('Aggregierte_Fallzahlen.xlsx', index=False)
# sortiert_df.to_csv('Aggregierte_Fallzahlen.csv', index=False)