import pandas as pd

# Pfad zur Excel-Datei
dateipfad = 'Fallzahlen.xlsx'

# Name des Sheets
sheet_name = 'Fallzahlen_2023'

# Einlesen der Excel-Datei
try:
    df = pd.read_excel(dateipfad, sheet_name=sheet_name)
    print("Daten erfolgreich eingelesen.")
except FileNotFoundError:
    print(f"Die Datei {dateipfad} wurde nicht gefunden.")
    exit()
except ValueError:
    print(f"Das Sheet '{sheet_name}' existiert nicht in der Datei.")
    exit()

# Überprüfen der Spaltennamen (optional)
print("Verfügbare Spalten:")
print(df.columns.tolist())

# Sortieren nach 'Straftaten_insgesamt' in absteigender Reihenfolge
# Falls aufsteigend gewünscht ist, setze ascending=True
try:
    df_sortiert = df.sort_values(by='Straftaten_insgesamt', ascending=False)
    print("Daten erfolgreich sortiert.")
except KeyError:
    print("Die Spalte 'Straftaten_insgesamt' wurde nicht gefunden.")
    exit()

# Zurücksetzen des Indexes (optional)
df_sortiert.reset_index(drop=True, inplace=True)

# Anzeigen des sortierten DataFrames
print("Sortiertes DataFrame:")
print(df_sortiert)