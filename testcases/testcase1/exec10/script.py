import pandas as pd

def parse_number(number_str):
    """
    Konvertiert eine Zahl im deutschen Format (z.B. "83,611") in einen Integer.
    Entfernt Punkte als Tausendertrennzeichen und ersetzt Kommas durch nichts.
    """
    if pd.isna(number_str):
        return 0
    # Entferne Punkte und ersetze Kommas
    return int(number_str.replace('.', '').replace(',', ''))

def main():
    # Pfad zur CSV-Datei
    csv_file = 'FZ_2023.csv'

    # Lese die CSV-Datei
    # Überspringe die ersten 4 Zeilen, die keine relevanten Daten enthalten
    df = pd.read_csv(csv_file, skiprows=4, sep=',', encoding='utf-8')

    # Um benutzerfreundliche Spaltennamen zu haben, benenne sie um
    df = df.rename(columns=lambda x: x.strip().replace('\n', ' ') if isinstance(x, str) else x)

    # Anzeige der Spaltennamen zur Überprüfung
    # print(df.columns)

    # Wähle die relevanten Spalten aus
    # Annahme: 'Bezeichnung (Bezirksregion)' ist der Name des Bezirks
    # und die dritte Spalte 'Straftaten - insgesamt-' ist die Gesamtzahl der Straftaten
    district_col = 'Bezeichnung (Bezirksregion)'
    
    # Identifiziere die Spalte für Gesamtstraftaten
    # Da der Spaltenname möglicherweise Zeilenumbrüche enthält, finde ihn mit einem Teilstring
    total_crimes_col = [col for col in df.columns if 'Straftaten' in col and 'insgesamt' in col]
    if not total_crimes_col:
        print("Die Spalte für Gesamtstraftaten wurde nicht gefunden.")
        return
    total_crimes_col = total_crimes_col[0]

    # Extrahiere die relevanten Daten
    data = df[[district_col, total_crimes_col]].copy()
    
    # Entferne eventuelle Anführungszeichen und konvertiere die Zahlen
    data[total_crimes_col] = data[total_crimes_col].apply(parse_number)

    # Sortiere die Daten nach der Gesamtzahl der Straftaten in absteigender Reihenfolge
    sorted_data = data.sort_values(by=total_crimes_col, ascending=False)

    # Optional: Entferne Bezirke, die nicht zugeordnet sind (falls gewünscht)
    # sorted_data = sorted_data[~sorted_data[district_col].str.contains("nicht zuzuordnen")]

    # Anzeige der sortierten Daten
    print("Bezirke sortiert nach der Gesamtzahl der Straftaten (absteigend):\n")
    print(sorted_data.to_string(index=False))

    # Optional: Speichere die sortierten Daten in eine neue CSV-Datei
    sorted_data.to_csv('FZ_2023_sortiert.csv', index=False)

if __name__ == "__main__":
    main()