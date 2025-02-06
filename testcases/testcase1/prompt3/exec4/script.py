import pandas as pd

def sort_fallzahlen_excel(file_path: str, sheet_name: str) -> pd.DataFrame:
    """
    Reads the specified sheet from an Excel file, sorts the data by 'Straftaten_insgesamt' 
    in descending order excluding rows with LOR-Schlüssel 999900 and 999999, which are 
    appended at the end.

    Parameters:
    - file_path: Path to the Excel file.
    - sheet_name: Name of the sheet to read.

    Returns:
    - A sorted pandas DataFrame.
    """
    try:
        # Read the Excel sheet
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        print(f"Successfully read the sheet '{sheet_name}' from '{file_path}'.")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return pd.DataFrame()
    except ValueError:
        print(f"Error: The sheet '{sheet_name}' does not exist in '{file_path}'.")
        return pd.DataFrame()
    except Exception as e:
        print(f"An unexpected error occurred while reading the Excel file: {e}")
        return pd.DataFrame()

    # Check if necessary columns exist
    required_columns = ['LOR-Schlüssel', 'Straftaten_insgesamt']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"Error: The following required columns are missing from the data: {missing_columns}")
        return pd.DataFrame()

    # Separate the rows with LOR-Schlüssel 999900 and 999999
    exclusion_keys = [999900, 999999]
    excluded_df = df[df['LOR-Schlüssel'].isin(exclusion_keys)]
    included_df = df[~df['LOR-Schlüssel'].isin(exclusion_keys)]

    if excluded_df.empty:
        print("Warning: No rows found with LOR-Schlüssel 999900 or 999999.")

    # Sort the included DataFrame by 'Straftaten_insgesamt' in descending order
    try:
        included_sorted_df = included_df.sort_values(by='Straftaten_insgesamt', ascending=False)
        print("Successfully sorted the included data by 'Straftaten_insgesamt' in descending order.")
    except KeyError:
        print("Error: The column 'Straftaten_insgesamt' does not exist in the data.")
        return pd.DataFrame()
    except Exception as e:
        print(f"An unexpected error occurred during sorting: {e}")
        return pd.DataFrame()

    # Concatenate the sorted included data with the excluded data
    sorted_df = pd.concat([included_sorted_df, excluded_df], ignore_index=True)
    print("Successfully concatenated the excluded rows at the end of the sorted data.")

    return sorted_df

if __name__ == "__main__":
    # Define the Excel file path and sheet name
    excel_file = 'Fallzahlen.xlsx'
    sheet = 'Fallzahlen_2023'

    # Get the sorted DataFrame
    sorted_fallzahlen_df = sort_fallzahlen_excel(excel_file, sheet)

    # Check if the DataFrame is not empty before proceeding
    if not sorted_fallzahlen_df.empty:
        print("Sorted DataFrame:")
        print(sorted_fallzahlen_df)
        # Optionally, you can save the sorted DataFrame to a new Excel file or another format
        # sorted_fallzahlen_df.to_excel('Sorted_Fallzahlen.xlsx', index=False)
    else:
        print("No data to display due to previous errors.")