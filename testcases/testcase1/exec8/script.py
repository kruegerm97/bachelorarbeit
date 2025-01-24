import pandas as pd
import matplotlib.pyplot as plt

# Dateiname der CSV-Datei
csv_datei = 'FZ_2023.csv'

# Anzahl der Zeilen, die zu Beginn übersprungen werden müssen
# Basierend auf den bereitgestellten Daten, scheint es 4 initiale Zeilen zu geben
skip_rows = 4

try:
    # Lesen der CSV-Datei mit pandas
    df = pd.read_csv(csv_datei, delimiter=',', encoding='utf-8', skiprows=skip_rows)
except FileNotFoundError:
    print(f"Die Datei {csv_datei} wurde nicht gefunden. Bitte stellen Sie sicher, dass sich die Datei im selben Verzeichnis wie dieses Skript befindet.")
    exit(1)
except pd.errors.ParserError as e:
    print(f"Fehler beim Parsen der CSV-Datei: {e}")
    exit(1)

# Anzeigen der Spalten zur Überprüfung
print("Spalten in der CSV-Datei:")
print(df.columns)

# Überprüfen, ob die notwendigen Spalten vorhanden sind
benoetigte_spalten = ['Bezeichnung (Bezirksregion)', 'Straftaten \n    -insgesamt-']
for spalte in benoetigte_spalten:
    if spalte not in df.columns:
        print(f"Die benötigte Spalte '{spalte}' wurde nicht gefunden. Bitte überprüfen Sie die CSV-Datei.")
        exit(1)

# Umbenennen der Spalten für einfacheren Zugriff
df.rename(columns={
    'Bezeichnung (Bezirksregion)': 'Bezirk',
    'Straftaten \n    -insgesamt-': 'Straftaten_insgesamt'
}, inplace=True)

# Entfernen von Anführungszeichen und Kommas, Umwandlung in Ganzzahlen
df['Straftaten_insgesamt'] = df['Straftaten_insgesamt'].astype(str).str.replace('"', '').str.replace(',', '').astype(int)

# Sortieren der Bezirke nach der Anzahl der Straftaten (absteigend)
df_sortiert = df.sort_values(by='Straftaten_insgesamt', ascending=False)

# Zur besseren Übersicht nur relevante Spalten anzeigen
df_sortiert_relevant = df_sortiert[['Bezirk', 'Straftaten_insgesamt']]

# Ausgabe der sortierten Tabelle
print("\nBezirke sortiert nach der Anzahl der insgesamt begangenen Straftaten (absteigend):")
print(df_sortiert_relevant.to_string(index=False))

# Optional: Visualisierung der Daten
plt.figure(figsize=(12, 8))
plt.barh(df_sortiert_relevant['Bezirk'], df_sortiert_relevant['Straftaten_insgesamt'], color='skyblue')
plt.xlabel('Anzahl der Straftaten insgesamt')
plt.title('Straftaten nach Bezirken in Berlin (2023)')
plt.gca().invert_yaxis()  # Bezirke mit den meisten Straftaten oben anzeigen
plt.tight_layout()
plt.show()