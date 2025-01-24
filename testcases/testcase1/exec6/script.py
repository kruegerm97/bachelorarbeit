import pandas as pd

def main():
    # Pfad zur CSV-Datei
    csv_file = 'FZ_2023.csv'

    try:
        # Einlesen der CSV-Datei, Überspringen der ersten 4 Zeilen, die keine relevanten Daten enthalten
        df = pd.read_csv(
            csv_file,
            sep=',',
            skiprows=4,
            encoding='utf-8',
            dtype=str
        )

        # Umbenennen der Spalten für einfacheren Zugriff (falls notwendig)
        df.columns = [
            'LOR-Schlüssel',
            'Bezeichnung',
            'Straftaten_insgesamt',
            'Raub',
            'Strassenraub_Handtaschenraub',
            'Koerperverletzungen_insgesamt',
            'Gefaehrliche_schwere_Koerperverletzung',
            'Freiheitsberaubung_Noetigung_Bedrohnung_Nachstellung',
            'Diebstahl_insgesamt',
            'Diebstahl_von_Kraftwagen',
            'Diebstahl_an_aus_Kfz',
            'Fahrraddiebstahl',
            'Wohnraumeinbruch',
            'Branddelikte_insgesamt',
            'Brandstiftung',
            'Sachbeschadigung_insgesamt',
            'Sachbeschadigung_durch_Graffiti',
            'Rauschgiftdelikte',
            'Kieztaten'
        ]

        # Funktion zur Umwandlung von Zahlenstrings in Integer
        def convert_to_int(x):
            if isinstance(x, str):
                # Entfernen von Anführungszeichen und Kommas
                return int(x.replace('"', '').replace(',', ''))
            return 0  # Standardwert, falls der Eintrag kein String ist

        # Anwenden der Umwandlungsfunktion auf die relevante Spalte
        df['Straftaten_insgesamt'] = df['Straftaten_insgesamt'].apply(convert_to_int)

        # Filterung der Bezirke: Ausschluss der Einträge, die nicht zugeordnet sind (z.B. LOR-Schlüssel endet mit '900' oder '999')
        df_filtered = df[~df['LOR-Schlüssel'].str.endswith(('900', '999'))].copy()

        # Sortierung der Bezirke nach der Gesamtzahl der Straftaten absteigend
        df_sorted = df_filtered.sort_values(by='Straftaten_insgesamt', ascending=False)

        # Anzeige der sortierten Bezirke
        print(df_sorted[['Bezeichnung', 'Straftaten_insgesamt']])

        # Optional: Speichern der sortierten Daten in einer neuen CSV-Datei
        df_sorted[['Bezeichnung', 'Straftaten_insgesamt']].to_csv('sortierte_straftaten.csv', index=False, encoding='utf-8')
        print("\nDie sortierten Daten wurden in 'sortierte_straftaten.csv' gespeichert.")

    except FileNotFoundError:
        print(f"Die Datei '{csv_file}' wurde nicht gefunden. Bitte überprüfen Sie den Pfad.")
    except Exception as e:
        print(f"Es ist ein Fehler aufgetreten: {e}")

if __name__ == "__main__":
    main()