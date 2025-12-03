"""
database.py

This module provides a Streamlit-based interface for managing financial CSV data.
Users can either upload an existing CSV file or generate a template CSV with
predefined required columns. Uploaded or generated CSVs are saved to a defined
project path (`DATA_PATH`).

Features:
- CSV upload with column validation
- Generate template CSV with required columns
- Auto-update session state when data is uploaded/created
- Success/error feedback messages directly below actions
"""

import os

import pandas as pd
import streamlit as st

from src.core import DATA_PATH, REQUIRED_COLUMNS

# ------------------------- UTILITY FUNCTIONS -------------------------


def file_exists() -> bool:
    """Return True if the data file exists."""

    return os.path.exists(DATA_PATH)


def validate_columns(df: pd.DataFrame) -> bool:
    """Validate if the DataFrame contains all required columns in order.

    Args:
        df (pd.DataFrame): The DataFrame to validate.

    Returns:
        bool: True if the DataFrame has the correct columns in the required order, False otherwise.
    """

    return list(df.columns[: len(REQUIRED_COLUMNS)]) == REQUIRED_COLUMNS


@st.cache_data
def get_data(file_mod_time: float) -> pd.DataFrame:
    """
    Load the financial dataset from DATA_PATH.

    Args:
        file_mod_time (float): Timestamp of the CSV file to invalidate cache on changes.

    Returns:
        pd.DataFrame: Cached DataFrame with the CSV content.
        Returns an empty DataFrame if the file does not exist or is empty.
    """

    try:
        df = pd.read_csv(DATA_PATH)
    except pd.errors.EmptyDataError:
        df = pd.DataFrame()  # empty
    return df


@st.cache_data
def convert_for_download(df):
    """Convert a DataFrame to CSV bytes for download."""

    return df.to_csv(index=False).encode("utf-8")


def save_data(df: pd.DataFrame) -> str:
    """Save a DataFrame to the project data path.

    Args:
        df (pd.DataFrame): The DataFrame to save.

    Returns:
        str: "Success" if saved successfully, "File already exists" if the file exists, or an error message if saving fails.
    """

    if file_exists():
        return "File already exists"
    try:
        df.to_csv(DATA_PATH, index=False)
        return "Success"
    except Exception as e:
        return str(e)


def delete_data() -> None:
    """Delete the current data file and reset session state."""

    try:
        os.remove(DATA_PATH)
        st.session_state["data_file"] = False
        st.session_state["view"] = None
        st.success("Data deleted successfully.")
        st.rerun()
    except Exception as e:
        st.error(f"Error deleting file: {e}")


# ------------------------- STATUS RENDERERS -------------------------


def render_status_panel() -> None:
    """Display current data status with compact buttons side by side."""

    st.subheader("Current Data Status")

    col_logo, col_info = st.columns([1, 5])
    with col_logo:
        st.image("public/docs.svg", width=180)

    with col_info:
        if st.session_state.get("data_file"):
            _render_file_available()
        else:
            _render_no_data()


def _render_file_available() -> None:
    """Render status panel when a data file exists."""

    st.success("✔ Data Available")
    st.caption("Your financial dataset is stored and ready to use.")

    delete_btn, download_btn, _ = st.columns([2, 8, 8])
    if delete_btn.button("Delete", icon=":material/delete:"):
        delete_data()

    with download_btn:
        file_mod_time = os.path.getmtime(DATA_PATH) if os.path.exists(DATA_PATH) else 0
        df = get_data(file_mod_time)
        csv_data = convert_for_download(df)
        st.download_button(
            label="Download",
            data=csv_data,
            file_name="finance.csv",
            mime="text/csv",
            icon=":material/download:",
        )


def _render_no_data() -> None:
    """Render status panel when no data file exists."""

    st.error("⚠ No Data Available")
    st.caption("Upload a CSV file or generate a blank template first.")

    upload_btn, generate_btn, _ = st.columns([3, 8, 8])
    if upload_btn.button("Upload Data", icon=":material/upload_file:"):
        st.session_state.view = "upload"

    if generate_btn.button("Generate Template", icon=":material/docs_add_on:"):
        st.session_state.view = "generate"


# ------------------------- VIEW RENDERERS -------------------------


def render_view_panel() -> None:
    """Render upload or generate workflow panel based on the session state."""

    view = st.session_state.get("view")
    if view == "upload":
        _render_upload_view()

    elif view == "generate":
        _render_generate_view()


def _render_upload_view() -> None:
    """Render the upload workflow view.

    Allows the user to upload a CSV file, validates required columns, previews the
    data, and provides a button to save the file to DATA_PATH.
    """

    st.subheader("Upload Your CSV File")
    msg = st.empty()

    uploaded = st.file_uploader(
        "Choose CSV file to upload", type=["csv"], key="upload_csv"
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
    if st.button("Save", key="save_uploaded"):
        result = save_data(df)
        if result == "Success":
            msg.success(f"File saved successfully at {DATA_PATH}")
            st.session_state["data_file"] = True
            st.session_state["view"] = None
            st.rerun()
        else:
            msg.error(f"Failed to save: {result}")


def _render_generate_view() -> None:
    """Render the template CSV generation view.

    Allows the user to generate a new CSV file with the required columns and save
    it to DATA_PATH.
    """

    st.subheader("Generate Template CSV")
    msg = st.empty()
    msg.info(
        f"Click 'Save' to generate a template CSV with columns: {REQUIRED_COLUMNS}"
    )

    if st.button("Save", key="generate_template"):
        df = pd.DataFrame(columns=REQUIRED_COLUMNS)
        result = save_data(df)
        if result == "Success":
            msg.success(f"Template CSV generated at {DATA_PATH}")
            st.session_state["data_file"] = True
            st.session_state["view"] = None
            st.rerun()
        else:
            msg.error(f"Failed to generate: {result}")


# ------------------------- ENTRY POINT -------------------------


def database_management_layout() -> None:
    """Main layout for the Data Management page."""

    st.title("Database Management")
    st.write("Manage your financial data CSV.")

    st.session_state.setdefault("view", None)
    st.session_state["data_file"] = file_exists()

    render_status_panel()

    if not st.session_state["data_file"]:
        render_view_panel()


if __name__ == "__main__":
    database_management_layout()
