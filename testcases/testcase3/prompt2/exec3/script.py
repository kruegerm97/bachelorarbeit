import pandas as pd

# Pfad zur Excel-Datei
excel_datei = 'Fallzahlen.xlsx'

# Name des Sheets
sheet_name = 'Fallzahlen_2023'

# Lesen des Excel-Sheets
try:
    df = pd.read_excel(excel_datei, sheet_name=sheet_name)
except FileNotFoundError:
    print(f"Die Datei '{excel_datei}' wurde nicht gefunden.")
    exit(1)
except Exception as e:
    print(f"Ein Fehler ist aufgetreten beim Lesen der Excel-Datei: {e}")
    exit(1)

# Überprüfen, ob die notwendigen Spalten vorhanden sind
if 'Bezirke' not in df.columns or 'Straftaten_insgesamt' not in df.columns:
    print("Die erforderlichen Spalten 'Bezirke' oder 'Straftaten_insgesamt' fehlen in der Tabelle.")
    exit(1)

# Finden des Gesamtwerts für Berlin
gesamt_zeile = df[df['Bezirke'] == 'Berlin (PKS gesamt)']

if gesamt_zeile.empty:
    print("Die Gesamtzeile 'Berlin (PKS gesamt)' wurde nicht gefunden.")
    exit(1)

gesamt_straftaten = gesamt_zeile['Straftaten_insgesamt'].values[0]

# Entfernen der Gesamtzeile aus den Bezirken
bezirke_df = df[df['Bezirke'] != 'Berlin (PKS gesamt)'].copy()

# Berechnen des prozentualen Anteils
bezirke_df['Prozentualer_Anteil'] = (bezirke_df['Straftaten_insgesamt'] / gesamt_straftaten) * 100

# Optional: Runden auf zwei Dezimalstellen
bezirke_df['Prozentualer_Anteil'] = bezirke_df['Prozentualer_Anteil'].round(2)

# Anzeigen der Ergebnisse
print(bezirke_df[['Bezirke', 'Straftaten_insgesamt', 'Prozentualer_Anteil']])

# Speichern der Ergebnisse in einer neuen Excel-Datei
ausgabe_datei = 'Fallzahlen_Prozente.xlsx'
try:
    bezirke_df.to_excel(ausgabe_datei, sheet_name='Prozentuale_Fallzahlen', index=False)
    print(f"\nDie prozentualen Anteile wurden in '{ausgabe_datei}' gespeichert.")
except Exception as e:
    print(f"Ein Fehler ist aufgetreten beim Speichern der Excel-Datei: {e}")