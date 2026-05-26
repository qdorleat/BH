from datetime import datetime

import pandas as pd
import streamlit as st

def process_csv(uploaded_file):
    # 1. SAFELY LOCATE THE HEADER ROW INDEX DYNAMICALLY
    uploaded_file.seek(0)
    header_row_index = None

    for idx, line in enumerate(uploaded_file):
        # Decode bytes and remove newline characters (\n, \r) from the edges
        line_str = line.decode("ISO-8859-1", errors="ignore").strip()

        # Remove quote marks (") to avoid matching issues with wrapped text
        line_str = line_str.replace('"', "")

        # Split the clean row string by the semicolon separator
        columns_in_line = [col.strip() for col in line_str.split(";")]

        # Match the exact string 'Séjour' now that quotes and newlines are gone
        if "Séjour" in columns_in_line:
            header_row_index = idx
            break

    # Fallback safety: if the keyword is missing, default to row index 0
    if header_row_index is None:
        st.error(
            "Could not find the 'Séjour' column header. Please check your file structure."
        )
        header_row_index = 0

    # 2. READ THE FILE STREAM WITH PANDAS
    uploaded_file.seek(0)

    # Define the exact list of expected columns to pull
    target_columns = [
        "Séjour",
        "Nom",
        "Prénom",
        "Date de naissance",
        "Arrivée",
        "Départ",
    ]

    df = pd.read_csv(uploaded_file,
                     header=header_row_index-1,
                     sep=';',
                     usecols=target_columns,
                     encoding='ISO-8859-1')

    # 1. Remove the last 2 rows
    df = df.iloc[:-2]

    # 2. Remove row if it's a duplicate (keeps the first occurrence) (filter by firstname, name and date of birth)
    df = df.drop_duplicates(subset=[df.columns[1], df.columns[2], df.columns[3]], keep="first")

    # Get today's date formatted as DD/MM/YYYY
    today_str = datetime.now().strftime("%d/%m/%Y")

    # 3. Keep only rows where 'Arriv�e' matches today's date
    df_filtered = df[df["Arriv�e"] == today_str]

    # 3. Rename the first column and overwrite all its row values
    df_filtered = df_filtered.rename(columns={df_filtered.columns[0]: "Etablissement"})
    df_filtered["Etablissement"] = "La Maladaire"

    return df_filtered
