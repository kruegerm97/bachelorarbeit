import pandas as pd

# Pfad zur Excel-Datei und Name des Sheets
excel_datei = 'Fallzahlen.xlsx'
blatt_name = 'Fallzahlen_2023'

# Lade die Daten aus der Excel-Datei
df = pd.read_excel(excel_datei, sheet_name=blatt_name)

# Finde die Gesamtzahl der Straftaten für ganz Berlin
berlin_gesamtreihe = df[df['Bezirke'] == 'Berlin (PKS gesamt)']
if berlin_gesamtreihe.empty:
    raise ValueError("Die Zeile 'Berlin (PKS gesamt)' wurde in den Daten nicht gefunden.")

berlin_gesamt = berlin_gesamtreihe['Straftaten_insgesamt'].iloc[0]

# Entferne die Gesamtzeile aus dem DataFrame
bezirke_df = df[df['Bezirke'] != 'Berlin (PKS gesamt)'].copy()

# Berechne den prozentualen Anteil der Straftaten für jeden Bezirk
bezirke_df['Prozentualer_Anteil'] = ((bezirke_df['Straftaten_insgesamt'] / berlin_gesamt) * 100).round(2)

# Ausgabe der Ergebnisse
print(bezirke_df[['Bezirke', 'Straftaten_insgesamt', 'Prozentualer_Anteil']])

# Speichere das Ergebnis in eine neue Excel-Datei
bezirke_df.to_excel('Fallzahlen_mit_Prozentanteilen.xlsx', index=False)