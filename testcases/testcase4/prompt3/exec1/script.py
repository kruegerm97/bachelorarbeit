import pandas as pd

# Schritt 1: Alle Sheets der Excel-Datei einlesen
excel_datei = 'Fallzahlen.xlsx'
xls = pd.ExcelFile(excel_datei)

# Dictionary zum Speichern der DataFrames
dataframes = {}

# Extrahiere die Jahreszahlen aus den Sheet-Namen und sortiere sie
sheet_jahre = []
for sheet in xls.sheet_names:
    try:
        # Annahme: Sheetnamen sind im Format 'Fallzahlen_Jahr', z.B. 'Fallzahlen_2014'
        jahr = int(sheet.split('_')[-1])
        sheet_jahre.append((jahr, sheet))
    except ValueError:
        print(f"Sheet '{sheet}' hat kein gültiges Jahresformat und wird übersprungen.")

# Sortiere die Sheets nach Jahr
sheet_jahre.sort()

# Lade die DataFrames und speichere sie im Dictionary
for jahr, sheet in sheet_jahre:
    df = pd.read_excel(xls, sheet_name=sheet)
    dataframes[jahr] = df

# Schritt 2: Extrahiere 'Straftaten_insgesamt' für 'Berlin (PKS gesamt)'
straftaten_gesamt = {}

for jahr, df in dataframes.items():
    # Filtern der Zeile 'Berlin (PKS gesamt)'
    berlin_row = df[df['Bezirke'] == 'Berlin (PKS gesamt)']
    if not berlin_row.empty:
        wert = berlin_row.iloc[0]['Straftaten_insgesamt']
        straftaten_gesamt[jahr] = wert
    else:
        print(f"Die Zeile 'Berlin (PKS gesamt)' wurde im Jahr {jahr} nicht gefunden.")

# Schritt 3: Berechne die prozentuale Veränderung zum Vorjahr
jahre = sorted(straftaten_gesamt.keys())
prozentuale_veraenderung = {}

for i in range(1, len(jahre)):
    aktuelles_jahr = jahre[i]
    vorheriges_jahr = jahre[i-1]
    wert_aktuell = straftaten_gesamt[aktuelles_jahr]
    wert_vorher = straftaten_gesamt[vorheriges_jahr]
    veraenderung = ((wert_aktuell - wert_vorher) / wert_vorher) * 100
    prozentuale_veraenderung[aktuelles_jahr] = veraenderung

# Schritt 4: Ergebnisse in einem neuen DataFrame speichern
ergebnisse = pd.DataFrame({
    'Jahr': list(prozentuale_veraenderung.keys()),
    'Prozentuale Veränderung (%)': list(prozentuale_veraenderung.values())
})

# Optional: Prozentuale Veränderung mit zwei Dezimalstellen formatieren
ergebnisse['Prozentuale Veränderung (%)'] = ergebnisse['Prozentuale Veränderung (%)'].round(2)

# Ergebnisse anzeigen
print(ergebnisse)

# Optional: Ergebnisse in eine neue Excel-Datei speichern
ergebnisse.to_excel('Prozentuale_Veraenderung_Fallzahlen.xlsx', index=False)