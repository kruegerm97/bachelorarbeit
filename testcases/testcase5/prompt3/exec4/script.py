import pandas as pd

# Schritt 1: Excel-Datei lesen und das Sheet 'Fallzahlen_2023' laden
datei_name = 'Fallzahlen&HZ 2014-2023.xlsx'
sheet_name = 'Fallzahlen_2023'

# Lese die Excel-Datei
try:
    df = pd.read_excel(datei_name, sheet_name=sheet_name)
    print(f"Sheet '{sheet_name}' erfolgreich geladen.")
except FileNotFoundError:
    print(f"Die Datei '{datei_name}' wurde nicht gefunden.")
    exit(1)
except ValueError:
    print(f"Das Sheet '{sheet_name}' existiert nicht in der Datei '{datei_name}'.")
    exit(1)

# Schritt 2: Daten in einem Pandas DataFrame speichern
# (Bereits durch pd.read_excel erledigt)

# Schritt 3: DataFrame auf notwendige Spalten reduzieren
notwendige_spalten = ['Bezeichnung (Bezirksregion)', 'Raub']
# Überprüfe, ob alle notwendigen Spalten vorhanden sind
fehlende_spalten = [spalte for spalte in notwendige_spalten if spalte not in df.columns]
if fehlende_spalten:
    print(f"Die folgenden benötigten Spalten fehlen im DataFrame: {fehlende_spalten}")
    exit(1)

df = df[notwendige_spalten]
print("DataFrame auf notwendige Spalten reduziert.")

# Schritt 4: Letzte zwei Zeilen entfernen (Gesamtwerte)
df = df.iloc[:-2].reset_index(drop=True)
print("Letzte zwei Zeilen (Gesamtwerte) entfernt.")

# Schritt 5: Oberbezirke identifizieren
oberbezirke = [
    'Mitte',
    'Friedrichshain-Kreuzberg',
    'Pankow',
    'Charlottenburg-Wilmersdorf',
    'Spandau',
    'Steglitz-Zehlendorf',
    'Tempelhof-Schöneberg',
    'Neukölln',
    'Treptow-Köpenick',
    'Marzahn-Hellersdorf',
    'Lichtenberg',
    'Reinickendorf'
]

# Füge eine neue Spalte 'Oberbezirk' hinzu, um jedem Unterbezirk den zugehörigen Oberbezirk zuzuweisen
df['Oberbezirk'] = None
current_oberbezirk = None

for idx, row in df.iterrows():
    bezirk = row['Bezeichnung (Bezirksregion)']
    if bezirk in oberbezirke:
        current_oberbezirk = bezirk
        df.at[idx, 'Oberbezirk'] = current_oberbezirk
    else:
        df.at[idx, 'Oberbezirk'] = current_oberbezirk

print("Oberbezirke zugewiesen.")

# Schritt 6: Oberbezirke von Unterbezirken trennen
# Annahme: Oberbezirke selbst sind keine Unterbezirke und sollten nicht berücksichtigt werden
df_unterbezirke = df[~df['Bezeichnung (Bezirksregion)'].isin(oberbezirke)].copy()
print("Unterbezirke von Oberbezirken getrennt.")

# Überprüfe, ob jedem Unterbezirk ein Oberbezirk zugewiesen wurde
if df_unterbezirke['Oberbezirk'].isnull().any():
    print("Warnung: Einige Unterbezirke haben keinen zugewiesenen Oberbezirk.")

# Schritt 7: Für jeden Oberbezirk den Unterbezirk mit dem höchsten 'Raub' identifizieren
# Zuerst stelle sicher, dass die 'Raub'-Spalte numerisch ist
df_unterbezirke['Raub'] = pd.to_numeric(df_unterbezirke['Raub'], errors='coerce')

# Entferne Zeilen mit fehlenden 'Raub'-Werten
df_unterbezirke = df_unterbezirke.dropna(subset=['Raub'])

# Gruppiere nach 'Oberbezirk' und finde den Unterbezirk mit dem maximalen 'Raub'
max_raub_unterbezirke = df_unterbezirke.loc[df_unterbezirke.groupby('Oberbezirk')['Raub'].idxmax()].reset_index(drop=True)

# Schritt 8: Ergebnis in einem neuen DataFrame speichern und formatieren
final_df = max_raub_unterbezirke[['Oberbezirk', 'Bezeichnung (Bezirksregion)', 'Raub']].rename(
    columns={
        'Bezeichnung (Bezirksregion)': 'Unterbezirk',
        'Raub': 'Raub'
    }
)

# Optional: Sortiere das finale DataFrame nach 'Oberbezirk' für bessere Übersichtlichkeit
final_df = final_df.sort_values(by='Oberbezirk').reset_index(drop=True)

# Schritt 9: Finale Ergebnisse anzeigen
print("\nUnterbezirke mit den höchsten 'Raub'-Werten je Oberbezirk:")
print(final_df)

# Optional: Speichere das Ergebnis in eine neue Excel-Datei
output_datei = 'Max_Raub_Unterbezirke_2023.xlsx'
final_df.to_excel(output_datei, index=False)
print(f"\nErgebnisse wurden in '{output_datei}' gespeichert.")