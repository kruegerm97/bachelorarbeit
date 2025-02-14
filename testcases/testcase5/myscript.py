import pandas as pd

# read excel
df = pd.read_excel("Fallzahlen&HZ 2014-2023.xlsx", sheet_name="Fallzahlen_2023", usecols=["Bezeichnung (Bezirksregion)", "Raub"])

# remove last two rows
df = df.iloc[:-2]

# list Oberbezirke
oberbezirke = {
    "Mitte", "Friedrichshain-Kreuzberg", "Pankow", "Charlottenburg-Wilmersdorf", 
    "Spandau", "Steglitz-Zehlendorf", "Tempelhof-Schöneberg", "Neukölln", 
    "Treptow-Köpenick", "Marzahn-Hellersdorf", "Lichtenberg", "Reinickendorf"
}

# put oberbezirk in oberbezirk column
df["Oberbezirk"] = df["Bezeichnung (Bezirksregion)"].where(df["Bezeichnung (Bezirksregion)"].isin(oberbezirke)).ffill()

# keep only unterbezirke
df = df[~df["Bezeichnung (Bezirksregion)"].isin(oberbezirke)].copy()

# convert Raub to numeric
df["Raub"] = pd.to_numeric(df["Raub"], errors="coerce")

# get top raub unterbezirke
top_raub_unterbezirke = df.loc[df.groupby("Oberbezirk")["Raub"].idxmax(), ["Oberbezirk", "Bezeichnung (Bezirksregion)", "Raub"]]

# rename columns
top_raub_unterbezirke.rename(columns={"Bezeichnung (Bezirksregion)": "Unterbezirk"}, inplace=True)

print(top_raub_unterbezirke)