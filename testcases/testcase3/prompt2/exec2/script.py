import pandas as pd

# Pfad zur Excel-Datei
excel_datei = 'Fallzahlen.xlsx'

# Name des Sheets
sheet_name = 'Fallzahlen_2023'

# Laden der Excel-Datei
try:
    df = pd.read_excel(excel_datei, sheet_name=sheet_name)
except FileNotFoundError:
    print(f"Die Datei '{excel_datei}' wurde nicht gefunden.")
    exit(1)
except Exception as e:
    print(f"Ein Fehler ist aufgetreten: {e}")
    exit(1)

# Sicherstellen, dass die notwendigen Spalten vorhanden sind
erforderliche_spalten = ['Bezirke', 'Straftaten_insgesamt']
for spalte in erforderliche_spalten:
    if spalte not in df.columns:
        print(f"Die Spalte '{spalte}' fehlt in der Excel-Datei.")
        exit(1)

# Extrahieren der Gesamtanzahl von ganz Berlin
gesamt_zeile = df[df['Bezirke'] == 'Berlin (PKS gesamt)']

if gesamt_zeile.empty:
    print("Die Zeile 'Berlin (PKS gesamt)' wurde nicht gefunden.")
    exit(1)

# Annahme: Es gibt genau eine Zeile mit 'Berlin (PKS gesamt)'
gesamt_straftaten = gesamt_zeile['Straftaten_insgesamt'].values[0]

if gesamt_straftaten == 0:
    print("Die Gesamtanzahl der Straftaten für Berlin ist 0. Division durch Null ist nicht möglich.")
    exit(1)

# Filtern der Bezirke (ohne die Gesamtzeile)
bezirke_df = df[df['Bezirke'] != 'Berlin (PKS gesamt)'].copy()

# Berechnung des prozentualen Anteils
bezirke_df['Prozentualer_Anteil (%)'] = (bezirke_df['Straftaten_insgesamt'] / gesamt_straftaten) * 100

# Optional: Runden auf zwei Dezimalstellen
bezirke_df['Prozentualer_Anteil (%)'] = bezirke_df['Prozentualer_Anteil (%)'].round(2)

# Sortieren nach dem prozentualen Anteil absteigend
bezirke_df.sort_values(by='Prozentualer_Anteil (%)', ascending=False, inplace=True)

# Ergebnis anzeigen
print(bezirke_df[['Bezirke', 'Straftaten_insgesamt', 'Prozentualer_Anteil (%)']])

# Optional: Speichern in eine neue Excel-Datei
output_datei = 'Fallzahlen_prozentual.xlsx'
try:
    bezirke_df.to_excel(output_datei, sheet_name='Prozentualer_Anteil', index=False)
    print(f"\nDie Ergebnisse wurden in '{output_datei}' gespeichert.")
except Exception as e:
    print(f"Fehler beim Speichern der Datei: {e}")