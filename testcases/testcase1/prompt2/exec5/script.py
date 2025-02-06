import pandas as pd

# Pfad zur Excel-Datei
datei_pfad = 'Fallzahlen.xlsx'

# Namen des Sheets
sheet_name = 'Fallzahlen_2023'

# Einlesen der Excel-Datei
try:
    df = pd.read_excel(datei_pfad, sheet_name=sheet_name)
    print("Excel-Datei erfolgreich eingelesen.")
except FileNotFoundError:
    print(f"Die Datei {datei_pfad} wurde nicht gefunden.")
    exit(1)
except Exception as e:
    print(f"Ein Fehler ist aufgetreten beim Einlesen der Datei: {e}")
    exit(1)

# Anzeigen der ersten paar Zeilen, um sicherzustellen, dass die Daten korrekt eingelesen wurden
print("\nErste 5 Zeilen der Originaldaten:")
print(df.head())

# Filterkriterien: Ausschließen der LOR-Schlüssel 999900 und 999999
ausschluss_schluessel = [999900, 999999]
df_filtered = df[~df['LOR-Schlüssel'].isin(ausschluss_schluessel)]

print(f"\nAnzahl der Zeilen nach dem Ausschluss: {len(df_filtered)}")

# Sortieren nach 'Straftaten_insgesamt' in absteigender Reihenfolge
df_sorted = df_filtered.sort_values(by='Straftaten_insgesamt', ascending=False).reset_index(drop=True)

print("\nErste 5 Zeilen der sortierten Daten:")
print(df_sorted.head())

# Optional: Speichern des sortierten DataFrames in eine neue Excel-Datei
ausgabe_pfad = 'Fallzahlen_sortiert.xlsx'
try:
    df_sorted.to_excel(ausgabe_pfad, index=False)
    print(f"\nSortierte Daten wurden erfolgreich in '{ausgabe_pfad}' gespeichert.")
except Exception as e:
    print(f"Ein Fehler ist aufgetreten beim Speichern der Datei: {e}")