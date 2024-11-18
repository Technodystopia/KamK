"""
This module provides a pipeline for data ingestion, transformation, and filtering of HOPP and NES datasets. 
It includes functions to create folder structures, convert Excel files to CSV, transform data by cleaning and 
restructuring columns, combine and filter CSV files, and save the outputs in specified directories.

The main functions include:
    - create_folder_structure: Sets up the necessary folder structure for data storage.
    - converter: Converts specific Excel files to CSV, selecting specific sheets.
    - transformer_hopp1: Transforms and cleans HOPP data files for specific quarters.
    - combiner: Combines multiple CSV files into a single dataset.
    - transformer_hopp2: Transforms a separate HOPP dataset, performing additional cleaning and restructuring.
    - filter_hopp1 and filter_hopp2: Filter datasets by specific 'Yksikkökoodi' values for selected records.
    - transformer_nes: Transforms NES datasets by cleaning and restructuring columns.
    - filter_nes: Filters NES datasets by specific 'Yksikkökoodi' values for selected records.
    - nes_categorizer: Scrapes the source CSV for question data and saves the scraped data in a JSON file.

Usage:
    Run the script to execute the complete data pipeline, which prepares data for analysis and further processing.
"""

import pandas as pd
import os
import json

def create_folder_structure():
    """
    Creates the required folder structure for storing data files. 
    Folders are created under a base directory 'data' if they do not exist.
    """
    base_dir = "data"
    folders = [
        "json",
        "lake/staging/CSV/hopp/combined",
        "lake/staging/CSV/hopp/filtered",
        "lake/staging/CSV/hopp/raw",
        "lake/staging/CSV/hopp/transformed",
        "lake/staging/CSV/nes/raw",
        "lake/staging/CSV/nes/filtered",
        "lake/staging/CSV/nes/transformed",
        "warehouse"
    ]

    for folder in folders:
        path = os.path.join(base_dir, folder)
        os.makedirs(path, exist_ok=True)

def converter():
    """
    Converts specified Excel files to CSV format. 
    Reads data from predefined sheets within each Excel file and saves it as CSV files in the specified directories.
    """
    excel_files = [
        '../apina/data/lake/staging/HOPP/117_HOpp-Q2_2023.xlsx',
        '../apina/data/lake/staging/HOPP/117_HOpp-Q3_2023.xlsx',
        '../apina/data/lake/staging/HOPP/HoPP_Q1_Kaks_Tiedonkeruulomake_kansallinen_2022.xlsx',
        '../apina/data/lake/staging/HOPP/HoPP_Q3_KAKS_Tiedonkeruulomake_kansallinen_2022.xlsx',
        '../apina/data/lake/staging/HOPP/HoPP_Q4_KAKS_Tiedonkeruulomake_kansallinen_2022.xlsx',
        '../apina/data/lake/staging/HOPP/HoPP_Q32021_Q22023_kansallinen_kooste_2023_09_18_8.xlsx',
        '../apina/data/lake/staging/HOPP/Kainuu_HoPP_Tiedonkeruulomake_kansallinen__002___002__järjestyksessä.xlsx',
        '../apina/data/lake/staging/NES/Kopio_117_NESplus_2023.xlsx',
        '../apina/data/lake/staging/NES/NESplus_2024_Kainuu_Raakadata.xlsx',
        '../apina/data/lake/staging/NES/NESplus_Yksikkötyyppikohtaiset_summamuuttujien_kansalliset_keskiarvot_2023.xlsx',
        '../apina/data/lake/staging/NES/Kopio_117_NESplus_2023.xlsx'
    ]
    sheet_names = ['Taul1 (2)', 'Taul1 (2)', 'Aikuiset', 'Aikuiset', 'Aikuiset', '2023_09_18_kansallinen kooste 8', 'Aikuiset', 'Matriisi', 'Data', 'Kaikki vastaajat', 'Read-me']
    csv_files = [
        '../apina/data/lake/staging/CSV/hopp/raw/117_HOpp-Q2_2023.csv',
        '../apina/data/lake/staging/CSV/hopp/raw/117_HOpp-Q3_2023.csv',
        '../apina/data/lake/staging/CSV/hopp/raw/HoPP_Q1_Kaks_Tiedonkeruulomake_kansallinen_2022.csv',
        '../apina/data/lake/staging/CSV/hopp/raw/HoPP_Q3_KAKS_Tiedonkeruulomake_kansallinen_2022.csv',
        '../apina/data/lake/staging/CSV/hopp/raw/HoPP_Q4_KAKS_Tiedonkeruulomake_kansallinen_2022.csv',
        '../apina/data/lake/staging/CSV/hopp/raw/HoPP_Q32021_Q22023_kansallinen_kooste_2023_09_18_8.csv',
        '../apina/data/lake/staging/CSV/hopp/raw/Kainuu_HoPP_Tiedonkeruulomake_kansallinen__002___002__järjestyksessä.csv',
        '../apina/data/lake/staging/CSV/nes/raw/Kopio_117_NESplus_2023.csv',
        '../apina/data/lake/staging/CSV/nes/raw/NESplus_2024_Kainuu_Raakadata.csv',
        '../apina/data/lake/staging/CSV/nes/raw/NESplus_Yksikkötyyppikohtaiset_summamuuttujien_kansalliset_keskiarvot_2023.csv',
        '../apina/data/lake/staging/CSV/nes/raw/nes_questions_and_categories.csv'
    ]

    for i, (excel_file, sheet_name, csv_file) in enumerate(zip(excel_files, sheet_names, csv_files)):
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        if isinstance(df, dict):
            for sheet, data in df.items():
                data.to_csv(f"{csv_file}_{sheet}.csv", index=False)
        else:
            df.to_csv(csv_file, index=False)

def search_replace():
    """
    Searches and replaces a specific string in CSV files within a given directory.
    Iterates through all CSV files in the specified directory 
    and replaces the string "EAAIKLA50" with "EALAPSAIK" in each file. 
    The modified files are overwritten with the updated content.
    """

    path = "data/lake/staging/CSV/hopp/raw"
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        df = pd.read_csv(file_path)
        df = df.replace("EAAIKLA50", "EALAPSAIK", regex=True)
        df.to_csv(file_path, index=False)
    
def transformer_hopp1():
    """
    Transforms raw HOPP CSV files by cleaning and restructuring column data.
    Specific columns are removed based on file index, and headers are redefined.
    The cleaned data is saved as new CSV files in a transformed directory.
    """
    input_files = [
        './data/lake/staging/CSV/hopp/raw/117_HOpp-Q2_2023.csv',
        './data/lake/staging/CSV/hopp/raw/117_HOpp-Q3_2023.csv',
        './data/lake/staging/CSV/hopp/raw/HoPP_Q1_Kaks_Tiedonkeruulomake_kansallinen_2022.csv',
        './data/lake/staging/CSV/hopp/raw/HoPP_Q3_KAKS_Tiedonkeruulomake_kansallinen_2022.csv',
        './data/lake/staging/CSV/hopp/raw/HoPP_Q4_KAKS_Tiedonkeruulomake_kansallinen_2022.csv',
        './data/lake/staging/CSV/hopp/raw/Kainuu_HoPP_Tiedonkeruulomake_kansallinen__002___002__järjestyksessä.csv'
    ]

    output_files = [
        './data/lake/staging/CSV/hopp/transformed/Hopp_Q2_2023.csv',
        './data/lake/staging/CSV/hopp/transformed/Hopp_Q3_2023.csv',
        './data/lake/staging/CSV/hopp/transformed/Hopp_Q1_2022.csv',
        './data/lake/staging/CSV/hopp/transformed/Hopp_Q3_2022.csv',
        './data/lake/staging/CSV/hopp/transformed/Hopp_Q4_2022.csv',
        './data/lake/staging/CSV/hopp/transformed/Hopp_Q3_2021.csv'
    ]

    for i, input_file in enumerate(input_files):
        df = pd.read_csv(input_file)

        if i == 0 or i == 1:
            df.drop(df.columns[0], axis=1, inplace=True)
        elif i in [2, 3, 4]:
            df.drop(df.columns[[0, 1]], axis=1, inplace=True)
        elif i == 5:
            df.drop(df.columns[[0, 25]], axis=1, inplace=True)

        if i in [0, 1, 5]:
            df = df.iloc[3:]
        else:
            df = df.iloc[5:]

        new_header = ['Yksikkökoodi', 'kvartaali ja vuosi'] + list(range(1, 23))
        df.columns = new_header

        df.to_csv(output_files[i], index=False)

def combiner():
    """
    Combines multiple HOPP CSV files from the transformed directory into a single CSV file.
    The combined data is saved in the combined folder.
    """
    target = "./data/lake/staging/CSV/hopp/transformed"
    csv_files = ["Hopp_Q1_2022.csv", "Hopp_Q3_2021.csv", "Hopp_Q3_2022.csv", "Hopp_Q4_2022.csv", "Hopp_Q2_2023.csv", "Hopp_Q3_2023.csv"]
    csv_files = [os.path.join(target, file) for file in csv_files]
    combined_df = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)
    output_file = "./data/lake/staging/CSV/hopp/combined/Hopp_combined.csv"
    combined_df.to_csv(output_file, index=False)

def transformer_hopp2():
    """
    Transforms a separate HOPP dataset by dropping specific columns and renaming others.
    Converts date format in a specific column to 'Q_YYYY' and saves the output as a new CSV file.
    """
    input_csv_path = 'data/lake/staging/CSV/hopp/raw/HoPP_Q32021_Q22023_kansallinen_kooste_2023_09_18_8.csv'
    output_csv_path = 'data/lake/staging/CSV/hopp/transformed/Hopp_kooste.csv'
    df = pd.read_csv(input_csv_path)
    df.drop(df.columns[0], axis=1, inplace=True)
    df.rename(columns={df.columns[0]: 'kvartaali ja vuosi', df.columns[1]: 'Yksikkökoodi'}, inplace=True)
    df['kvartaali ja vuosi'] = df['kvartaali ja vuosi'].apply(lambda x: f"{str(x)[5]}_{str(x)[:4]}")
    df.to_csv(output_csv_path, index=False)

def filter_hopp1():
    """
    Filters combined HOPP data for specific unit codes and saves the filtered data as a new CSV file.
    """
    input_csv_path = 'data/lake/staging/CSV/hopp/combined/Hopp_combined.csv'
    output_csv_path = 'data/lake/staging/CSV/hopp/filtered/Hopp_combined_filtered.csv'
    df = pd.read_csv(input_csv_path)
    filter_values = ['AIKTEHOHO', 'EALAPSAIK', 'ENSIHOITO']
    filtered_df = df[df['Yksikkökoodi'].isin(filter_values)]
    filtered_df.to_csv(output_csv_path, index=False)

def filter_hopp2():
    """
    Filters transformed HOPP dataset for specific unit codes and saves the filtered data as a new CSV file.
    """
    input_csv_path = 'data/lake/staging/CSV/hopp/transformed/Hopp_kooste.csv'
    output_csv_path = 'data/lake/staging/CSV/hopp/filtered/Hopp_kooste_filtered.csv'
    df = pd.read_csv(input_csv_path)
    filter_values = ['AIKTEHOHO', 'EALAPSAIK', 'ENSIHOITO']
    filtered_df = df[df['Yksikkökoodi'].isin(filter_values)]
    filtered_df.to_csv(output_csv_path, index=False)

def transformer_nes():
    """
    Transforms NES source (raw CSV) data by dropping specific columns and renaming others.
    Saves the transformed data as a new CSV file.

    Processes both 2023 and 2024 NES datasets as well as the national averages of 2023
    """
    # 2024 NES dataset
    input_csv_path = 'data/lake/staging/CSV/nes/raw/NESplus_2024_Kainuu_Raakadata.csv'
    output_csv_path = 'data/lake/staging/CSV/nes/transformed/nes_2024_transformed.csv'
    df = pd.read_csv(input_csv_path)
    df.drop(df.columns[[0, 1, 4]], axis=1, inplace=True)
    df.rename(columns={df.columns[0]: 'Yksikkökoodi'}, inplace=True)
    df.to_csv(output_csv_path, index=False)
    # 2023 NES dataset (comparison data)
    input_csv_path2 = 'data/lake/staging/CSV/nes/raw/Kopio_117_NESplus_2023.csv'
    output_csv_path2 = 'data/lake/staging/CSV/nes/transformed/nes_2023_transformed.csv'
    df2 = pd.read_csv(input_csv_path2)
    df2.drop(df2.columns[0], axis=1, inplace=True)
    df2.rename(columns={df2.columns[0]: 'Yksikkökoodi'}, inplace=True)
    df2.to_csv(output_csv_path2, index=False)
    # 2023 NES national averages (comparison data)
    input_csv_path3 = 'data/lake/staging/CSV/nes/raw/NESplus_Yksikkötyyppikohtaiset_summamuuttujien_kansalliset_keskiarvot_2023.csv'
    output_csv_path3 = 'data/lake/staging/CSV/nes/transformed/nes_2023_national_avgs_transformed.csv'
    df3 = pd.read_csv(input_csv_path3)
    df3 = df3.drop(df3.iloc[0].name)
    df3.rename(columns={df3.columns[0]: 'Yksikkökoodi'}, inplace=True)
    df3.to_csv(output_csv_path3, index=False)

def filter_nes():
    """
    Filters NES source (raw CSV) data for specific unit codes and saves the filtered data as a new CSV file.

    Processes both 2023 and 2024 NES datasets as well as the national averages of 2023
    """
    # 2024 NES dataset
    input_csv_path = 'data/lake/staging/CSV/nes/transformed/nes_2024_transformed.csv'
    output_csv_path = 'data/lake/staging/CSV/nes/filtered/nes_2024_filtered.csv'
    df = pd.read_csv(input_csv_path)
    filter_values = ['AIKTEHOHO', 'EALAPSAIK', 'ENSIHOITO']
    filtered_df = df[df['Yksikkökoodi'].isin(filter_values)]
    filtered_df.to_csv(output_csv_path, index=False)
    # 2023 NES dataset (comparison data)
    input_csv_path2 = 'data/lake/staging/CSV/nes/transformed/nes_2023_transformed.csv'
    output_csv_path2 = 'data/lake/staging/CSV/nes/filtered/nes_2023_filtered.csv'
    df2 = pd.read_csv(input_csv_path2)
    filter_values2 = ['AIKTEHOHO', 'EALAPSAIK', 'ENSIHOITO']
    filtered_df2 = df2[df2['Yksikkökoodi'].isin(filter_values2)]
    filtered_df2.to_csv(output_csv_path2, index=False)
    # 2023 NES national averages (comparison data)
    input_csv_path3 = 'data/lake/staging/CSV/nes/transformed/nes_2023_national_avgs_transformed.csv'
    output_csv_path3 = 'data/lake/staging/CSV/nes/filtered/nes_2023_national_avgs_filtered.csv'
    df3 = pd.read_csv(input_csv_path3)
    filter_values3 = ['AIKTEHOHO', 'EALAPSAIK', 'ENSIHOITO']
    filtered_df3 = df3[df3['Yksikkökoodi'].isin(filter_values3)]
    filtered_df3.to_csv(output_csv_path3, index=False)

def nes_categorizer() -> None:
    """
    Scrapes the source CSV for:
        - short name (abbreviation) of the question
        - long name of the question
        - category of the question
        - adds numbering to the entries

    Saves the scraped data in a JSON file with the categories.
    """
    input_csv_path = 'data/lake/staging/CSV/nes/raw/nes_questions_and_categories.csv'
    output_csv_path = 'data/json/nes_questions_and_categories.json'
    #output_csv_path2 = 'data/lake/staging/CSV/nes/transformed/nes_variables.json'
    df = pd.read_csv(input_csv_path, encoding='utf-8')
    df1 = df.iloc[15:68].copy()
    df1.reset_index(drop=True, inplace=True)
    df1.drop(df1.columns[3], axis=1, inplace=True)
    df1.rename(columns={
        df1.columns[0]: 'long',
        df1.columns[1]: 'short',
        df1.columns[2]: 'category'
        }, inplace=True)
    df1['category'] = df1['category'].ffill()
    df1.reset_index(drop=True, inplace=True)
    json_data = [[i + 1] + list(row) for i, row in enumerate(df1.values)]
    json_str = json.dumps(json_data, indent=4, ensure_ascii=False)
    with open(output_csv_path, 'w', encoding='utf-8') as nes_category_file:
        nes_category_file.write(json_str)
    # df2 = df.iloc[73:] ## Tällä sais muuttujat
    # TODO: Joko haetaan muuttujat tällä tai sitten käytetään järkeä ja copypastetaan.


#    df = df.drop(df.rows[[0, 1, 2, 3, 4, 5, 6]], axis=1, inplace=True)
    return None

def main():
    """
    Runs the data processing pipeline, which includes folder creation, file conversion, data transformation, 
    combination, and filtering.
    """
    create_folder_structure()
    converter()
    search_replace()
    transformer_hopp1()
    combiner()
    transformer_hopp2()
    filter_hopp1()
    filter_hopp2()
    transformer_nes()
    filter_nes()
    nes_categorizer()

if __name__ == "__main__":
    main()
