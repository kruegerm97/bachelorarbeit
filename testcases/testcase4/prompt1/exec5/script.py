import pandas as pd

# Pfad zur Excel-Datei
excel_file = 'Fallzahlen.xlsx'

# Excel-Datei laden
xls = pd.ExcelFile(excel_file)

# Liste zur Speicherung der jährlichen Gesamtdaten
jahresdaten = []

# Annahme: Die Sheet-Namen entsprechen den Jahreszahlen (z.B. '2018', '2019', ...)
for sheet in xls.sheet_names:
    # Daten des aktuellen Sheets lesen
    df = pd.read_excel(xls, sheet_name=sheet)
    
    # Sicherstellen, dass die 'LOR-Schlüssel' Spalte als String behandelt wird
    df['LOR-Schlüssel'] = df['LOR-Schlüssel'].astype(str)
    
    # Filtern nach der Zeile für ganz Berlin (angenommen '999999' ist der Schlüssel)
    berlin_gesamt = df[df['LOR-Schlüssel'] == '999999']
    
    if not berlin_gesamt.empty:
        # Gesamtzahl der Straftaten für Berlin aus der entsprechenden Zeile
        straftaten = berlin_gesamt['Straftaten_insgesamt'].values[0]
    else:
        # Wenn die 'Berlin (PKS gesamt)' Zeile nicht vorhanden ist, summiere alle Bezirke
        straftaten = df['Straftaten_insgesamt'].sum()
    
    # Füge die Daten zur Liste hinzu
    jahresdaten.append({'Jahr': sheet, 'Straftaten_insgesamt': straftaten})

# Erstelle einen DataFrame aus den gesammelten Daten
df_gesamt = pd.DataFrame(jahresdaten)

# Versuche, die 'Jahr' Spalte in Integer zu konvertieren für die Sortierung
try:
    df_gesamt['Jahr'] = df_gesamt['Jahr'].astype(int)
    df_gesamt = df_gesamt.sort_values('Jahr')
except ValueError:
    # Falls die Sheet-Namen nicht numerisch sind, sortiere alphabetisch
    df_gesamt = df_gesamt.sort_values('Jahr')

# Setze das Jahr als Index
df_gesamt.set_index('Jahr', inplace=True)

# Berechne die prozentuale Veränderung zum Vorjahr
df_gesamt['% Veränderung Vorjahr'] = df_gesamt['Straftaten_insgesamt'].pct_change() * 100

# Runde die Prozentwerte auf zwei Dezimalstellen
df_gesamt['% Veränderung Vorjahr'] = df_gesamt['% Veränderung Vorjahr'].round(2)

# Anzeige des resultierenden DataFrames
print(df_gesamt)

# Optional: Speichern des DataFrames in eine neue Excel-Datei
df_gesamt.to_excel('Prozentuale_Veraenderung_Straftaten_Berlin.xlsx')