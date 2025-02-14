import pandas as pd

# Pfad zur Excel-Datei
excel_file = 'Fallzahlen&HZ 2014-2023.xlsx'

# Liste der Jahre, die verarbeitet werden sollen
jahre = range(2014, 2024)  # 2014 bis 2023

# Initialisiere ein leeres DataFrame für die Aggregation
gesamt_df = pd.DataFrame()

# Iteriere über jedes Jahr und lese das entsprechende Sheet
for jahr in jahre:
    sheet_name = f'Fallzahlen_{jahr}'
    try:
        # Lese das Sheet
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        
        # Überprüfe, ob die notwendigen Spalten vorhanden sind
        notwendige_spalten = ['Bezeichnung (Bezirksregion)', 'Straftaten insgesamt']
        if not all(spalte in df.columns for spalte in notwendige_spalten):
            print(f"Warnung: Nicht alle notwendigen Spalten in Sheet {sheet_name} gefunden.")
            continue
        
        # Wähle nur die relevanten Spalten
        df_relevant = df[['Bezeichnung (Bezirksregion)', 'Straftaten insgesamt']]
        
        # Benenne die Spalten um, um das Jahr zu identifizieren
        df_relevant = df_relevant.rename(columns={'Straftaten insgesamt': f'Straftaten_{jahr}'})
        
        # Setze die Bezirksregion als Index
        df_relevant.set_index('Bezeichnung (Bezirksregion)', inplace=True)
        
        # Füge zum Gesamt-DataFrame hinzu
        if gesamt_df.empty:
            gesamt_df = df_relevant
        else:
            gesamt_df = gesamt_df.join(df_relevant, how='outer')
    
    except FileNotFoundError:
        print(f"Fehler: Die Datei {excel_file} wurde nicht gefunden.")
        exit(1)
    except ValueError:
        print(f"Warnung: Das Sheet {sheet_name} wurde in der Datei {excel_file} nicht gefunden.")
        continue

# Ersetze fehlende Werte (falls ein Bezirk in einem Jahr fehlt) mit 0
gesamt_df.fillna(0, inplace=True)

# Berechne die Gesamtsumme der Straftaten über alle Jahre hinweg
gesamt_df['Straftaten_Gesamt'] = gesamt_df.sum(axis=1)

# Sortiere die Bezirke nach der Gesamtsumme der Straftaten in absteigender Reihenfolge
top10 = gesamt_df['Straftaten_Gesamt'].sort_values(ascending=False).head(10)

# Optional: Zurück in ein DataFrame für bessere Darstellung
top10_df = top10.reset_index()
top10_df.columns = ['Bezirksregion', 'Gesamt_Straftaten']

# Ausgabe der Top 10 Bezirke
print("Top 10 Unterbezirke mit den meisten Straftaten (2014-2023):")
print(top10_df)

# Optional: Speichern der Ergebnisse in eine neue Excel-Datei
# top10_df.to_excel('Top10_Unterbezirke_Straftaten_2014-2023.xlsx', index=False)