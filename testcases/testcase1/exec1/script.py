import pandas as pd

def clean_number(value):
    """
    Entfernt Anführungszeichen und Tausender-Trennzeichen,
    und konvertiert den Wert in einen Integer.
    """
    if pd.isna(value):
        return 0
    return int(str(value).replace('"', '').replace(',', '').strip())

def main():
    # Pfad zur CSV-Datei
    csv_file = 'FZ_2023.csv'

    # Öffnen der CSV-Datei und Finden der Header-Zeile
    with open(csv_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Suche nach der Header-Zeile, die mit 'LOR-Schlüssel (Bezirksregion)' beginnt
    header_line_idx = None
    for idx, line in enumerate(lines):
        if line.startswith('LOR-Schlüssel (Bezirksregion)'):
            header_line_idx = idx
            break

    if header_line_idx is None:
        print("Header-Zeile nicht gefunden.")
        return

    # Laden der Daten mit pandas, überspringen der vorherigen Zeilen
    df = pd.read_csv(
        csv_file,
        delimiter=',',
        skiprows=header_line_idx,
        encoding='utf-8'
    )

    # Anzeigen der ersten Zeilen zur Überprüfung
    # print(df.head())

    # Benennung der relevanten Spalten
    # Angenommen, die Spalten sind wie folgt:
    # 'LOR-Schlüssel (Bezirksregion)', 'Bezeichnung (Bezirksregion)', 'Straftaten - insgesamt-', ...
    bezeichnung_col = 'Bezeichnung (Bezirksregion)'
    strftaten_col = 'Straftaten - insgesamt-'

    # Einige Spaltennamen könnten Leerzeichen oder Zeilenumbrüche enthalten, daher:
    df.columns = df.columns.str.strip().str.replace('\n', ' ')

    # Überprüfen, ob die benötigten Spalten vorhanden sind
    if bezeichnung_col not in df.columns or strftaten_col not in df.columns:
        print(f"Benötigte Spalten '{bezeichnung_col}' oder '{strftaten_col}' nicht gefunden.")
        return

    # Bereinigen der 'Straftaten - insgesamt-' Spalte
    df['Straftaten_insgesamt'] = df[strftaten_col].apply(clean_number)

    # Entfernen von aggregierten oder nicht zugeordnete Bezirke, falls gewünscht
    # Hier behalten wir alle Bezirke, Sie können dies nach Bedarf anpassen

    # Sortieren des DataFrames nach 'Straftaten_insgesamt' absteigend
    df_sorted = df.sort_values(by='Straftaten_insgesamt', ascending=False)

    # Auswählen der relevanten Spalten für die Ausgabe
    output_df = df_sorted[[bezeichnung_col, 'Straftaten_insgesamt']]

    # Zur besseren Lesbarkeit die Zahlen mit Tausender-Trennzeichen formatieren
    output_df['Straftaten_insgesamt'] = output_df['Straftaten_insgesamt'].apply(lambda x: f"{x:,}".replace(',', '.'))

    # Anzeigen der sortierten Bezirke
    print("Bezirke sortiert nach der Anzahl der Straftaten insgesamt (2023):\n")
    print(output_df.to_string(index=False))

    # Optional: Speichern der sortierten Liste in eine neue CSV-Datei
    output_df.to_csv('Sortierte_Bezirge_Straftaten_2023.csv', index=False, encoding='utf-8')

if __name__ == "__main__":
    main()