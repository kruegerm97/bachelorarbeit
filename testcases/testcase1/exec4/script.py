import pandas as pd

# Definiere den Dateinamen
csv_file = 'FZ_2023.csv'

# Lies die CSV-Datei ein
# Überspringe die ersten Zeilen, bis die eigentlichen Daten beginnen
# Da die Datei mehrere Kopfzeilen oder leere Zeilen enthalten könnte, 
# stelle sicher, dass der Header korrekt erkannt wird
df = pd.read_csv(csv_file, 
                sep=",",
                skiprows=4,  # Passe dies an, falls mehr/fewer Zeilen übersprungen werden müssen
                encoding='utf-8')

# Zeige die ersten paar Zeilen, um sicherzustellen, dass die Daten korrekt eingelesen wurden
print("Erste 5 Zeilen der CSV-Datei:")
print(df.head())

# Bereinige die Daten
# Entferne Tausender-Trennzeichen und konvertiere die Spalte zu numerischen Werten
df['Straftaten -insgesamt'] = df['Straftaten -insgesamt-'].astype(str).str.replace(",", "").astype(int)

# Optional: Entferne aggregierte oder nicht zugeordnete Bezirke
# Zum Beispiel, entferne Zeilen, die "nicht zuzuordnen" enthalten oder spezielle LOR-Schlüssel
df = df[~df['Bezeichnung (Bezirksregion)'].str.contains("nicht zuzuordnen", case=False, na=False)]

# Sortiere die Daten nach der Anzahl der Straftaten insgesamt in absteigender Reihenfolge
sorted_df = df.sort_values(by='Straftaten -insgesamt', ascending=False)

# Setze den Index zurück, um eine saubere Anzeige zu erhalten
sorted_df = sorted_df.reset_index(drop=True)

# Zeige die sortierte Liste
print("\nBezirke sortiert nach der Anzahl der insgesamt erfassten Straftaten (absteigend):")
print(sorted_df[['Bezeichnung (Bezirksregion)', 'Straftaten -insgesamt']])

# Optional: Speichere die sortierten Daten in eine neue CSV-Datei
sorted_df[['Bezeichnung (Bezirksregion)', 'Straftaten -insgesamt']].to_csv('Straftaten_sortiert.csv', index=False, encoding='utf-8-sig')