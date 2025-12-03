"""
home.py

Home page layout for the Personal Finance App.

This module renders the welcome screen of the app, highlighting key features,
guiding users on how to get started, and providing a friendly introduction to
the application.
"""

import streamlit as st

from src.core import APP_TITLE

# ------------------------- PAGE LAYOUT -------------------------


def home_layout() -> None:
    """Render the home/welcome page for the Personal Finance App.

    Displays an introduction, key features, and a getting started guide for
    new users.
    """
    st.markdown(
        f"""
        # {APP_TITLE}

        Welcome to **{APP_TITLE}**! We're thrilled to have you on board. This app is designed
        to help you manage your finances more effectively and gain valuable insights into
        your financial habits.

        ## Key Features:
        - **Track Your Spending**: Easily monitor your expenses across different categories.
        - **Set and Manage Budgets**: Create budgets for various categories and track your progress.
        - **Analyze Financial Trends**: Visualize your income, expenses, and savings with detailed charts.
        - **Financial Insights**: Receive personalized tips to help improve your financial health.
        - **Secure Data Management**: Keep your financial data safe with industry-standard security measures.

        ## Getting Started:
        1. **Upload Your Financial Data**: Begin by uploading your expense and income data.
        2. **Set Up Your Budget**: Define budgets for categories like groceries, entertainment, savings, etc.
        3. **Explore Reports**: Access detailed financial reports and visualizations to understand your financial situation.

        We are committed to helping you manage your finances with ease. Let's get started!

        **Your financial well-being is just a few clicks away.**
        """
    )


# ------------------------- ENTRY POINT -------------------------

if __name__ == "__main__":
    home_layout()
