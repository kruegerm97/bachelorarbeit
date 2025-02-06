import pandas as pd

# Pfad zur Excel-Datei
excel_datei = 'Fallzahlen.xlsx'

# Name des Sheets
sheet_name = 'Fallzahlen_2023'

# LOR-Schlüssel, die ausgeschlossen werden sollen
ausschluss_schluessel = [999900, 999999]

try:
    # Excel-Datei einlesen
    df = pd.read_excel(excel_datei, sheet_name=sheet_name)

    # Anzeige der ersten paar Zeilen zur Überprüfung (optional)
    print("Originaldaten:")
    print(df.head())

    # Filter anwenden, um die auszuschließenden LOR-Schlüssel zu entfernen
    df_filtered = df[~df['LOR-Schlüssel'].isin(ausschluss_schluessel)]

    # Anzeige der gefilterten Daten zur Überprüfung (optional)
    print("\nGefilterte Daten:")
    print(df_filtered.head())

    # Sortieren nach 'Straftaten_insgesamt' absteigend (größte zuerst)
    df_sorted = df_filtered.sort_values(by='Straftaten_insgesamt', ascending=False)

    # Ergebnis anzeigen (optional)
    print("\nSortierte Daten:")
    print(df_sorted)

    # Optional: Das sortierte DataFrame speichern
    # df_sorted.to_excel('Fallzahlen_sortiert.xlsx', index=False)

except FileNotFoundError:
    print(f"Die Datei {excel_datei} wurde nicht gefunden.")
except Exception as e:
    print(f"Ein Fehler ist aufgetreten: {e}")