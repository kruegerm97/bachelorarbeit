import pandas as pd
import re

def main():
    # Pfad zur Excel-Datei
    EXCEL_FILE = 'Fallzahlen&HZ2014-2023.xlsx'

    # Regulärer Ausdruck zur Identifizierung relevanter Sheets
    sheet_pattern = re.compile(r'^Fallzahlen_\d{4}$')
    # Jahre von 2014 bis 2023
    YEARS = range(2014, 2024)

    try:
        # Excel-Datei laden
        excel = pd.ExcelFile(EXCEL_FILE)
    except FileNotFoundError:
        print(f"Die Datei {EXCEL_FILE} wurde nicht gefunden.")
        return
    except Exception as e:
        print(f"Fehler beim Laden der Excel-Datei: {e}")
        return

    # Liste zum Speichern der DataFrames
    df_list = []

    # Iteration über alle Sheets in der Excel-Datei
    for sheet_name in excel.sheet_names:
        if sheet_pattern.match(sheet_name):
            try:
                # Sheet einlesen, die ersten 4 Zeilen überspringen
                df = pd.read_excel(excel, sheet_name=sheet_name, skiprows=4)

                # Spaltennamen bereinigen
                df.columns = df.columns.str.strip().str.replace('\n', '').str.replace(' ', '_').str.lower()

                # Relevante Spalten identifizieren
                if 'bezeichnung_(bezirksregion)' in df.columns and 'straftaten_insgesamt' in df.columns:
                    bezirk_col = 'bezeichnung_(bezirksregion)'
                    straftaten_col = 'straftaten_insgesamt'
                else:
                    # Alternative Spaltennamen suchen
                    columns_lower = [col.lower() for col in df.columns]
                    bezeichnung_idx = [i for i, col in enumerate(columns_lower) if 'bezeichnung' in col and 'bezirksregion' in col]
                    straftaten_idx = [i for i, col in enumerate(columns_lower) if 'straftaten' in col and 'gesamt' in col]
                    if bezeichnung_idx and straftaten_idx:
                        bezirk_col = df.columns[bezeichnung_idx[0]]
                        straftaten_col = df.columns[straftaten_idx[0]]
                    else:
                        print(f"Relevante Spalten in Sheet {sheet_name} nicht gefunden.")
                        continue

                # Relevante Spalten extrahieren und umbenennen
                df_subset = df[[bezirk_col, straftaten_col]].copy()
                df_subset = df_subset.rename(columns={bezirk_col: 'bezirk', straftaten_col: 'straftaten'})

                # NaN-Werte entfernen
                df_subset = df_subset.dropna(subset=['bezirk', 'straftaten'])

                # Straftaten bereinigen und in Integer umwandeln
                df_subset['straftaten'] = df_subset['straftaten'].astype(str).str.replace('[\.,]', '', regex=True).astype(int)

                # DataFrame zur Liste hinzufügen
                df_list.append(df_subset)
            except Exception as e:
                print(f"Fehler beim Verarbeiten von Sheet {sheet_name}: {e}")
                continue

    if not df_list:
        print("Keine relevanten Daten gefunden.")
        return

    # Alle DataFrames zusammenführen
    all_data = pd.concat(df_list, ignore_index=True)

    # Straftaten pro Bezirk summieren
    total_crimes = all_data.groupby('bezirk')['straftaten'].sum()

    # Bezirk mit den meisten Straftaten ermitteln
    max_bezirk = total_crimes.idxmax()
    max_crime = total_crimes.max()

    print(f"Bezirk mit den meisten Straftaten: {max_bezirk} mit insgesamt {max_crime} Straftaten.")

if __name__ == "__main__":
    main()