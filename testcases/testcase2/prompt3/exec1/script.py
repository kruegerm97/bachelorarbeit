import pandas as pd

def main():
    # 1. Excel-Datei einlesen und alle Sheets als DataFrames speichern
    excel_datei = 'Fallzahlen.xlsx'
    try:
        # Liest alle Sheets und speichert sie in einem Dictionary
        sheets_dict = pd.read_excel(excel_datei, sheet_name=None)
    except FileNotFoundError:
        print(f"Die Datei '{excel_datei}' wurde nicht gefunden.")
        return
    except Exception as e:
        print(f"Fehler beim Lesen der Excel-Datei: {e}")
        return

    # 2. DataFrames der einzelnen Sheets zusammenführen
    df_liste = []
    for sheet_name, df in sheets_dict.items():
        # Überprüfen, ob die erforderlichen Spalten existieren
        if 'LOR-Schlüssel' not in df.columns or 'Bezirke' not in df.columns:
            print(f"Sheet '{sheet_name}' enthält nicht die erforderlichen Spalten.")
            continue

        # Setzen von 'LOR-Schlüssel' und 'Bezirke' als Index
        df = df.set_index(['LOR-Schlüssel', 'Bezirke'])
        df_liste.append(df)

    if not df_liste:
        print("Keine gültigen Sheets zum Verarbeiten gefunden.")
        return

    # Alle DataFrames zusammenfügen und numerische Spalten akkumulieren
    zusammengefuegt_df = pd.concat(df_liste)
    # Gruppieren nach den Index-Spalten und summieren der numerischen Werte
    akkumuliert_df = zusammengefuegt_df.groupby(level=['LOR-Schlüssel', 'Bezirke']).sum().reset_index()

    # 3. DataFrame sortieren nach 'Straftaten_insgesamt', spezielle Zeilen am Ende platzieren
    # Definieren der speziellen LOR-Schlüssel
    spezielle_keys = [999900, 999999]

    # Trennen der regulären und speziellen Zeilen
    regulär_df = akkumuliert_df[~akkumuliert_df['LOR-Schlüssel'].isin(spezielle_keys)]
    spezielle_df = akkumuliert_df[akkumuliert_df['LOR-Schlüssel'].isin(spezielle_keys)]

    # Sortieren der regulären Zeilen nach 'Straftaten_insgesamt' absteigend
    sortiert_regulär_df = regulär_df.sort_values(by='Straftaten_insgesamt', ascending=False)

    # Kombinieren der sortierten regulären Zeilen mit den speziellen Zeilen
    endgültiges_df = pd.concat([sortiert_regulär_df, spezielle_df], ignore_index=True)

    # 4. Sortiertes DataFrame zurückgeben (hier als Ausgabe angezeigt)
    print(endgültiges_df)

if __name__ == '__main__':
    main()