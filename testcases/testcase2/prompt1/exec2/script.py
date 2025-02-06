import pandas as pd

# Pfad zur Excel-Datei
excel_datei = 'Fallzahlen.xlsx'

# Einlesen aller Sheets in ein Dictionary von DataFrames
try:
    alle_sheets = pd.read_excel(excel_datei, sheet_name=None)
except FileNotFoundError:
    print(f"Die Datei {excel_datei} wurde nicht gefunden.")
    exit(1)
except Exception as e:
    print(f"Fehler beim Einlesen der Excel-Datei: {e}")
    exit(1)

# Liste zur Speicherung der relevanten Daten aus allen Sheets
daten_liste = []

# Durch alle DataFrames iterieren und relevante Daten extrahieren
for sheet_name, df in alle_sheets.items():
    # Überprüfen, ob die notwendigen Spalten vorhanden sind
    if 'Bezirke' in df.columns and 'Straftaten_insgesamt' in df.columns:
        # Auswahl der relevanten Spalten
        df_relevant = df[['Bezirke', 'Straftaten_insgesamt']]
        daten_liste.append(df_relevant)
    else:
        print(f"Sheet '{sheet_name}' enthält nicht die erforderlichen Spalten.")
        
# Kombinieren aller relevanten Daten
if daten_liste:
    alle_daten = pd.concat(daten_liste)
else:
    print("Keine relevanten Daten gefunden.")
    exit(1)

# Aggregation der Straftaten pro Bezirk
aggregierte_daten = alle_daten.groupby('Bezirke', as_index=False)['Straftaten_insgesamt'].sum()

# Sortieren der Bezirke nach der Anzahl der Straftaten (absteigend)
aggregierte_daten_sortiert = aggregierte_daten.sort_values(by='Straftaten_insgesamt', ascending=False).reset_index(drop=True)

# Optional: Anzeige des resultierenden DataFrames
print(aggregierte_daten_sortiert)

# Optional: Speichern des DataFrames in eine neue Excel-Datei
# aggregierte_daten_sortiert.to_excel('Aggregierte_Fallzahlen.xlsx', index=False)