import pandas as pd

# Pfad zur Excel-Datei
excel_file = 'Fallzahlen.xlsx'

# Lade alle Sheet-Namen
xls = pd.ExcelFile(excel_file)
sheets = xls.sheet_names

# Extrahiere das Jahr aus den Sheet-Namen und sortiere die Sheets nach Jahr
sheet_years = []
for sheet in sheets:
    try:
        # Erwartetes Format: 'Fallzahlen_2014', 'Fallzahlen_2015', etc.
        year = int(sheet.split('_')[-1])
        sheet_years.append((year, sheet))
    except ValueError:
        print(f"Sheet-Name '{sheet}' enthält kein gültiges Jahr und wird übersprungen.")
        continue

# Sortiere die Sheets nach Jahr
sheet_years_sorted = sorted(sheet_years, key=lambda x: x[0])

# Liste zur Speicherung der Ergebnisse
data = []

# Iteriere über jedes Sheet und extrahiere die benötigten Daten
for year, sheet in sheet_years_sorted:
    # Lese das aktuelle Sheet
    df = pd.read_excel(excel_file, sheet_name=sheet)
    
    # Stelle sicher, dass die benötigten Spalten vorhanden sind
    if 'Bezirke' not in df.columns or 'Straftaten_insgesamt' not in df.columns:
        print(f"Sheet '{sheet}' fehlt die erforderliche Spalte. Überspringe dieses Sheet.")
        continue
    
    # Filtere die Zeile für "Berlin (PKS gesamt)"
    row = df[df['Bezirke'] == "Berlin (PKS gesamt)"]
    
    if not row.empty:
        # Extrahiere den Wert und stelle sicher, dass er numerisch ist
        value = row['Straftaten_insgesamt'].values[0]
        if pd.notnull(value):
            data.append({'Year': year, 'Straftaten_insgesamt': value})
        else:
            print(f"Der Wert für 'Straftaten_insgesamt' im Jahr {year} ist NaN.")
    else:
        print(f"'Berlin (PKS gesamt)' nicht in Sheet '{sheet}' gefunden.")

# Erstelle ein DataFrame aus den gesammelten Daten
df_data = pd.DataFrame(data)

# Sortiere das DataFrame nach Jahr, um sicherzustellen, dass die Reihenfolge stimmt
df_data = df_data.sort_values('Year').reset_index(drop=True)

# Berechne die prozentuale Veränderung zum Vorjahr
df_data['Prozentuale_Veraenderung'] = df_data['Straftaten_insgesamt'].pct_change() * 100

# Optional: Runde die Prozentwerte auf zwei Dezimalstellen
df_data['Prozentuale_Veraenderung'] = df_data['Prozentuale_Veraenderung'].round(2)

# Anzeige des Ergebnisses
print(df_data)

# Optional: Speichere das Ergebnis in eine neue Excel-Datei oder CSV
# df_data.to_excel('Prozentuale_Veraenderung_Fallzahlen.xlsx', index=False)
# df_data.to_csv('Prozentuale_Veraenderung_Fallzahlen.csv', index=False)