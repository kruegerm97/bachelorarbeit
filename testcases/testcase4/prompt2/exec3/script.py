import pandas as pd

# Pfad zur Excel-Datei
excel_file = 'Fallzahlen.xlsx'

# Lese alle Sheetnamen aus der Excel-Datei
xls = pd.ExcelFile(excel_file)
sheet_names = xls.sheet_names

# Initialisiere ein Dictionary, um die Daten zu speichern
data = {}

# Iteriere durch alle Sheets
for sheet in sheet_names:
    try:
        # Extrahiere das Jahr aus dem Sheetnamen, z.B. 'Fallzahlen_2014' -> 2014
        year = int(sheet.split('_')[-1])
    except ValueError:
        print(f"Sheet '{sheet}' folgt nicht dem erwarteten Namensformat. Überspringe...")
        continue

    # Lese das aktuelle Sheet
    df = pd.read_excel(xls, sheet_name=sheet)

    # Filtere die Zeile für 'Berlin (PKS gesamt)'
    berlin_data = df[df['Bezirke'] == 'Berlin (PKS gesamt)']

    if berlin_data.empty:
        print(f"Keine Daten für 'Berlin (PKS gesamt)' im Sheet '{sheet}' gefunden.")
        continue

    # Extrahiere den Wert der Spalte 'Straftaten_insgesamt'
    total_crimes = berlin_data['Straftaten_insgesamt'].values[0]

    # Speichere die Daten im Dictionary
    data[year] = total_crimes

# Erstelle einen DataFrame aus dem Dictionary
df_crimes = pd.DataFrame(list(data.items()), columns=['Jahr', 'Straftaten_insgesamt'])

# Sortiere den DataFrame nach Jahr
df_crimes = df_crimes.sort_values('Jahr').reset_index(drop=True)

# Berechne die prozentuale Veränderung zum Vorjahr
df_crimes['Prozentuale_Veränderung (%)'] = df_crimes['Straftaten_insgesamt'].pct_change() * 100

# Optional: Runde die prozentuale Veränderung auf zwei Dezimalstellen
df_crimes['Prozentuale_Veränderung (%)'] = df_crimes['Prozentuale_Veränderung (%)'].round(2)

# Zeige den Ergebnis-DataFrame
print(df_crimes)

# Optional: Speichere den DataFrame in eine neue Excel-Datei
df_crimes.to_excel('Straftaten_Veränderung_Zeitreihe.xlsx', index=False)