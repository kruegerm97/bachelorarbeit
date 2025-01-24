import pandas as pd

# Pfad zur CSV-Datei
csv_datei = 'FZ_2023.csv'

try:
    # Einlesen der CSV-Datei, Überspringen der ersten 4 Zeilen
    df = pd.read_csv(
        csv_datei,
        sep=',',
        skiprows=4,
        encoding='utf-8-sig'  # Unterstützt Umlaute und Sonderzeichen
    )
except FileNotFoundError:
    print(f"Die Datei {csv_datei} wurde nicht gefunden.")
    exit(1)

# Anzeige der ersten paar Zeilen zur Überprüfung
print("Erste 5 Zeilen der eingelesenen Daten:")
print(df.head())

# Benennung der relevanten Spalten
bezeichnung_col = 'Bezeichnung (Bezirksregion)'
straftaten_col = 'Straftaten insgesamt-'

# Überprüfen, ob die benötigten Spalten existieren
if bezeichnung_col not in df.columns or straftaten_col not in df.columns:
    print("Die erwarteten Spalten wurden in der CSV-Datei nicht gefunden.")
    exit(1)

# Bereinigen der 'Straftaten insgesamt-' Spalte
# Entfernen von Anführungszeichen und Tausendertrennungen
df[straftaten_col] = df[straftaten_col].astype(str).str.replace('"', '').str.replace(',', '').astype(int)

# Filtern der Bezirke:
# Ausschließen von Zeilen, die 'nicht zuzuordnen' oder Gesamtwerte enthalten
# Annahme: Bezirke mit bestimmten LOR-Schlüssel (z.B. '999999') sind Gesamt oder nicht zuzuordnen
# Alternativ kann nach dem Namen gefiltert werden
df_gefiltert = df[
    ~df[bezeichnung_col].str.contains('nicht zuzuordnen', case=False, na=False) &
    ~df[bezeichnung_col].str.contains('gesamt', case=False, na=False) &
    ~df[bezeichnung_col].str.contains('PKS gesamt', case=False, na=False)
]

# Sortieren nach 'Straftaten insgesamt-' in absteigender Reihenfolge
df_sortiert = df_gefiltert.sort_values(by=straftaten_col, ascending=False)

# Auswahl der gewünschten Spalten zur Anzeige
ergebnis = df_sortiert[[bezeichnung_col, straftaten_col]]

# Umbenennen der Spalten für bessere Lesbarkeit
ergebnis = ergebnis.rename(columns={
    bezeichnung_col: 'Bezirk',
    straftaten_col: 'Straftaten Insgesamt 2023'
})

# Anzeige des sortierten Ergebnisses
print("\nBezirke nach Gesamtzahl der Straftaten im Jahr 2023 (absteigend):")
print(ergebnis.to_string(index=False))