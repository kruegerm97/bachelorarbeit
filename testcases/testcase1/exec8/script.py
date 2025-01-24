import pandas as pd

# Pfad zur CSV-Datei
csv_datei = 'Fallzahlen&HZ2014-2023/FZ_2023.csv'  # Passe den Pfad entsprechend an

# Da die ersten 4 Zeilen Metadaten enthalten, überspringen wir diese
try:
    df = pd.read_csv(csv_datei, skiprows=4, delimiter=',', encoding='utf-8')
except FileNotFoundError:
    print(f"Die Datei {csv_datei} wurde nicht gefunden.")
    exit(1)
except Exception as e:
    print(f"Beim Lesen der Datei ist ein Fehler aufgetreten: {e}")
    exit(1)

# Anzeige der ersten paar Zeilen, um die Struktur zu verstehen
print("Erste fünf Zeilen der CSV-Datei:")
print(df.head())

# Überprüfen der Spaltennamen
print("\nSpaltennamen:")
print(df.columns.tolist())

# Annahme: Die Spalte "Straftaten -insgesamt-" ist die dritte Spalte
# Wegen Zeilenumbrüchen im Spaltennamen könnte der tatsächliche Name variieren
# Daher suchen wir die Spalte, die "Straftaten" und "insgesamt" enthält
spalte_straftaten = None
for spalte in df.columns:
    if 'Straftaten' in spalte and 'insgesamt' in spalte:
        spalte_straftaten = spalte
        break

if spalte_straftaten is None:
    print("Die Spalte für 'Straftaten insgesamt' wurde nicht gefunden.")
    exit(1)

# Entfernen von Tausender-Trennzeichen und Konvertieren zu Integer
df[spalte_straftaten] = df[spalte_straftaten].astype(str).str.replace(',', '').astype(int)

# Optional: Entfernen von überschüssigen Leerzeichen in den Bezirksnamen
df['Bezeichnung (Bezirksregion)'] = df['Bezeichnung (Bezirksregion)'].str.strip()

# Sortieren nach der Anzahl der Straftaten insgesamt in absteigender Reihenfolge
df_sortiert = df.sort_values(by=spalte_straftaten, ascending=False)

# Auswahl der relevanten Spalten für die Ausgabe
ergebnis = df_sortiert[['Bezeichnung (Bezirksregion)', spalte_straftaten]]

# Anzeige der sortierten Ergebnisse
print("\nBezirke sortiert nach insgesamt registrierten Straftaten im Jahr 2023:")
print(ergebnis.to_string(index=False))