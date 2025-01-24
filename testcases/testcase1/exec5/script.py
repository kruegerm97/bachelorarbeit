import pandas as pd

# Pfad zur CSV-Datei
csv_file = 'FZ_2023.csv'

# Lesen der CSV-Datei
# - Überspringen der ersten 4 Zeilen, die Metadaten enthalten
# - Festlegen des Trennzeichens auf Komma
# - Festlegen von Anführungszeichen auf "
# - Umgang mit Tausendertrennzeichen (,)
try:
    df = pd.read_csv(
        csv_file,
        skiprows=4,
        sep=',',
        quotechar='"',
        thousands=',',
        encoding='utf-8'
    )
except FileNotFoundError:
    print(f"Die Datei '{csv_file}' wurde nicht gefunden.")
    exit(1)
except Exception as e:
    print(f"Beim Lesen der Datei ist ein Fehler aufgetreten: {e}")
    exit(1)

# Anzeigen der ersten paar Zeilen, um die Struktur zu verstehen
print("Erste Zeilen des DataFrames:")
print(df.head())

# Bereinigen der Spaltennamen (Entfernen von Zeilenumbrüchen und überflüssigen Leerzeichen)
df.columns = df.columns.str.replace('\n', ' ').str.strip()

# Überprüfen, ob die relevante Spalte vorhanden ist
total_crimes_column = 'Straftaten - insgesamt-'
if total_crimes_column not in df.columns:
    print(f"Die Spalte '{total_crimes_column}' wurde in den Daten nicht gefunden.")
    exit(1)

# Entfernen von möglichen Leerzeichen in den Bezirksnamen
df['Bezeichnung (Bezirksregion)'] = df['Bezeichnung (Bezirksregion)'].str.strip()

# Sortieren des DataFrames basierend auf der Gesamtzahl der Straftaten in absteigender Reihenfolge
df_sorted = df.sort_values(by=total_crimes_column, ascending=False)

# Zur besseren Lesbarkeit die Index zurücksetzen
df_sorted.reset_index(drop=True, inplace=True)

# Ausgabe der sortierten Bezirke mit deren Gesamtzahl der Straftaten
print("\nBezirke sortiert nach der Gesamtzahl der Straftaten (absteigend):")
print(df_sorted[['Bezeichnung (Bezirksregion)', total_crimes_column]])

# Optional: Speichern des sortierten DataFrames in eine neue CSV-Datei
output_file = 'FZ_2023_sorted.csv'
try:
    df_sorted[['Bezeichnung (Bezirksregion)', total_crimes_column]].to_csv(
        output_file,
        index=False,
        encoding='utf-8'
    )
    print(f"\nDie sortierten Daten wurden erfolgreich in '{output_file}' gespeichert.")
except Exception as e:
    print(f"Beim Speichern der Datei ist ein Fehler aufgetreten: {e}")