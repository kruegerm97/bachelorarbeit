import pandas as pd

# Pfad zur Excel-Datei
excel_datei = 'Fallzahlen.xlsx'

# Name des Sheets
sheet_name = 'Fallzahlen_2023'

# LOR-Schlüssel, die ausgeschlossen werden sollen
ausgeschlossene_lor_schluessel = [999900, 999999]

# Einlesen der Excel-Datei
try:
    df = pd.read_excel(excel_datei, sheet_name=sheet_name, engine='openpyxl')
    print("Excel-Datei erfolgreich eingelesen.")
except FileNotFoundError:
    print(f"Die Datei {excel_datei} wurde nicht gefunden.")
    exit(1)
except Exception as e:
    print(f"Ein Fehler ist aufgetreten beim Einlesen der Excel-Datei: {e}")
    exit(1)

# Filtern der Zeilen, die nicht zu Bezirken gehören
df_filtered = df[~df['LOR-Schlüssel'].isin(ausgeschlossene_lor_schluessel)]

# Sortieren nach 'Straftaten_insgesamt' in absteigender Reihenfolge
df_sorted = df_filtered.sort_values(by='Straftaten_insgesamt', ascending=False).reset_index(drop=True)

# Anzeige des sortierten DataFrames
print("Sortierte Daten nach 'Straftaten_insgesamt':")
print(df_sorted)

# Optional: Speichern des sortierten DataFrames in eine neue Excel-Datei
# df_sorted.to_excel('Fallzahlen_sortiert.xlsx', index=False)