import pandas as pd

# 1. Lesen Sie alle Sheets der Excel-Datei ein und speichern Sie jedes Sheet in einem separaten DataFrame
excel_file = 'Fallzahlen.xlsx'
xls = pd.read_excel(excel_file, sheet_name=None)  # Liest alle Sheets als ein Dictionary

# Dictionary zur Speicherung der 'Straftaten_insgesamt' Werte pro Jahr
straftaten_dict = {}

for sheet_name, df in xls.items():
    # Extrahiere das Jahr aus dem Sheet-Namen, z.B. 'Fallzahlen_2014' -> 2014
    try:
        year = int(sheet_name.split('_')[-1])
    except ValueError:
        print(f"Sheet-Name '{sheet_name}' entspricht nicht dem erwarteten Muster 'Fallzahlen_Jahr'. Übersprungen.")
        continue
    
    # 2. Extrahiere den Wert der Spalte 'Straftaten_insgesamt' für die Zeile 'Berlin (PKS gesamt)'
    # Überprüfen Sie, ob die Spaltennamen korrekt sind. Möglicherweise müssen Sie 'Bezirke' anpassen.
    # Hier wird angenommen, dass die Spalte mit Bezirken 'Bezirke' heißt
    berlin_row = df[df['Bezirke'] == 'Berlin (PKS gesamt)']
    
    if not berlin_row.empty:
        straf_value = berlin_row['Straftaten_insgesamt'].values[0]
        straftaten_dict[year] = straf_value
    else:
        print(f"'Berlin (PKS gesamt)' nicht in Sheet '{sheet_name}' gefunden.")

# 3. Berechnen Sie die prozentuale Veränderung zum jeweiligen Vorjahr
# Sortieren der Jahre
sorted_years = sorted(straftaten_dict.keys())
percentage_changes = []

for i in range(1, len(sorted_years)):
    current_year = sorted_years[i]
    previous_year = sorted_years[i - 1]
    current_value = straftaten_dict[current_year]
    previous_value = straftaten_dict[previous_year]
    
    # Prozentuale Veränderung berechnen
    if previous_value != 0:
        percent_change = ((current_value - previous_value) / previous_value) * 100
    else:
        percent_change = None  # Vermeiden von Division durch Null
    
    percentage_changes.append({
        'Jahr': current_year,
        'Prozentuale Veränderung': percent_change
    })

# 4. Speichern Sie die Ergebnisse in einem neuen DataFrame
result_df = pd.DataFrame(percentage_changes)

# Optional: Hinzufügen des ersten Jahres mit einer NaN für die Veränderung
result_df = pd.concat([
    pd.DataFrame({'Jahr': [sorted_years[0]], 'Prozentuale Veränderung': [None]}),
    result_df
], ignore_index=True)

# Anzeige des Ergebnisses
print(result_df)

# Optional: Speichern des Ergebnisses in eine neue Excel-Datei
result_df.to_excel('Prozentuale_Veraenderung_Straftaten.xlsx', index=False)