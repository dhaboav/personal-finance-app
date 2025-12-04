"""
cashflow.py

This module implements the CashFlow page of the financial dashboard. It provides
an overview of income, expenses, and savings, with options to filter transactions
by month, display them in a table, and add new data.

The page uses Streamlit for UI, pandas for data manipulation, and integrates
with the core data storage defined in `DATA_PATH`. It is designed to be modular,
scalable, and easy to maintain.
"""

import os

import pandas as pd
import streamlit as st

from src.core import DATA_PATH
from src.types import MONTH_MAP, MONTH_OPTIONS
from src.utils.file import get_data


# ------------------------- UTILITY FUNCTIONS -------------------------
def load_cashflow_data() -> pd.DataFrame:
    """
    Load the cashflow data from CSV file, converting the 'Date' column to datetime.

    Returns:
        pd.DataFrame: DataFrame containing cashflow transactions.
    """

    file_mod_time = os.path.getmtime(DATA_PATH) if os.path.exists(DATA_PATH) else 0
    df = get_data(file_mod_time)
    df["Date"] = pd.to_datetime(df["Date"], yearfirst=True)

    return df


def filter_by_month(df: pd.DataFrame, month_jap: str) -> pd.DataFrame:
    """
    Filter the DataFrame by the selected Japanese month.

    Args:
        df (pd.DataFrame): Original DataFrame with 'Date' column.
        month_jap (str): Japanese month string from MONTH_OPTIONS (e.g., "1月", "全て").

    Returns:
        pd.DataFrame: Filtered DataFrame.
    """

    month_num = MONTH_MAP.get(month_jap, 0)
    if month_num == 0:
        return df.copy()

    return df[df["Date"].map(lambda x: x.month) == month_num]


# ------------------------- RENDERERS -------------------------


def cashflow_layout() -> None:
    """Render the CashFlow page with filters, table display, and add-data button."""

    st.title("CashFlow")
    st.write(
        "This section provides an overview of your cash flow. Analyze your income and expenses over time."
    )
    st.write("\n" * 2)

    with st.container(border=True):
        add_btn, month_filter_btn = st.columns([10, 1], vertical_alignment="bottom")

        # Add data button
        add_btn.button("Add Data", icon=":material/add_2:")

        df = load_cashflow_data()
        month_filter = month_filter_btn.selectbox(
            "Month Filter",
            options=MONTH_OPTIONS,
            index=0,
            placeholder="Month filter",
        )

        filtered_df = filter_by_month(df, month_filter)
        column_config = {
            "Date": st.column_config.DatetimeColumn("Date", format="Y年M月D日"),
            "Total": st.column_config.NumberColumn("Total (Rp)", format="accounting"),
        }

        st.dataframe(filtered_df, column_config=column_config)


if __name__ == "__main__":
    cashflow_layout()
