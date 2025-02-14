import pandas as pd

# Pfad zur Excel-Datei
excel_file = 'Fallzahlen&HZ 2014-2023.xlsx'

# Liste der relevanten Sheet-Namen
sheet_names = [f'Fallzahlen_{jahr}' for jahr in range(2014, 2024)]

# Initialisiere ein leeres DataFrame zur Speicherung aller Daten
all_data = pd.DataFrame()

# Iteriere über alle relevanten Sheets und füge die Daten hinzu
for sheet in sheet_names:
    try:
        # Lese das aktuelle Sheet
        df = pd.read_excel(excel_file, sheet_name=sheet)
        
        # Überprüfe, ob die notwendigen Spalten vorhanden sind
        if 'Bezeichnung (Bezirksregion)' in df.columns and 'Straftaten \n-insgesamt-' in df.columns:
            # Wähle nur die relevanten Spalten
            df_subset = df[['Bezeichnung (Bezirksregion)', 'Straftaten \n-insgesamt-']]
            
            # Entferne mögliche NaN-Werte und stelle sicher, dass 'Straftaten \n-insgesamt-' numerisch ist
            df_subset = df_subset.dropna(subset=['Straftaten \n-insgesamt-'])
            df_subset['Straftaten \n-insgesamt-'] = pd.to_numeric(df_subset['Straftaten \n-insgesamt-'], errors='coerce').fillna(0)
            
            # Füge die Daten zum all_data DataFrame hinzu
            all_data = pd.concat([all_data, df_subset], ignore_index=True)
        else:
            print(f"Warnung: Die notwendigen Spalten sind im Sheet '{sheet}' nicht vorhanden.")
    except Exception as e:
        print(f"Fehler beim Verarbeiten des Sheets '{sheet}': {e}")

# Gruppiere die Daten nach Unterbezirk und summiere die Straftaten
total_straftaten = all_data.groupby('Bezeichnung (Bezirksregion)')['Straftaten \n-insgesamt-'].sum()

# Sortiere die Unterbezirke nach den meisten Straftaten
top_10_unterbezirke = total_straftaten.sort_values(ascending=False).head(10)

# Ausgabe der Ergebnisse
print("Die Top 10 Unterbezirke mit den meisten Straftaten (2014-2023):")
print(top_10_unterbezirke)