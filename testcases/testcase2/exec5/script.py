import pandas as pd
from io import StringIO
import re

def find_header_row(df, keyword):
    """
    Find the header row in the DataFrame where the keyword is located.
    
    Parameters:
    - df: pandas DataFrame without headers
    - keyword: string to search for in the header
    
    Returns:
    - integer index of the header row or None if not found
    """
    for idx, row in df.iterrows():
        if row.astype(str).str.contains(keyword, case=False, na=False).any():
            return idx
    return None

def clean_column_names(columns):
    """
    Clean column names by removing newline characters and extra spaces.
    
    Parameters:
    - columns: pandas Index object containing column names
    
    Returns:
    - pandas Index object with cleaned column names
    """
    return columns.str.replace(r'\n', ' ', regex=True).str.strip()

def parse_crime_data(excel_file):
    """
    Parse crime data from the Excel file and identify the Bezirk with the most crimes.
    
    Parameters:
    - excel_file: string path to the Excel file
    
    Returns:
    - tuple containing the Bezirk with the most crimes and the total number of crimes
    """
    # Load the Excel file
    xls = pd.ExcelFile(excel_file)
    
    # Initialize a dictionary to accumulate total crimes per Bezirk
    total_crimes = {}
    
    # Iterate through each sheet in the Excel file
    for sheet_name in xls.sheet_names:
        # Process only sheets that follow the naming convention 'Fallzahlen_YYYY'
        if re.match(r'^Fallzahlen_\d{4}$', sheet_name):
            # Read the sheet without headers
            df_raw = pd.read_excel(xls, sheet_name, header=None)
            
            # Find the header row containing 'LOR-Schlüssel (Bezirksregion)'
            header_row = find_header_row(df_raw, 'LOR-Schlüssel (Bezirksregion)')
            
            if header_row is not None:
                # Read the sheet again using the identified header row
                df = pd.read_excel(
                    xls, 
                    sheet_name, 
                    header=header_row, 
                    thousands=',', 
                    dtype={'LOR-Schlüssel (Bezirksregion)': str}
                )
                
                # Clean the column names
                df.columns = clean_column_names(df.columns)
                
                # Ensure required columns are present
                required_columns = [
                    'Bezeichnung (Bezirksregion)', 
                    'Straftaten insgesamt'
                ]
                
                # Sometimes column names might have slight variations; adjust accordingly
                column_map = {}
                for col in df.columns:
                    if 'Bezeichnung' in col:
                        column_map[col] = 'Bezeichnung (Bezirksregion)'
                    elif 'Straftaten' in col and 'insgesamt' in col.lower():
                        column_map[col] = 'Straftaten insgesamt'
                
                df = df.rename(columns=column_map)
                
                if all(col in df.columns for col in required_columns):
                    # Select relevant columns
                    df_relevant = df[required_columns].copy()
                    
                    # Drop rows where 'Bezeichnung (Bezirksregion)' is NaN or empty
                    df_relevant = df_relevant.dropna(subset=['Bezeichnung (Bezirksregion)'])
                    df_relevant = df_relevant[df_relevant['Bezeichnung (Bezirksregion)'].str.strip() != '']
                    
                    # Ensure 'Straftaten insgesamt' is numeric
                    df_relevant['Straftaten insgesamt'] = pd.to_numeric(
                        df_relevant['Straftaten insgesamt'], errors='coerce'
                    ).fillna(0).astype(int)
                    
                    # Group by Bezirk and sum the crimes
                    df_sum = df_relevant.groupby('Bezeichnung (Bezirksregion)')['Straftaten insgesamt'].sum()
                    
                    # Accumulate the total crimes per Bezirk
                    for bezirk, crimes in df_sum.items():
                        if bezirk in total_crimes:
                            total_crimes[bezirk] += crimes
                        else:
                            total_crimes[bezirk] = crimes
                else:
                    print(f"Required columns not found in sheet '{sheet_name}'. Skipping this sheet.")
            else:
                print(f"Header row not found in sheet '{sheet_name}'. Skipping this sheet.")
    
    if total_crimes:
        # Convert the total_crimes dictionary to a pandas Series for easy manipulation
        total_crimes_series = pd.Series(total_crimes)
        
        # Identify the Bezirk with the maximum total crimes
        top_bezirk = total_crimes_series.idxmax()
        max_crimes = total_crimes_series.max()
        
        return top_bezirk, max_crimes
    else:
        return None, 0

if __name__ == "__main__":
    # Path to the Excel file
    excel_file = 'Fallzahlen&HZ2014-2023.xlsx'
    
    # Parse the crime data
    bezirk, crimes = parse_crime_data(excel_file)
    
    if bezirk:
        print(f"Der Bezirk mit den meisten Straftaten von allen Jahren kombiniert ist: {bezirk} mit {crimes} Straftaten.")
    else:
        print("Keine relevanten Daten gefunden.")