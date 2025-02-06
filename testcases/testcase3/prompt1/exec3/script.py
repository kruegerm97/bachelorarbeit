import pandas as pd

# Pfad zur Excel-Datei
excel_datei = 'Fallzahlen.xlsx'

# Name des Sheets
sheet_name = 'Fallzahlen_2023'

# Lesen der Excel-Datei
try:
    df = pd.read_excel(excel_datei, sheet_name=sheet_name)
except FileNotFoundError:
    print(f"Die Datei '{excel_datei}' wurde nicht gefunden.")
    exit(1)
except Exception as e:
    print(f"Fehler beim Lesen der Excel-Datei: {e}")
    exit(1)

# Anzeigen der geladenen Daten (optional)
#print(df.head())

# Herausfinden der Gesamtstraftaten in Berlin
# Annahme: Die Gesamtstraftaten stehen in der Zeile mit 'Berlin (PKS gesamt)'
gesamt_row = df[df['Bezirke'] == 'Berlin (PKS gesamt)']

if gesamt_row.empty:
    print("Die Zeile 'Berlin (PKS gesamt)' wurde nicht gefunden.")
    exit(1)

gesamt_straftaten = gesamt_row['Straftaten_insgesamt'].values[0]

# Filtern der Bezirke (Ausschluss von Gesamtzeilen)
bezirke_df = df[~df['Bezirke'].isin(['Berlin (PKS gesamt)', 'Stadtgebiet Berlin, nicht zuzuordnen'])]

# Berechnung des prozentualen Anteils
bezirke_df = bezirke_df.copy()  # Vermeidung von SettingWithCopyWarning
bezirke_df['Prozentualer_Anteil (%)'] = (bezirke_df['Straftaten_insgesamt'] / gesamt_straftaten) * 100

# Optional: Runden auf zwei Dezimalstellen
bezirke_df['Prozentualer_Anteil (%)'] = bezirke_df['Prozentualer_Anteil (%)'].round(2)

# Sortieren nach Prozentualem Anteil absteigend (optional)
bezirke_df = bezirke_df.sort_values(by='Prozentualer_Anteil (%)', ascending=False)

# Ergebnis anzeigen
ergebnis = bezirke_df[['Bezirke', 'Straftaten_insgesamt', 'Prozentualer_Anteil (%)']]
print(ergebnis)

# Optional: Ergebnis in eine neue Excel-Datei speichern
# ergebnis.to_excel('Prozentuale_Anteile_Straftaten.xlsx', index=False)