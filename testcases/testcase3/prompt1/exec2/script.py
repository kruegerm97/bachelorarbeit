import pandas as pd

# Pfad zur Excel-Datei
excel_file = 'Fallzahlen.xlsx'

# Name des Sheets
sheet_name = 'Fallzahlen_2023'

# Lesen des Excel-Sheets
df = pd.read_excel(excel_file, sheet_name=sheet_name)

# Annehmen, dass die Gesamtzahl in der Zeile mit 'Berlin (PKS gesamt)' steht
# Suchen der Gesamtzeile
total_row = df[df['Bezirke'] == 'Berlin (PKS gesamt)']

if total_row.empty:
    raise ValueError("Die Gesamtzeile 'Berlin (PKS gesamt)' wurde nicht gefunden.")

# Extrahieren der Gesamtzahl der Straftaten
total_crimes = total_row['Straftaten_insgesamt'].values[0]

# Filtern der Bezirke (ohne Gesamtzeile)
districts_df = df[df['Bezirke'] != 'Berlin (PKS gesamt)'].copy()

# Berechnen des prozentualen Anteils
districts_df['Prozentualer_Anteil (%)'] = (districts_df['Straftaten_insgesamt'] / total_crimes) * 100

# Optional: Runden auf zwei Dezimalstellen
districts_df['Prozentualer_Anteil (%)'] = districts_df['Prozentualer_Anteil (%)'].round(2)

# Anzeigen der Ergebnisse
print(districts_df[['Bezirke', 'Straftaten_insgesamt', 'Prozentualer_Anteil (%)']])

# Optional: Speichern der Ergebnisse in eine neue Excel-Datei
output_file = 'Straftaten_Prozentual_Anteil.xlsx'
districts_df.to_excel(output_file, sheet_name='Prozentuale Anteile', index=False)
print(f"\nDie Ergebnisse wurden in '{output_file}' gespeichert.")