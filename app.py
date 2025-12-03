"""
main.py

Entry point for the Personal Finance Streamlit App.

This script sets up the application layout, configures page navigation, and
launches the selected page.

Features:
- Wide page layout configuration
"""

import streamlit as st

from src.core import PAGES_PATH

# ------------------------- PAGE DEFINITIONS -------------------------


def get_pages() -> list:
    """Define the pages for the Streamlit navigation.

    Returns:
        list: A list of Streamlit Page objects for navigation.
    """
    return [
        st.Page(f"{PAGES_PATH}/home.py", title="Home", icon=":material/home:"),
        st.Page(
            f"{PAGES_PATH}/dashboard.py", title="Dashboard", icon=":material/dashboard:"
        ),
        st.Page(f"{PAGES_PATH}/cashflow.py", title="Cashflow", icon=":material/table:"),
        st.Page(
            f"{PAGES_PATH}/upload_data.py",
            title="Upload Data",
            icon=":material/file_upload:",
        ),
    ]


# ------------------------- MAIN APP LAYOUT -------------------------


def app_layout() -> None:
    """Set up the Streamlit page configuration and run the selected page."""
    st.set_page_config(layout="wide", page_title="Personal Finance App")
    pages = st.navigation(get_pages())
    pages.run()


# ------------------------- ENTRY POINT -------------------------

if __name__ == "__main__":
    app_layout()
