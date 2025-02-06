import pandas as pd

def berechne_prozentualer_anteil_straftaten():
    try:
        # Excel-Datei laden
        dateipfad = 'Fallzahlen.xlsx'  # Pfad zur Excel-Datei
        sheet_name = 'Fallzahlen_2023'  # Name des Sheets
        
        df = pd.read_excel(dateipfad, sheet_name=sheet_name)
        
        # Überprüfen, ob die benötigten Spalten vorhanden sind
        erforderliche_spalten = ['Bezirke', 'Straftaten_insgesamt']
        fehlende_spalten = [spalte for spalte in erforderliche_spalten if spalte not in df.columns]
        if fehlende_spalten:
            raise ValueError(f"Die folgenden benötigten Spalten fehlen im Excel-Sheet: {fehlende_spalten}")
        
        # Gesamte Straftaten aus der Gesamtzeile holen
        gesamt_row = df[df['Bezirke'] == 'Berlin (PKS gesamt)']
        if not gesamt_row.empty:
            gesamt_straftaten = gesamt_row['Straftaten_insgesamt'].iloc[0]
            print(f"Gesamte Straftaten in Berlin: {gesamt_straftaten}")
        else:
            # Falls die Gesamtzeile nicht vorhanden ist, summiere alle Bezirkswerte
            gesamt_straftaten = df[~df['Bezirke'].isin(['Stadtgebiet Berlin, nicht zuzuordnen'])]['Straftaten_insgesamt'].sum()
            print(f"Gesamte Straftaten in Berlin (berechnet): {gesamt_straftaten}")
        
        # Bezirke ausschließen, die nicht zugeordnet werden können oder die Gesamtzeile sind
        bezirke_df = df[~df['Bezirke'].isin(['Berlin (PKS gesamt)', 'Stadtgebiet Berlin, nicht zuzuordnen'])]
        
        # Prozentualen Anteil berechnen
        bezirke_df = bezirke_df.copy()  # Kopie erstellen, um SettingWithCopyWarning zu vermeiden
        bezirke_df['Prozentualer_Anteil (%)'] = (bezirke_df['Straftaten_insgesamt'] / gesamt_straftaten) * 100
        
        # Prozentualen Anteil auf 2 Dezimalstellen runden
        bezirke_df['Prozentualer_Anteil (%)'] = bezirke_df['Prozentualer_Anteil (%)'].round(2)
        
        # Ergebnis anzeigen
        print("\nProzentualer Anteil der Straftaten pro Bezirk:")
        print(bezirke_df[['Bezirke', 'Straftaten_insgesamt', 'Prozentualer_Anteil (%)']])
        
        # Optional: Ergebnis in eine neue Excel-Datei speichern
        ausgabe_datei = 'Straftaten_Prozentual.xlsx'
        bezirke_df[['Bezirke', 'Straftaten_insgesamt', 'Prozentualer_Anteil (%)']].to_excel(ausgabe_datei, index=False)
        print(f"\nDas Ergebnis wurde in '{ausgabe_datei}' gespeichert.")
        
    except FileNotFoundError:
        print("Fehler: Die Datei 'Fallzahlen.xlsx' wurde nicht gefunden. Bitte überprüfe den Dateipfad.")
    except ValueError as ve:
        print(f"Fehler: {ve}")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

if __name__ == "__main__":
    berechne_prozentualer_anteil_straftaten()