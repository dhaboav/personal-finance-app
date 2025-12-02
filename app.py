import streamlit as st

from src.core import PAGES_PATH


def app_layout():
    st.set_page_config(layout="wide")
    pages = st.navigation(
        [
            st.Page(f"{PAGES_PATH}/home.py", title="Home", icon=":material/home:"),
            st.Page(
                f"{PAGES_PATH}/dashboard.py",
                title="Dashboard",
                icon=":material/dashboard:",
            ),
            st.Page(
                f"{PAGES_PATH}/cashflow.py", title="Cashflow", icon=":material/table:"
            ),
            st.Page(
                f"{PAGES_PATH}/upload_data.py",
                title="Upload Data",
                icon=":material/file_upload:",
            ),
        ]
    )

    pages.run()


if __name__ == "__main__":
    app_layout()
