import pandas as pd

# Pfad zur Excel-Datei
excel_datei = 'Fallzahlen.xlsx'

# Name des Sheets
sheet_name = 'Fallzahlen_2023'

# Lesen der Excel-Datei
df = pd.read_excel(excel_datei, sheet_name=sheet_name)

# Überprüfen, ob die notwendigen Spalten vorhanden sind
notwendige_spalten = ['Bezirke', 'Straftaten_insgesamt']
for spalte in notwendige_spalten:
    if spalte not in df.columns:
        raise ValueError(f"Die Spalte '{spalte}' fehlt in der Excel-Datei.")

# Extrahieren der Gesamtanzahl von ganz Berlin
gesamt_row = df[df['Bezirke'] == 'Berlin (PKS gesamt)']

if gesamt_row.empty:
    raise ValueError("Die Gesamtzeile 'Berlin (PKS gesamt)' wurde nicht gefunden.")

gesamt_straftaten = gesamt_row['Straftaten_insgesamt'].values[0]

# Entfernen der Gesamtzeile aus dem DataFrame
bezirk_df = df[df['Bezirke'] != 'Berlin (PKS gesamt)'].copy()

# Berechnung des prozentualen Anteils
bezirk_df['Prozent_Straftaten_insgesamt'] = (bezirk_df['Straftaten_insgesamt'] / gesamt_straftaten) * 100

# Optional: Runde die Prozentwerte auf zwei Dezimalstellen
bezirk_df['Prozent_Straftaten_insgesamt'] = bezirk_df['Prozent_Straftaten_insgesamt'].round(2)

# Ausgabe des Ergebnisses
print(bezirk_df[['Bezirke', 'Straftaten_insgesamt', 'Prozent_Straftaten_insgesamt']])

# Optional: Speichern in einer neuen Excel-Datei
ausgabe_datei = 'Fallzahlen_mit_Prozentsatz.xlsx'
bezirk_df.to_excel(ausgabe_datei, index=False)
print(f"\nDie Ergebnisse wurden in '{ausgabe_datei}' gespeichert.")