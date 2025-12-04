"""
months.py

Provides month enumerations and mappings.

This module defines English month enums for logic/filtering and
Japanese month display names for UI. It also provides helper
mappings for Streamlit selectbox options.

Classes:
    Months: English month enumeration with numeric values.
    MonthsJap: Dictionary mapping English month names to Japanese display names.

Constants:
    MONTH_MAP: Maps Japanese month names to numeric values for filtering.
    MONTH_OPTIONS: Ordered list of Japanese month names for Streamlit selectbox.
"""

from enum import Enum


class Months(Enum):
    """English months with numeric values for filtering.

    Args:
        All (int): Represents all months (value 0).
        January - December (int): Numeric values corresponding to each month.
    """

    All = 0
    January = 1
    February = 2
    March = 3
    April = 4
    May = 5
    June = 6
    July = 7
    August = 8
    September = 9
    October = 10
    November = 11
    December = 12


MonthsJap = {month.name: f"{month.value}月" for month in Months if month != Months.All}

all_month = {"All": "全て"}
MonthsJap = {**all_month, **MonthsJap}

MONTH_MAP = {jap: Months[name].value for name, jap in MonthsJap.items()}
MONTH_MAP["全て"] = 0

MONTH_OPTIONS = list(MonthsJap.values())
