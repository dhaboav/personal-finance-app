"""
labels.py

Defines the Labels enumeration for cashflow transactions.

This enum categorizes the type of cashflow as either outcome (expense),
income, or savings. It is used throughout the application for data
validation, filtering, and form selection.
"""

from enum import Enum


class Labels(Enum):
    """Enumeration of transaction labels for the cashflow application."""

    Outcome = 0
    Income = 1
    Savings = 2
