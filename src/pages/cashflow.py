"""
cashflow.py

CashFlow page of the financial dashboard.

This module provides an overview of income, expenses, and savings.
It supports adding transactions, filtering by month, and displaying
data in a table. Designed for efficiency, modularity, and future-proofing.
"""

import os
from typing import List, Optional

import pandas as pd
import streamlit as st

from src.core import DATA_PATH, REQUIRED_COLUMNS
from src.types import MONTH_MAP, MONTH_OPTIONS, Categories, Labels
from src.utils.file import get_data

# ------------------------- DATA MANAGEMENT ------------------------- #


def load_cashflow_data() -> pd.DataFrame:
    """Load cashflow CSV data and convert the 'Date' column to datetime.

    Returns:
        pd.DataFrame: Cashflow data with datetime-converted 'Date'.
    """
    file_mod_time = os.path.getmtime(DATA_PATH) if os.path.exists(DATA_PATH) else 0
    df = get_data(file_mod_time)
    df["Date"] = pd.to_datetime(df["Date"], yearfirst=True)

    return df


def filter_by_month(df: pd.DataFrame, month_jap: str) -> pd.DataFrame:
    """Filter DataFrame by Japanese month string.

    Args:
        df (pd.DataFrame): Cashflow DataFrame.
        month_jap (str): Japanese month string.

    Returns:
        pd.DataFrame: Filtered DataFrame containing only rows from the specified month.
    """
    month_num = MONTH_MAP.get(month_jap, 0)
    if month_num == 0:
        return df.copy()

    return df[df["Date"].map(lambda x: x.month) == month_num]


def add_new_row(
    date: pd.Timestamp,
    desc: str,
    label: Optional[str],
    category: Optional[str],
    total: Optional[int],
) -> None:
    """Add a new row to the cashflow DataFrame and update session state.

    Args:
        date (pd.Timestamp): Transaction date.
        desc (str): Transaction description.
        label (str): Transaction label.
        category (str): Transaction category.
        total (int): Transaction total amount.
    """
    df = st.session_state.cashflow_df

    # Construct new row dynamically using REQUIRED_COLUMNS
    new_row = pd.DataFrame(
        [dict(zip(REQUIRED_COLUMNS, [date, desc, label, category, total]))]
    )

    # Efficient append without excessive copying
    st.session_state.cashflow_df = pd.concat([df, new_row], ignore_index=True)

    # Persist changes to disk
    st.session_state.cashflow_df.to_csv(DATA_PATH, index=False)


# ------------------------- FORM MANAGEMENT ------------------------- #


def validate_form_inputs(
    desc: str, label: Optional[str], category: Optional[str], total: Optional[int]
) -> List[str]:
    """Validate form inputs and return missing fields.

    Args:
        desc (str): Transaction description.
        label (str): Transaction label.
        category (str): Transaction category.
        total (int): Transaction total.

    Returns:
        List[str]: List of missing or invalid field names.
    """
    missing_fields = []
    if not desc.strip():
        missing_fields.append("Description")
    if label is None:
        missing_fields.append("Label")
    if category is None:
        missing_fields.append("Category")
    if total is None or total <= 0:
        missing_fields.append("Total")

    return missing_fields


def _render_add_form(msg) -> None:
    """Render the Add Transaction form with validation and Save/Close actions.

    Args:
        msg (st.delta_generator.DeltaGenerator): Streamlit placeholder for messages.
    """
    with st.form("data_form"):
        st.write("Add a new transaction")

        date_input = st.date_input("Date")
        desc_input = st.text_input("Description", placeholder="Enter description")
        label_input = st.selectbox(
            "Label",
            options=[x.name for x in Labels],
            index=None,
            placeholder="Select a label",
        )
        category_input = st.selectbox(
            "Category",
            options=[x.name for x in Categories],
            index=None,
            placeholder="Select a category",
        )
        total_input = st.number_input(
            "Total",
            min_value=0,
            step=1,
            format="%d",
            value=None,
            placeholder="Enter total",
        )

        col1, col2 = st.columns([1, 16])
        save_clicked = col1.form_submit_button("Save")
        close_clicked = col2.form_submit_button("Close")

        if save_clicked:
            missing_fields = validate_form_inputs(
                desc_input, label_input, category_input, total_input
            )
            if missing_fields:
                msg.error(
                    f"Please fill in the following fields: {', '.join(missing_fields)}"
                )
            else:
                add_new_row(
                    pd.Timestamp(date_input),
                    desc_input,
                    label_input,
                    category_input,
                    total_input,
                )
                msg.success("Transaction added successfully!")

        if close_clicked:
            st.session_state["form"] = None
            st.rerun()


def render_form_panel(msg) -> None:
    """Render the form panel if session state indicates 'add' mode.

    Args:
        msg (st.delta_generator.DeltaGenerator): Streamlit placeholder for messages.
    """
    if st.session_state.get("form") == "add":
        _render_add_form(msg)


# ------------------------- TABLE RENDERING ------------------------- #


def render_table() -> None:
    """Render the CashFlow table with month filter and Add Data button."""
    with st.container():
        add_btn_col, month_filter_col = st.columns([10, 1], vertical_alignment="bottom")

        if add_btn_col.button("Add Data", icon=":material/add_2:"):
            st.session_state["form"] = "add"
            st.rerun()

        df = st.session_state.cashflow_df

        # Month filter
        month_filter = month_filter_col.selectbox(
            "Month Filter", options=MONTH_OPTIONS, index=0
        )
        filtered_df = filter_by_month(df, month_filter)

        # Column config for formatting
        column_config = {
            "Date": st.column_config.DatetimeColumn("Date", format="Y年M月D日"),
            "Total": st.column_config.NumberColumn("Total (Rp)", format="accounting"),
        }

        st.dataframe(filtered_df, column_config=column_config)


# ------------------------- PAGE LAYOUT ------------------------- #


def cashflow_layout() -> None:
    """Main layout for CashFlow page."""
    st.title("CashFlow Dashboard")
    st.write(
        "Overview of income, expenses, and savings. Filter transactions by month and add new data."
    )

    # Initialize session state
    if "cashflow_df" not in st.session_state:
        st.session_state.cashflow_df = load_cashflow_data()
    st.session_state.setdefault("form", None)

    msg = st.empty()  # Placeholder for messages

    render_form_panel(msg)
    render_table()


# ------------------------- RUN ------------------------- #

if __name__ == "__main__":
    cashflow_layout()
