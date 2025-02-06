import pandas as pd

# Pfad zur Excel-Datei
excel_file = 'Fallzahlen.xlsx'

# Lese alle Sheets in der Excel-Datei
# sheet_name=None lädt alle Sheets und gibt ein Dictionary zurück
sheets_dict = pd.read_excel(excel_file, sheet_name=None)

# Liste zur Speicherung der jährlichen Gesamtstraftaten
data = []

# Iteriere über alle Sheets
for sheet_name, df in sheets_dict.items():
    # Überprüfe, ob 'LOR-Schlüssel' und 'Straftaten_insgesamt' in den Spalten vorhanden sind
    if 'LOR-Schlüssel' in df.columns and 'Straftaten_insgesamt' in df.columns:
        # Suche die Zeile, die die Gesamtzahl für Berlin enthält
        # Annahme: 'LOR-Schlüssel' 999999 oder 'Berlin (PKS gesamt)' repräsentiert die Gesamtdaten
        total_row = df[df['LOR-Schlüssel'] == 999999]
        
        # Falls nicht gefunden, versuche mit dem Namen
        if total_row.empty:
            total_row = df[df['LOR-Schlüssel'].astype(str).str.contains('Berlin \(PKS gesamt\)', regex=True)]
        
        # Falls immer noch nicht gefunden, überspringe das Sheet
        if total_row.empty:
            print(f"Warnung: Gesamtdaten nicht in Sheet '{sheet_name}' gefunden.")
            continue
        
        # Extrahiere das Jahr aus dem Sheet-Namen
        # Annahme: Der Sheet-Name enthält das Jahr, z.B. "2020", "Jahr 2020", etc.
        # Hier wird versucht, eine vierstellige Zahl zu extrahieren
        import re
        match = re.search(r'\b(19|20)\d{2}\b', sheet_name)
        if match:
            year = int(match.group())
        else:
            print(f"Warnung: Jahr konnte nicht aus dem Sheet-Namen '{sheet_name}' extrahiert werden. Überspringe dieses Sheet.")
            continue
        
        # Extrahiere die Gesamtzahl der Straftaten
        total_crimes = total_row['Straftaten_insgesamt'].values[0]
        
        # Füge die Daten zur Liste hinzu
        data.append({'Jahr': year, 'Straftaten_insgesamt': total_crimes})
    else:
        print(f"Warnung: Erforderliche Spalten nicht in Sheet '{sheet_name}' vorhanden.")

# Erstelle einen DataFrame aus den gesammelten Daten
df_total = pd.DataFrame(data)

# Sortiere den DataFrame nach dem Jahr
df_total = df_total.sort_values('Jahr').reset_index(drop=True)

# Berechne die prozentuale Veränderung zum Vorjahr
df_total['Prozentuale_Veraenderung_zum_Vorjahr (%)'] = df_total['Straftaten_insgesamt'].pct_change() * 100

# Optional: Rundung der prozentualen Veränderung auf zwei Dezimalstellen
df_total['Prozentuale_Veraenderung_zum_Vorjahr (%)'] = df_total['Prozentuale_Veraenderung_zum_Vorjahr (%)'].round(2)

# Setze das Jahr als Index (optional)
df_total.set_index('Jahr', inplace=True)

# Anzeige des Ergebnis-DataFrames
print(df_total)

# Optional: Speichere das Ergebnis in eine neue Excel-Datei
df_total.to_excel('Zeitreihe_Straftaten_Berlin.xlsx')