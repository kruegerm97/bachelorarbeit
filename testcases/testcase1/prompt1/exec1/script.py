import pandas as pd

# Pfad zur Excel-Datei
datei_pfad = 'Fallzahlen.xlsx'

try:
    # Einlesen des spezifischen Sheets 'Fallzahlen_2023'
    df = pd.read_excel(datei_pfad, sheet_name='Fallzahlen_2023')

    # Anzeigen der ersten paar Zeilen zur Überprüfung
    print("Original DataFrame:")
    print(df.head())

    # Sortieren nach der Spalte 'Straftaten_insgesamt' in absteigender Reihenfolge
    df_sortiert = df.sort_values(by='Straftaten_insgesamt', ascending=False)

    # Zurücksetzen des Index (optional)
    df_sortiert.reset_index(drop=True, inplace=True)

    # Anzeige der sortierten DataFrame
    print("\nSortierter DataFrame nach 'Straftaten_insgesamt':")
    print(df_sortiert)

    # Optional: Speichern des sortierten DataFrames in eine neue Excel-Datei
    sortierte_datei_pfad = 'Fallzahlen_sortiert.xlsx'
    df_sortiert.to_excel(sortierte_datei_pfad, index=False)
    print(f"\nDer sortierte DataFrame wurde in '{sortierte_datei_pfad}' gespeichert.")

except FileNotFoundError:
    print(f"Die Datei '{datei_pfad}' wurde nicht gefunden.")
except ValueError as ve:
    print(f"Fehler beim Einlesen des Sheets: {ve}")
except Exception as e:
    print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")