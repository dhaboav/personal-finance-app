"""
upload_data.py

This module provides a Streamlit-based interface for managing financial CSV data.
Users can either upload an existing CSV file or generate a template CSV with
predefined required columns. Uploaded or generated CSVs are saved to a defined
project path (`DATA_PATH`).

Features:
- CSV upload with column validation
- Template CSV generation
- Success/error feedback messages directly below actions
"""

from os.path import exists as file_path

import pandas as pd
import streamlit as st

from src.core import DATA_PATH, REQUIRED_COLUMNS

# ------------------------- UTILITY FUNCTIONS -------------------------


def validate_columns(df: pd.DataFrame) -> bool:
    """Validate if the DataFrame contains all required columns in order.

    Args:
        df (pd.DataFrame): The DataFrame to validate.

    Returns:
        bool: True if the DataFrame has the correct columns in the required order, False otherwise.
    """
    return list(df.columns[: len(REQUIRED_COLUMNS)]) == REQUIRED_COLUMNS


def save_data(df: pd.DataFrame) -> str:
    """Save a DataFrame to the project data path.

    Args:
        df (pd.DataFrame): The DataFrame to save.

    Returns:
        str: "Success" if saved successfully, "File already exists" if the file exists, or an error message if saving fails.
    """
    if file_path(DATA_PATH):
        return "File already exists"

    try:
        df.to_csv(DATA_PATH, index=False)
        return "Success"
    except Exception as e:
        return str(e)


# ------------------------- MAIN LAYOUT -------------------------


def upload_data_layout() -> None:
    """Render the main Streamlit layout for uploading or generating CSV files.

    Provides two main workflows:
        1. Upload an existing CSV file with validation.
        2. Generate a template CSV with required columns.
    """
    st.title("Upload or Generate Your Data")
    st.write("Upload your financial data CSV or generate a template CSV file.")

    # Initialize session state
    st.session_state.setdefault("view", None)

    # --- ACTION BUTTONS ---
    upload_btn, generate_btn = st.columns(2)

    if upload_btn.button(
        "Upload", icon=":material/upload_file:", use_container_width=True
    ):
        st.session_state.view = "upload"

    if generate_btn.button(
        "Generate Template CSV", icon=":material/docs_add_on:", use_container_width=True
    ):
        st.session_state.view = "generate"

    # Display selected workflow
    view = st.session_state.view
    if not view:
        return

    # --- WORKFLOW CONTAINER ---
    with st.container(border=True, key="data_container"):
        if view == "upload":
            render_upload_view()
        elif view == "generate":
            render_generate_view()


# ------------------------- VIEW RENDERERS -------------------------


def render_upload_view() -> None:
    """Render the upload workflow view.

    Allows the user to upload a CSV file, validates required columns, previews the
    data, and provides a button to save the file to DATA_PATH.
    """
    st.subheader("Upload Your CSV File")
    msg = st.empty()

    uploaded = st.file_uploader(
        f"Choose CSV file to upload",
        type=["csv"],
        key="upload_csv",
    )

    if not uploaded:
        msg.info(f"Please upload a CSV file (required columns: {REQUIRED_COLUMNS})")
        st.stop()

    # --- READ AND VALIDATE CSV ---
    try:
        df = pd.read_csv(uploaded)
    except Exception as e:
        msg.error(f"Error reading file: {e}")
        st.stop()

    if not validate_columns(df):
        msg.error(
            f"Invalid CSV format.\nExpected: {REQUIRED_COLUMNS}\nGot: {list(df.columns)}"
        )
        st.stop()

    # --- PREVIEW ---
    st.dataframe(df.head(5))

    # --- SAVE ---
    if st.button("Save", key="save_uploaded_csv"):
        result = save_data(df)
        if result == "Success":
            msg.success(f"File saved successfully at {DATA_PATH}")
        else:
            msg.error(f"Failed to save file: {result}")


def render_generate_view() -> None:
    """Render the template CSV generation view.

    Allows the user to generate a new CSV file with the required columns and save
    it to DATA_PATH.
    """
    st.subheader("Generate Template CSV")
    msg = st.empty()

    msg.info(
        f"Click 'Save' to generate a template CSV with columns: {REQUIRED_COLUMNS}"
    )

    if st.button("Save", key="generate_csv"):
        df = pd.DataFrame(columns=REQUIRED_COLUMNS)
        result = save_data(df)
        if result == "Success":
            msg.success(f"Template CSV generated successfully at {DATA_PATH}")
        else:
            msg.error(f"Failed to generate template CSV: {result}")


# ------------------------- ENTRY POINT -------------------------

if __name__ == "__main__":
    upload_data_layout()
