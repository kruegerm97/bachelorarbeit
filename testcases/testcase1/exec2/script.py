import pandas as pd

# Datei einlesen
# Da die ersten 4 Zeilen Metadaten und leere Zeilen enthalten, überspringen wir diese
df = pd.read_csv('FZ_2023.csv', sep=',', skiprows=4, encoding='utf-8')

# Spaltennamen bereinigen: Entferne Zeilenumbrüche und führende/trailende Leerzeichen
df.columns = df.columns.str.replace('\n', ' ').str.strip()

# Identifizieren der relevanten Spalten
# Angenommen, die Spalte für "Straftaten insgesamt" enthält das Wort "insgesamt"
total_crime_col = [col for col in df.columns if 'insgesamt' in col.lower() and 'straftaten' in col.lower()]
if not total_crime_col:
    raise ValueError("Die Spalte 'Straftaten insgesamt' wurde nicht gefunden.")
total_crime_col = total_crime_col[0]

# Identifizieren der Spalte für Bezirksnamen
district_col = 'Bezeichnung (Bezirksregion)'

# Filtern der relevanten Daten:
# - Ausschließen von Zeilen, die nicht zuzuordnen sind
# - Ausschließen der Gesamtsumme (z.B. "Berlin (PKS gesamt)")
df_filtered = df[~df[district_col].str.contains('nicht zuzuordnen|gesamt|Stadtgebiet Berlin', case=False, na=False)]

# Bereinigen der "Straftaten insgesamt" Spalte:
# - Entfernen von Tausendertrennzeichen (Kommas und Punkte)
# - Konvertieren in Ganzzahlen
df_filtered[total_crime_col] = df_filtered[total_crime_col].astype(str).str.replace('[.,]', '', regex=True).astype(int)

# Sortieren nach der Anzahl der Straftaten insgesamt in absteigender Reihenfolge
df_sorted = df_filtered.sort_values(by=total_crime_col, ascending=False)

# Optional: Zur besseren Lesbarkeit die DataFrame nur mit relevanten Spalten anzeigen
result = df_sorted[[district_col, total_crime_col]]

# Ausgabe der sortierten Liste
print(result.to_string(index=False))