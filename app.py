import re
from pathlib import Path

import streamlit as st

from config import DEFAULT_EXPORT_DIR
from services.csv_processor import process_csv
from services.excel_exporter import export_to_excel
from services.filename_generator import generate_filename
from services.history_service import add_history_entry
from services.mail_sender import send_email

st.set_page_config(
    page_title="CSV → XLSX Mailer",
    layout="wide"
)

st.title("Génération et envoi du BH du jour")

st.sidebar.header("Configuration")

export_directory = st.sidebar.text_input(
    "Dossier d'export",
    value=str(DEFAULT_EXPORT_DIR)
)

export_directory = Path(export_directory)
export_directory.mkdir(exist_ok=True)

uploaded_file = st.file_uploader(
    "Choisir un fichier CSV",
    type=["csv"]
)

if uploaded_file is not None:

    # --- 1. EXTRACT AND REFORMAT THE DATE FROM FILENAME ---
    input_filename = uploaded_file.name  # e.g., "2026-05-21_exportOnSitePeople.csv"

    # Search for 4 digits, dash, 2 digits, dash, 2 digits
    date_match = re.search(r"(\d{4})-(\d{2})-(\d{2})", input_filename)

    if date_match:
        year, month, day = date_match.groups()
        output_filename = f"BH_{year}.{month}.{day}.xlsx"
    else:
        # Fallback filename if the date pattern is missing
        output_filename = "BH_export.xlsx"

    st.subheader("Prévisualisation du BH")

    df = process_csv(uploaded_file)

    st.dataframe(df, use_container_width=True)

    st.write(f"Nombre de personnes enregistrées : {len(df)}")

    generated_filename = generate_filename(
        prefix="rapport"
    )

    output_path = export_directory / output_filename

    export_to_excel(df, output_path)

    st.success(f"Fichier généré : {output_path.name}")

    with open(output_path, "rb") as f:
        st.download_button(
            label="Télécharger XLSX",
            data=f,
            file_name=output_path.name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    st.subheader("Envoi Email")

    recipient = st.text_input(
        "Destinataire",
        value="quentin.dorleat@gmail.com"
    )

    subject = st.text_input(
        "Sujet",
        value="Rapport automatique"
    )

    body = st.text_area(
        "Corps du message",
        value=(
            "Bonjour,\n\n"
            "Veuillez trouver le BH du jour pour la Maladaire en pièce jointe.\n\n"
            "Cordialement"
        )
    )

    if st.button("Envoyer le mail"):

        try:
            send_email(
                recipient=recipient,
                subject=subject,
                body=body,
                attachment_path=output_path
            )

            add_history_entry(
                recipient=recipient,
                subject=subject,
                file_path=output_path
            )

            st.success("Email envoyé avec succès")

        except Exception as e:
            st.error(f"Erreur : {e}")
