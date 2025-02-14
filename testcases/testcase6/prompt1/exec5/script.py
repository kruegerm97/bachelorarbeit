import pandas as pd

# Pfad zur Excel-Datei
excel_datei = 'Fallzahlen&HZ 2014-2023.xlsx'

# Liste der relevanten Sheet-Namen
jahre = list(range(2014, 2024))  # 2014 bis 2023
sheet_namen = [f'Fallzahlen_{jahr}' for jahr in jahre]

# Initialisiere ein leeres DataFrame zur Aggregation
aggregate_df = pd.DataFrame()

# Iteriere über jedes Sheet und aggregiere die Daten
for sheet in sheet_namen:
    try:
        # Lese das aktuelle Sheet
        df = pd.read_excel(excel_datei, sheet_name=sheet)
        
        # Überprüfe, ob die notwendigen Spalten vorhanden sind
        if 'Bezeichnung (Bezirksregion)' in df.columns and 'Straftaten -insgesamt-' in df.columns:
            # Wähle die relevanten Spalten aus
            temp_df = df[['Bezeichnung (Bezirksregion)', 'Straftaten -insgesamt-']].copy()
            
            # Gruppiere nach Bezirksregion und summiere die Straftaten
            temp_agg = temp_df.groupby('Bezeichnung (Bezirksregion)', as_index=False)['Straftaten -insgesamt-'].sum()
            
            # Füge die aggregierten Daten zum Gesamt-DataFrame hinzu
            aggregate_df = pd.concat([aggregate_df, temp_agg], ignore_index=True)
        else:
            print(f"Warnung: Die erforderlichen Spalten sind im Sheet '{sheet}' nicht vorhanden.")
    except Exception as e:
        print(f"Fehler beim Verarbeiten des Sheets '{sheet}': {e}")

# Überprüfe, ob Daten aggregiert wurden
if aggregate_df.empty:
    print("Keine Daten zum Aggregieren gefunden.")
else:
    # Gruppiere erneut nach Bezirksregion, um die Gesamtstraftaten über alle Jahre zu berechnen
    gesamt_agg = aggregate_df.groupby('Bezeichnung (Bezirksregion)', as_index=False)['Straftaten -insgesamt-'].sum()
    
    # Sortiere die Bezirke nach den meisten Straftaten
    top_10 = gesamt_agg.sort_values(by='Straftaten -insgesamt-', ascending=False).head(10)
    
    # Ausgabe der Top 10 Unterbezirke
    print("Top 10 Unterbezirke mit den meisten Straftaten insgesamt (2014-2023):")
    print(top_10.to_string(index=False))
    
    # Optional: Speichern der Ergebnisse in einer CSV-Datei
    top_10.to_csv('Top_10_Unterbezirke_Straftaten_2014-2023.csv', index=False)
    print("\nDie Ergebnisse wurden in 'Top_10_Unterbezirke_Straftaten_2014-2023.csv' gespeichert.")