import pandas as pd

def process_fallzahlen(excel_file):
    # 1. Die Excel-Datei einlesen und die Sheets als DataFrames speichern.
    # Alle Sheets werden in einem Dictionary gespeichert, wobei der Sheet-Name der Schlüssel ist.
    xls = pd.ExcelFile(excel_file)
    sheets_dict = {}
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        sheets_dict[sheet_name] = df

    # 2. Die DataFrames der einzelnen Sheets zusammen joinen,
    # sodass pro Zeile der akkumulierte Wert der einzelnen Straftaten steht.
    # Annahme: Alle DataFrames haben die selben 'LOR-Schlüssel' und 'Bezirke'.
    # Wir setzen 'LOR-Schlüssel' und 'Bezirke' als Index und summieren die numerischen Spalten.
    
    # Liste der DataFrames
    df_list = []
    for df in sheets_dict.values():
        # Setze 'LOR-Schlüssel' und 'Bezirke' als Index
        df = df.set_index(['LOR-Schlüssel', 'Bezirke'])
        df_list.append(df)

    # Addiere alle DataFrames
    # Dabei werden numerische Spalten summiert, nicht-numerische ignoriert
    joined_df = pd.concat(df_list).groupby(['LOR-Schlüssel', 'Bezirke']).sum().reset_index()

    # 3. Das neue gejointe DataFrame nach der Spalte "Straftaten_insgesamt" sortieren.
    # Zeilen mit den LOR-Schlüsseln 999900 und 999999 werden nicht in die Sortierung einbezogen
    # und am Ende des DataFrames angehängt.
    
    # Trenne die speziellen LOR-Schlüssel
    special_keys = [999900, 999999]
    normal_df = joined_df[~joined_df['LOR-Schlüssel'].isin(special_keys)]
    special_df = joined_df[joined_df['LOR-Schlüssel'].isin(special_keys)]

    # Sortiere das normale DataFrame nach 'Straftaten_insgesamt' absteigend
    sorted_normal_df = normal_df.sort_values(by='Straftaten_insgesamt', ascending=False)

    # Füge die speziellen Zeilen am Ende hinzu
    final_df = pd.concat([sorted_normal_df, special_df], ignore_index=True)

    # 4. Das sortierte Pandas DataFrame zurückgeben.
    return final_df

if __name__ == "__main__":
    # Pfad zur Excel-Datei
    excel_file = 'Fallzahlen.xlsx'
    
    # Verarbeite die Excel-Datei
    sorted_df = process_fallzahlen(excel_file)
    
    # Optional: Zeige die ersten Zeilen des sortierten DataFrames an
    print(sorted_df.head())

    # Optional: Speichere das sortierte DataFrame in eine neue Excel-Datei
    sorted_df.to_excel('Fallzahlen_sortiert.xlsx', index=False)