"""
config.py

This module defines global constants and configuration for the App.

Features:
- Loads environment variables from a .env file using `python-dotenv`.
- Provides default app settings, data paths, and required CSV schema.
- Centralized place for configuration values used across the app.

Constants:
- APP_TITLE (str): The title of the application, configurable via environment variable.
- PAGES_PATH (str): Path to the Streamlit pages directory.
- DATA_PATH (str): Default location to save/load financial CSV data.
- REQUIRED_COLUMNS (List[str]): Expected column names for financial CSV files.
"""

from os import getenv

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ------------------------- APP CONFIGURATION -------------------------

APP_TITLE = getenv("APP_TITLE", "Personal Finance App")
PAGES_PATH = "src/pages"
DATA_PATH = "data/finance.csv"
REQUIRED_COLUMNS = ["Date", "Desc", "Label", "Category", "Total"]
