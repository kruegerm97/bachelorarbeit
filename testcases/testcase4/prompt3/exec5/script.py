import pandas as pd

# 1. Lesen Sie alle Sheets der Excel-Datei ein
excel_file = 'Fallzahlen.xlsx'
all_sheets = pd.read_excel(excel_file, sheet_name=None)

# Liste zur Speicherung der Ergebnisse
daten_liste = []

# 2. Extrahieren Sie den Wert der Spalte 'Straftaten_insgesamt' für 'Berlin (PKS gesamt)'
for sheet_name, df in all_sheets.items():
    # Extrahieren Sie das Jahr aus dem Sheet-Namen, z.B. 'Fallzahlen_2014' -> 2014
    try:
        jahr = int(sheet_name.split('_')[-1])
    except ValueError:
        print(f"Das Sheet '{sheet_name}' hat keinen gültigen Jahresnamen und wird übersprungen.")
        continue
    
    # Suche nach der Zeile 'Berlin (PKS gesamt)'
    berlin_data = df[df['Bezirke'] == 'Berlin (PKS gesamt)']
    
    if berlin_data.empty:
        print(f"'Berlin (PKS gesamt)' wurde im Sheet '{sheet_name}' nicht gefunden.")
        continue
    
    # Extrahiere den Wert der Spalte 'Straftaten_insgesamt'
    strftaten_insgesamt = berlin_data['Straftaten_insgesamt'].values[0]
    
    daten_liste.append({'Jahr': jahr, 'Straftaten_insgesamt': strftaten_insgesamt})

# 3. Erstellen Sie ein DataFrame aus den gesammelten Daten
daten_df = pd.DataFrame(daten_liste)

# Sortieren Sie das DataFrame nach Jahr aufsteigend
daten_df = daten_df.sort_values('Jahr').reset_index(drop=True)

# 4. Berechnen Sie die prozentuale Veränderung zum Vorjahr
daten_df['Prozentuale_Veraenderung'] = daten_df['Straftaten_insgesamt'].pct_change() * 100

# Optional: Runden Sie die Prozentsätze auf zwei Dezimalstellen
daten_df['Prozentuale_Veraenderung'] = daten_df['Prozentuale_Veraenderung'].round(2)

# 5. Erstellen Sie das Endergebnis DataFrame
ergebnis_df = daten_df[['Jahr', 'Prozentuale_Veraenderung']]

# Optional: Benennen Sie die Spalten auf Deutsch um
ergebnis_df.columns = ['Jahr', 'Prozentuale Veränderung (%)']

# 6. Anzeigen des Ergebnisses
print(ergebnis_df)

# 7. Speichern Sie das Ergebnis in einer neuen Excel-Datei (optional)
ergebnis_df.to_excel('Prozentuale_Veraenderung_Fallzahlen.xlsx', index=False)