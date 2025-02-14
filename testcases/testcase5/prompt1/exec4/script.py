import pandas as pd

def finde_oberbezirke_mit_meisten_raub(excel_datei, sheet_name):
    # Excel-Datei lesen
    try:
        df = pd.read_excel(excel_datei, sheet_name=sheet_name, dtype={'LOR-Schlüssel': str})
    except Exception as e:
        print(f"Fehler beim Lesen der Excel-Datei: {e}")
        return
    
    # Sicherstellen, dass 'LOR-Schlüssel' als String gelesen werden und führende Nullen beibehalten
    df['LOR-Schlüssel'] = df['LOR-Schlüssel'].str.strip().str.zfill(6)
    
    # Entfernen von nicht zuzuordenenden Bezirken
    df = df[~df['Bezeichnung (Bezirksregion)'].str.contains('nicht zuzuordnen', na=False)]
    
    # Identifizieren der Oberbezirke: 5-stelliger LOR-Schlüssel, der mit '000' endet
    oberbezke = df[df['LOR-Schlüssel'].str.endswith('000') & (df['LOR-Schlüssel'].str.len() == 5)]
    
    if oberbezke.empty:
        print("Keine Oberbezirke gefunden. Überprüfen Sie die Kriterien zur Identifikation der Oberbezirke.")
        return
    
    # Liste der Oberbezirke
    oberbezke_list = oberbezke[['LOR-Schlüssel', 'Bezeichnung (Bezirksregion)']].to_dict('records')
    
    # Ergebnisse speichern
    ergebnisse = []
    
    for ober in oberbezke_list:
        ober_code = ober['LOR-Schlüssel']
        ober_name = ober['Bezeichnung (Bezirksregion)']
        
        # Finden der Unterbezirke, die mit dem Oberbezirkscode beginnen
        # Annahme: Der Oberbezirkscode ohne die letzten drei Nullen ist der Präfix
        prefix = ober_code[:-3]  # z.B. '10' aus '10000'
        
        # Unterbezirke finden
        unterbezke = df[
            (df['LOR-Schlüssel'].str.startswith(prefix)) &
            (df['LOR-Schlüssel'] != ober_code)
        ]
        
        if unterbezke.empty:
            print(f"Keine Unterbezirke für Oberbezirk {ober_name} gefunden.")
            continue
        
        # Unterbezirk mit den meisten Raubdelikten finden
        max_raub_idx = unterbezke['Raub'].idxmax()
        max_raub = unterbezke.loc[max_raub_idx]
        unterbez_name = max_raub['Bezeichnung (Bezirksregion)']
        raub_count = max_raub['Raub']
        
        ergebnisse.append({
            'Oberbezirk': ober_name,
            'Unterbezirk': unterbez_name,
            'Raubdelikte': raub_count
        })
    
    # Ergebnisse anzeigen
    print("Unterbezirke mit den meisten Raubdelikten pro Oberbezirk:")
    for res in ergebnisse:
        print(f"Oberbezirk: {res['Oberbezirk']}, "
              f"Unterbezirk: {res['Unterbezirk']}, "
              f"Raubdelikte: {res['Raubdelikte']}")

if __name__ == "__main__":
    excel_datei = 'Fallzahlen&HZ 2014-2023.xlsx'  # Pfad zur Excel-Datei
    sheet_name = 'Fallzahlen_2023'               # Name des Sheets
    finde_oberbezirke_mit_meisten_raub(excel_datei, sheet_name)