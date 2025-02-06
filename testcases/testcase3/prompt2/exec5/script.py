import pandas as pd

# Pfad zur Excel-Datei und Name des Sheets
excel_datei = 'Fallzahlen.xlsx'
sheet_name = 'Fallzahlen_2023'

# Excel-Datei einlesen
df = pd.read_excel(excel_datei, sheet_name=sheet_name)

# Gesamtanzahl der Straftaten in Berlin extrahieren
# Annahme: Der Eintrag für "Berlin (PKS gesamt)" ist eindeutig
gesamt_strafaten = df.loc[df['Bezirke'] == 'Berlin (PKS gesamt)', 'Straftaten_insgesamt'].values[0]

# Entfernen der Gesamtzeile, um nur die Bezirke zu betrachten
df_bezirke = df[df['Bezirke'] != 'Berlin (PKS gesamt)'].copy()

# Berechnung des prozentualen Anteils der Straftaten für jeden Bezirk
df_bezirke['Prozent_Straftaten'] = (df_bezirke['Straftaten_insgesamt'] / gesamt_strafaten) * 100

# Optional: Sortieren nach dem prozentualen Anteil
df_bezirke.sort_values(by='Prozent_Straftaten', ascending=False, inplace=True)

# Ergebnis anzeigen
print(df_bezirke[['Bezirke', 'Straftaten_insgesamt', 'Prozent_Straftaten']])

# Optional: Ergebnisse in eine neue Excel-Datei speichern
ausgabe_datei = 'Fallzahlen_mit_Prozent.xlsx'
df_bezirke.to_excel(ausgabe_datei, index=False)
print(f"\nDie Ergebnisse wurden in '{ausgabe_datei}' gespeichert.")