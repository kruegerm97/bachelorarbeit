import pandas as pd

# Pfad zur Excel-Datei
excel_file = 'Fallzahlen&HZ2014-2023.xlsx'

# Name des Sheets
sheet_name = 'Fallzahlen_2023'

# Anzahl der Zeilen überspringen (basierend auf den bereitgestellten Daten)
skip_rows = 4  # Anpassung je nach tatsächlichem Aufbau

# Lesen der Excel-Datei
df = pd.read_excel(
    excel_file,
    sheet_name=sheet_name,
    skiprows=skip_rows,
    engine='openpyxl'
)

# Anzeigen der ersten paar Zeilen, um die Struktur zu überprüfen (optional)
#print(df.head())

# Spaltennamen identifizieren und anpassen
# Basierend auf den bereitgestellten Daten könnte die Spalte 'Straftaten insgesamt' anders benannt sein
# Wir gehen davon aus, dass die dritte Spalte die Gesamtzahl der Straftaten enthält
# Falls nötig, passen Sie den Spaltennamen entsprechend an

# Beispiel: Annahme, dass die Spalte 'Straftaten insgesamt' den Namen 'Straftaten insgesamt' hat
# Ansonsten prüfen Sie df.columns und passen Sie den Namen an
# Hier nutze ich den Index der Spalte, falls die Namen nicht exakt passen

# Angenommen, die Spalte mit den Straftaten ist die dritte (Index 2)
# und heißt ähnlich wie "Straftaten insgesamt" in deutscher Sprache

# Festlegen des tatsächlichen Spaltennamens
# Zeigen der Spaltennamen zur Identifizierung (optional)
#print(df.columns)

# Beispielspaltennamen basierend auf den Daten
# Anpassen, falls sie anders benannt sind
# Hier nehme ich an, die Spalte heißt 'Straftaten insgesamt' oder ähnlich
# Eventuell müssen Sie die genaue Bezeichnung aus den Spaltennamen entnehmen

# Finden der Spalte, die "Straftaten insgesamt" entspricht
# Dies kann je nach Excel-Datei variieren
# Hier ein Beispiel, wie man die Spalte identifizieren könnte:

straftaten_spalte = None
for col in df.columns:
    if 'Straftaten' in str(col):
        straffaten_spalte = col
        break

if straffaten_spalte is None:
    raise ValueError("Die Spalte 'Straftaten insgesamt' wurde nicht gefunden.")

# Bereinigen der Straftatenzahlen:
# Entfernen von Anführungszeichen und Kommas, dann Umwandlung in Ganzzahlen
df[straffaten_spalte] = df[straffaten_spalte].astype(str)  # Sicherstellen, dass es ein String ist
df[straffaten_spalte] = df[straffaten_spalte].str.replace('"', '').str.replace(',', '').astype(int)

# Sortieren nach der Straftatenzahl in absteigender Reihenfolge
df_sorted = df.sort_values(by=straffaten_spalte, ascending=False)

# Optional: Zurücksetzen des Indexes
df_sorted.reset_index(drop=True, inplace=True)

# Anzeigen der sortierten Daten
print(df_sorted[['Bezeichnung (Bezirksregion)', straffaten_spalte]])

# Optional: Speichern der sortierten Daten in einer neuen Excel-Datei
output_file = 'Sortierte_Fallzahlen_2023.xlsx'
df_sorted.to_excel(output_file, sheet_name='Sortiert', index=False)
print(f"Die sortierten Daten wurden in '{output_file}' gespeichert.")