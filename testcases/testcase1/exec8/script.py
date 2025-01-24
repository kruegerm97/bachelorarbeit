import pandas as pd

# Pfad zur Excel-Datei
excel_datei = 'Fallzahlen&HZ2014-2023.xlsx'

# Namen des Sheets
sheet_name = 'Fallzahlen_2023'

# Überspringe die ersten 4 Zeilen, die Metadaten enthalten
# Annahme: Die Header befinden sich in der 5. Zeile (Index 4)
df = pd.read_excel(
    excel_datei,
    sheet_name=sheet_name,
    skiprows=4,
    thousands=',',    # Komma als Tausender-Trennzeichen
    decimal='.',      # Punkt als Dezimaltrennzeichen (falls vorhanden)
    engine='openpyxl' # Sicherstellen, dass openpyxl verwendet wird
)

# Anzeigen der ersten paar Zeilen, um sicherzustellen, dass die Daten korrekt geladen wurden
print("Erste Zeilen des geladenen DataFrames:")
print(df.head())

# Überprüfen der Spaltennamen
print("\nSpaltennamen:")
print(df.columns)

# Falls die Spaltennamen unerwartete Leerzeichen oder Zeilenumbrüche enthalten,
# kann es hilfreich sein, sie zu bereinigen. Beispielsweise:
df.columns = df.columns.str.strip().str.replace('\n', ' ').str.replace('\r', '')

# Anzeigen der bereinigten Spaltennamen
print("\nBereinigte Spaltennamen:")
print(df.columns)

# Sicherstellen, dass die Spalte 'Straftaten -insgesamt-' korrekt benannt ist
# Anpassen des Spaltennamens falls erforderlich
spalte_straftaten = 'Straftaten -insgesamt-'  # Passe diesen Namen an, falls nötig

if spalte_straftaten not in df.columns:
    raise ValueError(f"Die erwartete Spalte '{spalte_straftaten}' wurde nicht gefunden. Bitte überprüfe die Spaltennamen.")

# Konvertiere die Spalte in numerische Werte (falls noch nicht geschehen)
df[spalte_straftaten] = pd.to_numeric(df[spalte_straftaten], errors='coerce')

# Optional: Entferne Zeilen, bei denen die Gesamtzahl der Straftaten fehlt
df = df.dropna(subset=[spalte_straftaten])

# Sortiere den DataFrame nach der Gesamtzahl der Straftaten in absteigender Reihenfolge
df_sorted = df.sort_values(by=spalte_straftaten, ascending=False)

# Optional: Zur besseren Lesbarkeit den Index zurücksetzen
df_sorted = df_sorted.reset_index(drop=True)

# Anzeigen der sortierten Daten
print("\nSortierte Daten nach 'Straftaten -insgesamt-':")
print(df_sorted[[ 'Bezeichnung (Bezirksregion)', spalte_straftaten ]].head(10))  # Zeigt die Top 10 Bezirke

# Speichern der sortierten Daten in eine neue Excel-Datei
sortierte_datei = 'Fallzahlen_2023_sortiert.xlsx'
df_sorted.to_excel(sortierte_datei, index=False)
print(f"\nDie sortierten Daten wurden in '{sortierte_datei}' gespeichert.")