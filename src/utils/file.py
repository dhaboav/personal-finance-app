"""
file.py

This module contains utility functions for managing the financial dataset used in application.

Features:
- Check for the existence of the data file.
- Validate that a DataFrame has the required columns in the correct order.
- Load the dataset with caching, handling missing or empty files gracefully.
- Convert a DataFrame to CSV bytes suitable for download.
- Save a DataFrame to the project data path safely.
- Delete the data file and reset relevant Streamlit session state.
"""

import os

import pandas as pd
import streamlit as st

from src.core import DATA_PATH, REQUIRED_COLUMNS


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
    except FileNotFoundError:
        df = pd.DataFrame(columns=REQUIRED_COLUMNS)
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
