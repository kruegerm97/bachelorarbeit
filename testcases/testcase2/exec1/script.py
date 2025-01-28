import pandas as pd
import re

def find_top_crime_district(excel_file_path):
    # Lade die Excel-Datei
    try:
        xl = pd.ExcelFile(excel_file_path)
    except FileNotFoundError:
        print(f"Die Datei {excel_file_path} wurde nicht gefunden.")
        return
    except Exception as e:
        print(f"Ein Fehler ist beim Lesen der Excel-Datei aufgetreten: {e}")
        return

    # Definiere das Muster für relevante Sheets (Fallzahlen_2014 bis Fallzahlen_2023)
    pattern = re.compile(r"Fallzahlen_\d{4}")

    # Filtere die Sheet-Namen
    relevant_sheets = [sheet for sheet in xl.sheet_names if pattern.fullmatch(sheet)]

    if not relevant_sheets:
        print("Keine relevanten Sheets gefunden.")
        return

    # Initialisiere eine Liste zur Speicherung der Datenframes
    df_list = []

    for sheet in relevant_sheets:
        try:
            # Lese das Sheet, überspringe die ersten 5 Zeilen, die Metadaten enthalten könnten
            df = pd.read_excel(xl, sheet_name=sheet, skiprows=5)

            # Verwende die ersten Zeilen als Header, falls notwendig
            # df.columns = df.iloc[0]
            # df = df[1:]

            # Wähle die relevanten Spalten
            # Angenommen, 'Bezeichnung (Bezirksregion)' ist die Bezirksbezeichnung
            # und 'Straftaten \n-insgesamt-' ist die Gesamtanzahl der Straftaten
            bezirk_col = 'Bezeichnung (Bezirksregion)'
            strftaten_col = 'Straftaten \n-insgesamt-'

            if bezirk_col not in df.columns or strftaten_col not in df.columns:
                # Möglicherweise sind die Spalten leicht anders benannt, versuche es mit ähnlichen Namen
                bezirk_col = [col for col in df.columns if 'Bezeichnung' in col][0]
                strftaten_col = [col for col in df.columns if 'Straftaten' in col and 'insgesamt' in col][0]

            temp_df = df[[bezirk_col, strftaten_col]].copy()

            # Bereinige die Straftaten-Spalte: Entferne Kommas und konvertiere zu int
            temp_df[strftaten_col] = temp_df[strftaten_col].astype(str).str.replace(',', '').str.replace('.', '').astype(int)

            # Entferne eventuelle NaN oder leere Bezirke
            temp_df = temp_df.dropna(subset=[bezirk_col, strftaten_col])

            # Füge das bereinigte DataFrame zur Liste hinzu
            df_list.append(temp_df)

        except Exception as e:
            print(f"Ein Fehler ist beim Verarbeiten des Sheets {sheet} aufgetreten: {e}")
            continue

    if not df_list:
        print("Keine Daten zum Verarbeiten vorhanden.")
        return

    # Kombiniere alle DataFrames
    combined_df = pd.concat(df_list)

    # Gruppiere nach Bezirk und summiere die Straftaten
    total_crimes = combined_df.groupby(bezirk_col)[strftaten_col].sum()

    # Finde den Bezirk mit den meisten Straftaten
    top_district = total_crimes.idxmax()
    top_crimes = total_crimes.max()

    print(f"Der Bezirk mit den meisten Straftaten über alle Jahre ist '{top_district}' mit insgesamt {top_crimes} Straftaten.")

    return top_district, top_crimes

# Beispielaufruf:
# Ersetze 'Fallzahlen&HZ2014-2023.xlsx' durch den Pfad zu deiner Excel-Datei
excel_file = 'Fallzahlen&HZ2014-2023.xlsx'
find_top_crime_district(excel_file)