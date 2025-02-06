import pandas as pd

# Pfad zur Excel-Datei
excel_datei = 'Fallzahlen.xlsx'

# Lade alle Sheets in ein Dictionary
alle_sheets = pd.read_excel(excel_datei, sheet_name=None)

# Liste zur Speicherung der jährlichen Straftaten
jahrliche_straftaten = []

for sheet_name, df in alle_sheets.items():
    try:
        # Versuche, das Jahr aus dem Sheetnamen zu extrahieren
        jahr = int(sheet_name)
    except ValueError:
        # Wenn der Sheetname kein Jahr ist, überspringe dieses Sheet
        print(f"Sheet '{sheet_name}' übersprungen (kein gültiges Jahr).")
        continue
    
    # Finde die Zeile für 'Berlin (PKS gesamt)'
    berlin_gesamt = df[df['Bezirke'] == 'Berlin (PKS gesamt)']
    
    if nicht berlin_gesamt.empty:
        # Extrahiere die Gesamtzahl der Straftaten
        gesamt_straftaten = berlin_gesamt['Straftaten_insgesamt'].values[0]
        jahrliche_straftaten.append({'Jahr': jahr, 'Straftaten_insgesamt': gesamt_straftaten})
    else:
        print(f"Keine Daten für 'Berlin (PKS gesamt)' in Sheet '{sheet_name}' gefunden.")

# Erstelle einen DataFrame aus den gesammelten Daten
df_jahrlich = pd.DataFrame(jahrliche_straftaten)

# Sortiere den DataFrame nach Jahr
df_jahrlich = df_jahrlich.sort_values('Jahr').reset_index(drop=True)

# Berechne die prozentuale Veränderung zum Vorjahr
df_jahrlich['Veränderung_prozent'] = df_jahrlich['Straftaten_insgesamt'].pct_change() * 100

# Runde die Veränderungen auf zwei Dezimalstellen
df_jahrlich['Veränderung_prozent'] = df_jahrlich['Veränderung_prozent'].round(2)

# Anzeige des resultierenden DataFrames
print(df_jahrlich)