import pandas as pd

# Pfad zur CSV-Datei
csv_datei = 'FZ_2023.csv'

# Schritt 1: Lesen der CSV-Datei und Überspringen der irrelevanten ersten Zeilen
# Wir lesen die Datei ohne Header und durchsuchen dann nach der Zeile, die die Spaltenüberschriften enthält
with open(csv_datei, 'r', encoding='utf-8') as file:
    for i, zeile in enumerate(file):
        if zeile.startswith('LOR-Schlüssel (Bezirksregion)'):
            header_zeile = i
            break

# Schritt 2: Laden der Daten mit den korrekten Headern
df = pd.read_csv(
    csv_datei,
    skiprows=header_zeile,
    sep=',',
    encoding='utf-8',
    quotechar='"',
    engine='python'  # Verwenden des Python-Engines für bessere Handhabung von Anführungszeichen
)

# Schritt 3: Bereinigung der Daten

# Entfernen von führenden und nachfolgenden Leerzeichen in den Spaltennamen
df.columns = df.columns.str.strip()

# Entfernen von Zeilen, die keinen gültigen LOR-Schlüssel haben (z.B. leere Zeilen)
df = df.dropna(subset=['LOR-Schlüssel (Bezirksregion)'])

# Optional: Entfernen der Gesamtsumme-Zeile, falls nicht benötigt
df = df[df['LOR-Schlüssel (Bezirksregion)'] != '999999']

# Schritt 4: Konvertieren der "Straftaten - insgesamt -" Spalte in numerische Werte
# Entfernen von Punkten und Kommata, die als Tausendertrennzeichen dienen
# In diesem Datensatz scheinen die Kommata als Tausendertrennzeichen zu fungieren

# Definieren der Spaltennamen basierend auf den gelieferten Daten
# Es ist wichtig, den genauen Spaltennamen zu verwenden. Hier nehmen wir an, dass die dritte Spalte "Straftaten - insgesamt -" heißt
# Falls der Name anders ist, passen Sie ihn entsprechend an.
spalte_straftaten = 'Straftaten - insgesamt-'

# Entfernen von Kommas und Konvertieren in Integer
df[spalte_straftaten] = df[spalte_straftaten].astype(str).str.replace(',', '').astype(int)

# Schritt 5: Sortieren der Bezirke nach der Anzahl der Straftaten insgesamt in absteigender Reihenfolge
df_sortiert = df.sort_values(by=spalte_straftaten, ascending=False)

# Schritt 6: Auswahl der relevanten Spalten für die Ausgabe
# Zum Beispiel: Bezirksregion und Anzahl der Straftaten
df_sortiert = df_sortiert[['Bezeichnung (Bezirksregion)', spalte_straftaten]]

# Schritt 7: Anzeigen des sortierten DataFrames
print(df_sortiert.to_string(index=False))