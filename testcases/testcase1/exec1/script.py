import pandas as pd

# Dateiname und Sheetname definieren
excel_file = 'Fallzahlen&HZ2014-2023.xlsx'
sheet_name = 'Fallzahlen_2023'

# Anzahl der zu überspringenden Zeilen vor den Daten (hier die ersten 4 Zeilen)
skip_rows = 4

# Lese das Excel-Sheet
df = pd.read_excel(
    excel_file,
    sheet_name=sheet_name,
    skiprows=skip_rows,  # Überspringe die ersten 4 Zeilen
    dtype=str  # Lese alle Daten als Strings, um die Formatierung zu kontrollieren
)

# Optional: Anzeigen der ersten Zeilen, um die Struktur zu prüfen
# print(df.head())

# Benenne die Spalten um, falls notwendig (abhängig von der tatsächlichen Header-Zeile)
# Hier nehme ich an, dass die Spalte "Straftaten -insgesamt-" genau so heißt
# Falls es Leerzeichen oder andere Zeichen gibt, passe den Namen entsprechend an

# Überprüfe die exakten Spaltennamen
print("Spaltennamen:", df.columns.tolist())

# Angenommen, die richtige Spalte heißt "Straftaten \n -insgesamt-"
# Passen wir den Namen an, falls er Zeilenumbrüche oder zusätzliche Leerzeichen enthält
df.columns = [col.strip().replace('\n', ' ') for col in df.columns]

# Identifiziere die genaue Spalte für "Straftaten insgesamt"
strftaten_col = None
for col in df.columns:
    if 'Straftaten' in col and 'insgesamt' in col:
        strftaten_col = col
        break

if not strftaten_col:
    raise ValueError("Die Spalte für 'Straftaten insgesamt' wurde nicht gefunden.")

print(f"Verwende die Spalte: '{strftaten_col}' für die Sortierung.")

# Entferne Tausendertrennzeichen und konvertiere die Spalte in numerische Werte
# Ersetze eventuelle nicht-numerische Einträge mit NaN
df['Straftaten_gesamt_numeric'] = pd.to_numeric(
    df[strftaten_col].str.replace(',', '').str.strip(),
    errors='coerce'
)

# Überprüfe, ob es fehlgeschlagene Konvertierungen gibt
if df['Straftaten_gesamt_numeric'].isnull().any():
    print("Warnung: Einige Einträge konnten nicht konvertiert werden und werden als NaN behandelt.")

# Sortiere das DataFrame nach der neuen numerischen Spalte in absteigender Reihenfolge
sorted_df = df.sort_values(by='Straftaten_gesamt_numeric', ascending=False)

# Optional: Entferne Einträge, die nicht zu einem Bezirk gehören (z.B. "nicht zuzuordnen")
# Angenommen, Bezirke haben einen LOR-Schlüssel, der nicht mit "99" oder "0" beginnt
# Passe dies nach Bedarf an

# Zum Beispiel:
# sorted_df = sorted_df[~sorted_df['LOR-Schlüssel (Bezirksregion)'].str.startswith(('99', '0'))]

# Zeige die sortierten Daten an
print(sorted_df[['LOR-Schlüssel (Bezirksregion)', 'Bezeichnung (Bezirksregion)', 'Straftaten_gesamt_numeric']])

# Optional: Speichere die sortierten Daten in eine neue Excel-Datei
sorted_df.to_excel('Fallzahlen_2023_sortiert.xlsx', index=False)