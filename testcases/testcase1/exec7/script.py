import pandas as pd

# Pfad zur Excel-Datei
excel_file = 'Fallzahlen&HZ2014-2023.xlsx'

# Name des Sheets
sheet_name = 'Fallzahlen_2023'

# Anzahl der Zeilen, die übersprungen werden müssen, bevor die Header-Zeile kommt
# Basierend auf deinen Daten nehme ich an, dass die Header in der 5. Zeile (index=4) beginnen
skip_rows = 4

# Lesen des Excel-Sheets
try:
    df = pd.read_excel(
        excel_file,
        sheet_name=sheet_name,
        skiprows=skip_rows,
        thousands=',',  # Entfernt Tausender-Trennzeichen
        engine='openpyxl'
    )
except FileNotFoundError:
    print(f"Die Datei '{excel_file}' wurde nicht gefunden.")
    exit(1)
except Exception as e:
    print(f"Beim Lesen der Excel-Datei ist ein Fehler aufgetreten: {e}")
    exit(1)

# Anzeigen der ersten paar Zeilen, um die Struktur zu verstehen (optional)
# print(df.head())

# Bereinigen der Spaltennamen: Entfernen von Leerzeichen und Zeilenumbrüchen
df.columns = [col.strip().replace('\n', ' ') for col in df.columns]

# Identifizieren der relevanten Spalten
# Angenommen, die Spalte heißt "Straftaten - insgesamt -", passe den Namen ggf. an
straftaten_col = 'Straftaten -insgesamt-'

if straftaten_col not in df.columns:
    print(f"Die Spalte '{straftaten_col}' wurde nicht gefunden. Verfügbare Spalten: {df.columns.tolist()}")
    exit(1)

# Optional: Entfernen von aggregierten oder nicht zugeordneten Bezirken
# Falls du nur tatsächliche Bezirke möchtest, kannst du Zeilen filtern, die bestimmte Schlüssel enthalten
# Beispiel:
# df = df[~df['LOR-Schlüssel (Bezirksregion)'].str.contains('900|999')]

# Entfernen von Bezirken, die nicht zugeordnet sind
df = df[~df['Bezeichnung (Bezirksregion)'].str.contains('nicht zuzuordnen', case=False, na=False)]

# Entfernen von Gesamtwerten, z.B. "Berlin (PKS gesamt)"
df = df[~df['Bezeichnung (Bezirksregion)'].str.contains('gesamt', case=False, na=False)]

# Konvertieren der "Straftaten insgesamt" Spalte zu numerisch
# Fehlerhafte Einträge werden als NaN gesetzt
df[straftaten_col] = pd.to_numeric(df[straftaten_col], errors='coerce')

# Entfernen von Zeilen mit fehlenden "Straftaten insgesamt" Werten
df = df.dropna(subset=[straftaten_col])

# Sortieren nach "Straftaten insgesamt" absteigend
sorted_df = df.sort_values(by=straftaten_col, ascending=False)

# Optional: Zurücksetzen des Indexes
sorted_df = sorted_df.reset_index(drop=True)

# Anzeigen der sortierten Daten
print(sorted_df[['Bezeichnung (Bezirksregion)', straftaten_col]])

# Optional: Speichern der sortierten Daten in eine neue Excel- oder CSV-Datei
# sorted_df.to_excel('Sortierte_Fallzahlen_2023.xlsx', index=False)
# oder
# sorted_df.to_csv('Sortierte_Fallzahlen_2023.csv', index=False, sep=';')  # Mit Semikolon-Trennzeichen für deutsche Excel-Versionen