import pandas as pd

# Pfad zur Excel-Datei
excel_datei = 'Fallzahlen.xlsx'

# Name des Sheets
sheet_name = 'Fallzahlen_2023'

try:
    # Einlesen der Excel-Datei
    df = pd.read_excel(excel_datei, sheet_name=sheet_name)
    print("Excel-Datei erfolgreich eingelesen.")

    # Überprüfen, ob die erforderte Spalte existiert
    if 'Straftaten_insgesamt' not in df.columns:
        raise ValueError("Die Spalte 'Straftaten_insgesamt' wurde im DataFrame nicht gefunden.")

    # Sortieren des DataFrames nach 'Straftaten_insgesamt' in absteigender Reihenfolge
    df_sorted = df.sort_values(by='Straftaten_insgesamt', ascending=False).reset_index(drop=True)
    print("DataFrame erfolgreich nach 'Straftaten_insgesamt' sortiert.")

    # Optional: Anzeige der sortierten Daten
    print(df_sorted)

    # Optional: Speichern des sortierten DataFrames in eine neue Excel-Datei
    # df_sorted.to_excel('Fallzahlen_sorted.xlsx', index=False)
    # print("Sortierte Daten wurden in 'Fallzahlen_sorted.xlsx' gespeichert.")

except FileNotFoundError:
    print(f"Die Datei '{excel_datei}' wurde nicht gefunden.")
except ValueError as ve:
    print(f"Fehler: {ve}")
except Exception as e:
    print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")