import pandas as pd

# Pfad zur Excel-Datei
excel_file = 'Fallzahlen.xlsx'

# LOR-Schlüssel, die ausgeschlossen werden sollen
exclude_lor_keys = [999900, 999999]

# Alle Sheets laden
sheets_dict = pd.read_excel(excel_file, sheet_name=None)

# Liste zur Speicherung der bereinigten DataFrames
filtered_dfs = []

for sheet_name, df in sheets_dict.items():
    # Sicherstellen, dass die benötigten Spalten vorhanden sind
    if 'LOR-Schlüssel' not in df.columns or 'Bezirke' not in df.columns:
        print(f"Sheet '{sheet_name}' übersprungen, da erforderliche Spalten fehlen.")
        continue
    
    # Ausschließen der unerwünschten LOR-Schlüssel
    df_filtered = df[~df['LOR-Schlüssel'].isin(exclude_lor_keys)].copy()
    
    # Optional: Hinzufügen einer Spalte zur Kennzeichnung des Sheets
    df_filtered['Sheet'] = sheet_name
    
    filtered_dfs.append(df_filtered)

# Überprüfen, ob es DataFrames zum Zusammenführen gibt
if not filtered_dfs:
    raise ValueError("Keine gültigen Daten zum Zusammenführen gefunden.")

# Zusammenführen aller DataFrames auf Basis von 'LOR-Schlüssel' und 'Bezirke'
# Falls es gemeinsame Spalten außer den Schlüsseln gibt, werden sie mit Suffixen versehen
from functools import reduce

# Füge die DataFrames schrittweise zusammen
merged_df = reduce(lambda left, right: pd.merge(left, right, on=['LOR-Schlüssel', 'Bezirke'], how='outer', suffixes=('', '_dup')), filtered_dfs)

# Optional: Entfernen von doppelten Spalten, die durch die Zusammenführung entstehen könnten
merged_df = merged_df.loc[:, ~merged_df.columns.duplicated()]

# Sortieren nach 'Straftaten_insgesamt' absteigend
if 'Straftaten_insgesamt' in merged_df.columns:
    sorted_df = merged_df.sort_values(by='Straftaten_insgesamt', ascending=False)
else:
    print("'Straftaten_insgesamt' Spalte nicht gefunden. Sortierung übersprungen.")
    sorted_df = merged_df

# Reset des Indexes
sorted_df.reset_index(drop=True, inplace=True)

# Ergebnis anzeigen
print(sorted_df)

# Optional: Speichern des sortierten DataFrames in eine neue Excel-Datei
sorted_df.to_excel('Zusammengefuegte_Fallzahlen.xlsx', index=False)