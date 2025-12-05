"""
categories.py

Defines the Categories enumeration for cashflow transactions.

This enum represents the different categories of financial transactions
such as consumption, savings, investment, and income. It is used throughout
the application for data validation, display in forms, and filtering.
"""

from enum import Enum


class Categories(Enum):
    """Enumeration of transaction categories for the cashflow application."""

    Consumption = 0
    Lifestyle = 1
