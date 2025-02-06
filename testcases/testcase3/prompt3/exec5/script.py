import pandas as pd

def berechne_prozentanteile(dateipfad: str, sheet_name: str = 'Fallzahlen_2023') -> pd.DataFrame:
    """
    Liest eine Excel-Datei ein, überprüft notwendige Spalten, berechnet den prozentualen Anteil
    der Straftaten pro Bezirk und gibt das Ergebnis als DataFrame zurück.

    :param dateipfad: Pfad zur Excel-Datei (z.B. 'Fallzahlen.xlsx')
    :param sheet_name: Name des Sheets in der Excel-Datei (Standard: 'Fallzahlen_2023')
    :return: DataFrame mit Bezirken und deren prozentualem Anteil an den Straftaten
    """
    # 1. Excel-Datei einlesen
    try:
        df = pd.read_excel(dateipfad, sheet_name=sheet_name)
        print(f"Excel-Datei '{dateipfad}' erfolgreich eingelesen.")
    except FileNotFoundError:
        print(f"Fehler: Die Datei '{dateipfad}' wurde nicht gefunden.")
        return
    except Exception as e:
        print(f"Ein Fehler ist beim Einlesen der Excel-Datei aufgetreten: {e}")
        return

    # 2. DataFrame speichern (bereits durch pd.read_excel erledigt)

    # 3. Überprüfen, ob die notwendigen Spalten vorhanden sind
    notwendige_spalten = {'Bezirke', 'Straftaten_insgesamt'}
    vorhandene_spalten = set(df.columns)

    fehlende_spalten = notwendige_spalten - vorhandene_spalten
    if fehlende_spalten:
        print(f"Fehler: Die folgenden notwendigen Spalten fehlen in der Tabelle: {fehlende_spalten}")
        return
    else:
        print("Überprüfung der notwendigen Spalten erfolgreich.")

    # 4. Gesamtzahl der Straftaten für ganz Berlin finden
    gesamt_row = df[df['Bezirke'] == 'Berlin (PKS gesamt)']
    if gesamt_row.empty:
        print("Fehler: Keine Zeile mit 'Bezirke' als 'Berlin (PKS gesamt)' gefunden.")
        return

    gesamt_straftaten = gesamt_row['Straftaten_insgesamt'].iloc[0]
    print(f"Gesamtzahl der Straftaten in Berlin: {gesamt_straftaten}")

    # 5. Prozentualen Anteil der einzelnen Bezirke berechnen
    # Ausschließen der Gesamtzeile aus den Bezirken
    bezirke_df = df[df['Bezirke'] != 'Berlin (PKS gesamt)'].copy()

    # Berechnung des prozentualen Anteils
    bezirke_df['Prozentualer_Anteil'] = (bezirke_df['Straftaten_insgesamt'] / gesamt_straftaten) * 100

    # Optional: Auf zwei Dezimalstellen runden
    bezirke_df['Prozentualer_Anteil'] = bezirke_df['Prozentualer_Anteil'].round(2)

    # 6. Ergebnis als DataFrame zurückgeben
    ergebnis_df = bezirke_df[['Bezirke', 'Straftaten_insgesamt', 'Prozentualer_Anteil']]

    return ergebnis_df

# Beispielhafte Nutzung des Skripts
if __name__ == "__main__":
    dateipfad = 'Fallzahlen.xlsx'  # Pfad zur Excel-Datei
    ergebnis = berechne_prozentanteile(dateipfad)

    if ergebnis is not None:
        print("\nProzentuale Anteile der Straftaten pro Bezirk:")
        print(ergebnis)

        # Optional: Ergebnis in eine neue Excel-Datei speichern
        # ergebnis.to_excel('Prozentuale_Anteile_Straftaten.xlsx', index=False)