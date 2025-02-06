import pandas as pd

def berechne_prozentuale_anteile(dateipfad: str, sheet_name: str = 'Fallzahlen_2023'):
    """
    Berechnet den prozentualen Anteil der Straftaten jedes Bezirks an den gesamten Straftaten in Berlin.

    :param dateipfad: Pfad zur Excel-Datei 'Fallzahlen.xlsx'.
    :param sheet_name: Name des Sheets in der Excel-Datei. Standard ist 'Fallzahlen_2023'.
    :return: DataFrame mit Bezirken und deren prozentualen Anteilen.
    """
    try:
        # Excel-Datei lesen
        df = pd.read_excel(dateipfad, sheet_name=sheet_name)
    except FileNotFoundError:
        print(f"Die Datei {dateipfad} wurde nicht gefunden.")
        return
    except Exception as e:
        print(f"Ein Fehler ist beim Lesen der Excel-Datei aufgetreten: {e}")
        return

    # Gesamtstraftaten für Berlin abrufen
    total_crimes_row = df[df['Bezirke'] == 'Berlin (PKS gesamt)']
    if not total_crimes_row.empty:
        total_crimes = total_crimes_row['Straftaten_insgesamt'].values[0]
    else:
        # Falls 'Berlin (PKS gesamt)' nicht vorhanden ist, summiere die Bezirke
        exclude_bezirke = ['Berlin (PKS gesamt)', 'Stadtgebiet Berlin, nicht zuzuordnen']
        total_crimes = df.loc[~df['Bezirke'].isin(exclude_bezirke), 'Straftaten_insgesamt'].sum()

    # Bezirke filtern (ausschließen: Gesamtdaten und nicht zuordenbare Gebiete)
    exclude_bezirke = ['Berlin (PKS gesamt)', 'Stadtgebiet Berlin, nicht zuzuordnen']
    bezirke_df = df.loc[~df['Bezirke'].isin(exclude_bezirke)].copy()

    # Prozentualen Anteil berechnen
    bezirke_df['Prozentualer_Anteil'] = (bezirke_df['Straftaten_insgesamt'] / total_crimes) * 100

    # Optional: Auf zwei Dezimalstellen runden
    bezirke_df['Prozentualer_Anteil'] = bezirke_df['Prozentualer_Anteil'].round(2)

    # Ergebnis anzeigen
    print("Prozentualer Anteil der Straftaten nach Bezirk:")
    print(bezirke_df[['Bezirke', 'Straftaten_insgesamt', 'Prozentualer_Anteil']])

    # Optional: Ergebnis in eine neue Excel-Datei speichern
    output_datei = 'Prozentuale_Anteile_Straftaten.xlsx'
    try:
        bezirke_df[['Bezirke', 'Straftaten_insgesamt', 'Prozentualer_Anteil']].to_excel(output_datei, index=False)
        print(f"\nDie Ergebnisse wurden in '{output_datei}' gespeichert.")
    except Exception as e:
        print(f"Ein Fehler ist beim Speichern der Ergebnisdatei aufgetreten: {e}")

if __name__ == "__main__":
    # Pfad zur Excel-Datei
    dateipfad = 'Fallzahlen.xlsx'
    
    # Prozentuale Anteile berechnen
    berechne_prozentuale_anteile(dateipfad)