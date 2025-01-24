import pandas as pd

# Pfad zur CSV-Datei (passen Sie den Pfad entsprechend an)
csv_datei = 'FZ_2023.csv'

# Lesen der CSV-Datei
# Überspringt die ersten 4 Zeilen, da diese keine relevanten Daten enthalten
df = pd.read_csv(csv_datei, skiprows=4, delimiter=',', encoding='utf-8')

# Anzeigen der Spaltennamen, um sicherzustellen, dass die Daten korrekt eingelesen wurden
#print(df.columns.tolist())

# Entfernen von Tausender-Trennzeichen und Konvertieren der numerischen Spalten in Zahlen
# Annahme: Alle Spalten ab der dritten sind numerische Werte
# Erste zwei Spalten sind 'LOR-Schlüssel (Bezirksregion)' und 'Bezeichnung (Bezirksregion)'
numerische_spalten = df.columns[2:]

for spalte in numerische_spalten:
    # Entfernen von Kommas und Punkten als Tausender-Trennzeichen
    df[spalte] = df[spalte].astype(str).str.replace('.', '').str.replace(',', '')
    # Konvertieren in numerische Typen
    df[spalte] = pd.to_numeric(df[spalte], errors='coerce')

# Überprüfen, ob die Konvertierung funktioniert hat
#print(df.head())

# Sortieren der Bezirke nach 'Straftaten -insgesamt-' in absteigender Reihenfolge
df_sortiert = df.sort_values(by='Straftaten -insgesamt-', ascending=False)

# Auswahl der relevanten Spalten für die Ausgabe
ergebnis = df_sortiert[['Bezeichnung (Bezirksregion)', 'Straftaten -insgesamt-']]

# Anzeigen des sortierten Ergebnisses
print(ergebnis)

# Optional: Speichern des sortierten Ergebnisses in einer neuen CSV-Datei
df_sortiert.to_csv('FZ_2023_sortiert.csv', index=False, encoding='utf-8')