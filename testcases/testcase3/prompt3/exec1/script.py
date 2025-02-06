import pandas as pd

def main():
    # 1. Excel-Datei einlesen
    excel_datei = 'Fallzahlen.xlsx'
    sheet_name = 'Fallzahlen_2023'
    
    try:
        df = pd.read_excel(excel_datei, sheet_name=sheet_name)
        print(f"Excel-Datei '{excel_datei}' erfolgreich eingelesen.")
    except FileNotFoundError:
        print(f"Fehler: Die Datei '{excel_datei}' wurde nicht gefunden.")
        return
    except Exception as e:
        print(f"Ein Fehler ist beim Einlesen der Excel-Datei aufgetreten: {e}")
        return

    # 2. Tabelle als Pandas DataFrame speichern
    # (bereits durch das Einlesen mit pandas erledigt)
    
    # 3. Überprüfen, ob die notwendigen Spalten vorhanden sind
    erforderliche_spalten = ['Bezirke', 'Straftaten_insgesamt']
    fehlende_spalten = [spalte for spalte in erforderliche_spalten if spalte not in df.columns]
    
    if fehlende_spalten:
        print(f"Fehler: Fehlende Spalten in der Excel-Datei: {fehlende_spalten}")
        return
    else:
        print("Alle erforderlichen Spalten sind vorhanden.")

    # 4. Gesamtzahl der Straftaten für ganz Berlin finden
    gesamt_row = df[df['Bezirke'] == 'Berlin (PKS gesamt)']
    
    if gesamt_row.empty:
        print("Fehler: Die Zeile mit 'Berlin (PKS gesamt)' wurde nicht gefunden.")
        return
    
    gesamt_straftaten = gesamt_row['Straftaten_insgesamt'].values[0]
    print(f"Gesamtzahl der Straftaten für Berlin: {gesamt_straftaten}")

    # 5. Prozentualen Anteil der einzelnen Bezirke berechnen
    # Ausschließen der Gesamtzeile für die Berechnung
    df_bezirke = df[df['Bezirke'] != 'Berlin (PKS gesamt)'].copy()
    
    if df_bezirke.empty:
        print("Fehler: Es gibt keine Bezirke nach dem Ausschluss von 'Berlin (PKS gesamt)'.")
        return
    
    # Prozentualer Anteil berechnen
    df_bezirke['Prozentualer_Anteil (%)'] = (df_bezirke['Straftaten_insgesamt'] / gesamt_straftaten) * 100

    # Optional: Runden auf zwei Dezimalstellen
    df_bezirke['Prozentualer_Anteil (%)'] = df_bezirke['Prozentualer_Anteil (%)'].round(2)
    
    print("Prozentualer Anteil der Straftaten pro Bezirk berechnet.")

    # 6. Ergebnis als DataFrame zurückgeben
    # Hier zeigen wir das Ergebnis an. Sie können es auch in eine Datei speichern.
    ergebnis_df = df_bezirke[['Bezirke', 'Straftaten_insgesamt', 'Prozentualer_Anteil (%)']]
    print("\nErgebnis DataFrame:")
    print(ergebnis_df.to_string(index=False))

    # Optional: Ergebnis in eine neue Excel-Datei speichern
    ausgabe_datei = 'Fallzahlen_prozentual.xlsx'
    try:
        ergebnis_df.to_excel(ausgabe_datei, index=False)
        print(f"\nErgebnis erfolgreich in '{ausgabe_datei}' gespeichert.")
    except Exception as e:
        print(f"Ein Fehler ist beim Speichern der Ergebnisdatei aufgetreten: {e}")

if __name__ == "__main__":
    main()