import pandas as pd

def main():
    # Pfad zur CSV-Datei
    csv_file = 'FZ_2023.csv'

    try:
        # CSV-Datei lesen, die ersten 4 Zeilen überspringen
        df = pd.read_csv(
            csv_file,
            sep=',',
            quotechar='"',
            thousands=',',
            skiprows=4,
            encoding='utf-8'
        )
    except FileNotFoundError:
        print(f"Die Datei {csv_file} wurde nicht gefunden. Bitte überprüfe den Pfad.")
        return
    except Exception as e:
        print(f"Ein Fehler ist beim Lesen der Datei aufgetreten: {e}")
        return

    # Säubere die Spaltennamen (entferne führende/trailende Leerzeichen und Zeilenumbrüche)
    df.columns = df.columns.str.strip().str.replace('\n', ' ').str.replace('\r', ' ')

    # Überprüfen, welche Spalten vorhanden sind
    print("Verfügbare Spalten:")
    for col in df.columns:
        print(f"- {col}")

    # Angenommen, die Spalte für insgesamt Straftaten heißt 'Straftaten -insgesamt-'
    # Möglicherweise musst du den genauen Spaltennamen anpassen
    total_crime_col = 'Straftaten -insgesamt-'

    if total_crime_col not in df.columns:
        print(f"Die erwartete Spalte '{total_crime_col}' wurde nicht gefunden.")
        return

    # Entferne Zeilen, die 'nicht zuzuordnen' enthalten
    df = df[~df['Bezeichnung (Bezirksregion)'].str.contains('nicht zuzuordnen', na=False)]

    # Konvertiere die Spalte für insgesamt Straftaten in numerische Werte
    df[total_crime_col] = pd.to_numeric(df[total_crime_col], errors='coerce')

    # Entferne Zeilen mit fehlenden Werten in der Strafaten-Spalte
    df = df.dropna(subset=[total_crime_col])

    # Sortiere die Daten nach der Anzahl der Straftaten insgesamt in absteigender Reihenfolge
    df_sorted = df.sort_values(by=total_crime_col, ascending=False)

    # Setze den Index zurück für eine saubere Ausgabe
    df_sorted = df_sorted.reset_index(drop=True)

    # Ausgabe der sortierten Daten
    print("\nBezirke sortiert nach der Anzahl der insgesamt gemeldeten Straftaten (2023):\n")
    print(df_sorted[['Bezeichnung (Bezirksregion)', total_crime_col]])

    # Optional: Speichere das Ergebnis in eine neue CSV-Datei
    output_file = 'sorted_crime_data_2023.csv'
    df_sorted[['Bezeichnung (Bezirksregion)', total_crime_col]].to_csv(
        output_file,
        index=False,
        encoding='utf-8'
    )
    print(f"\nDie sortierten Daten wurden in '{output_file}' gespeichert.")

if __name__ == "__main__":
    main()