import pandas as pd

# Schritt 1: Alle Sheets der Excel-Datei einlesen
excel_datei = 'Fallzahlen.xlsx'
xls = pd.read_excel(excel_datei, sheet_name=None)

# Dictionary zum Speichern der 'Straftaten_insgesamt'-Werte pro Jahr
straftaten_dict = {}

# Schleife durch jedes Sheet
for sheet_name, df in xls.items():
    # Extrahiere das Jahr aus dem Sheet-Namen, z.B. 'Fallzahlen_2014' -> 2014
    try:
        jahr = int(sheet_name.split('_')[-1])
    except ValueError:
        print(f"Sheet '{sheet_name}' entspricht nicht dem erwarteten Muster und wird übersprungen.")
        continue
    
    # Schritt 2: Wert der Spalte 'Straftaten_insgesamt' für 'Berlin (PKS gesamt)' extrahieren
    try:
        wert = df.loc[df['Bezirke'] == 'Berlin (PKS gesamt)', 'Straftaten_insgesamt'].values[0]
        straftaten_dict[jahr] = wert
    except IndexError:
        print(f"'Berlin (PKS gesamt)' wurde in Sheet '{sheet_name}' nicht gefunden.")
        straftaten_dict[jahr] = None

# Umwandlung des Dictionaries in ein sortiertes DataFrame
straftaten_series = pd.Series(straftaten_dict).sort_index()
straftaten_df = straftaten_series.reset_index()
straftaten_df.columns = ['Jahr', 'Straftaten_insgesamt']

# Schritt 3: Prozentuale Veränderung zum Vorjahr berechnen
straftaten_df['Prozentuale_Veraenderung'] = straftaten_df['Straftaten_insgesamt'].pct_change() * 100

# Optional: Prozentuale Veränderung auf zwei Dezimalstellen runden
straftaten_df['Prozentuale_Veraenderung'] = straftaten_df['Prozentuale_Veraenderung'].round(2)

# Schritt 4: Ergebnisse in einem neuen DataFrame speichern
ergebnisse_df = straftaten_df[['Jahr', 'Prozentuale_Veraenderung']]

# Ausgabe der Ergebnisse
print(ergebnisse_df)

# Optional: Ergebnisse in eine neue Excel-Datei speichern
# ergebnisse_df.to_excel('Prozentuale_Veraenderung.xlsx', index=False)