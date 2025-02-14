import pandas as pd

# Pfad zur Excel-Datei
excel_datei = 'Fallzahlen&HZ 2014-2023.xlsx'

# Lesen des Sheets 'Fallzahlen_2023'
df = pd.read_excel(excel_datei, sheet_name='Fallzahlen_2023')

# Anzeigen der ersten Zeilen zur Überprüfung (optional)
# print(df.head())

# Sicherstellen, dass 'LOR-Schlüssel' als String behandelt wird
df['LOR-Schlüssel'] = df['LOR-Schlüssel'].astype(str)

# Extrahieren der Oberbezirk-Information aus den ersten 3 Zeichen des LOR-Schlüssels
# Passen Sie dies an, falls die Struktur anders ist
df['Oberbezirk_Key'] = df['LOR-Schlüssel'].str[:3]

# Optional: Definieren Sie eine Mapping-Tabelle für Oberbezirk_Key zu Oberbezirk_Name
# Hier ist ein Beispiel. Sie müssen dies basierend auf Ihrer spezifischen Kodierung anpassen.
oberbezirk_mapping = {
    '100': 'Mitte',
    '110': 'Cluster A',  # Beispielnamen
    '120': 'Cluster B',
    # Fügen Sie weitere Zuordnungen hier hinzu
    # ...
}

# Hinzufügen einer Spalte für den Oberbezirk-Namen
df['Oberbezirk'] = df['Oberbezirk_Key'].map(oberbezirk_mapping)

# Falls bestimmte Keys nicht im Mapping vorhanden sind, können Sie den Key als Namen verwenden
df['Oberbezirk'] = df['Oberbezirk'].fillna(df['Oberbezirk_Key'])

# Bereinigen der Daten: Entfernen von Einträgen, die nicht zugeordnet werden können
ausgeschlossene_terms = ['nicht zuzuordnen', 'gesamt']

df_clean = df[~df['Bezeichnung (Bezirksregion)'].str.contains('|'.join(ausgeschlossene_terms), na=False)]

# Gruppieren nach Oberbezirk und Finden des Unterbezirks mit den meisten Raubdelikten
result = df_clean.loc[df_clean.groupby('Oberbezirk')['Raub'].idxmax()][['Oberbezirk', 'Bezeichnung (Bezirksregion)', 'Raub']]

# Sortieren der Ergebnisse nach Oberbezirk (optional)
result = result.sort_values('Oberbezirk')

# Ausgabe der Ergebnisse
for index, row in result.iterrows():
    print(f"Oberbezirk: {row['Oberbezirk']}, Unterbezirk mit den meisten Raubdelikten: {row['Bezeichnung (Bezirksregion)']} ({row['Raub']} Raubdelikte)")

# Optional: Speichern der Ergebnisse in einer neuen Excel- oder CSV-Datei
# result.to_excel('Ergebnis_Most_Raubdelikte.xlsx', index=False)
# oder
# result.to_csv('Ergebnis_Most_Raubdelikte.csv', index=False)