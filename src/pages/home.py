import streamlit as st

from src.core import APP_TITLE


def home_layout():
    st.markdown(
        f"""
        # {APP_TITLE}

        Welcome to **{APP_TITLE}**! We're thrilled to have you on board. This app is designed to help you manage your finances more effectively and gain valuable insights into your financial habits.

        ## Key Features:
        - **Track Your Spending**: Easily monitor your expenses across different categories to stay on top of your budget.
        - **Set and Manage Budgets**: Create budgets for various categories and track your progress in real-time.
        - **Analyze Financial Trends**: Visualize your income, expenses, and savings with detailed charts and reports.
        - **Financial Insights**: Receive personalized tips to help improve your financial health based on your spending patterns.
        - **Secure Data Management**: Keep your financial data safe with industry-standard security measures.

        ## Getting Started:
        1. **Upload Your Financial Data**: Begin by uploading your expense and income data to start tracking your financial journey.
        2. **Set Up Your Budget**: Define budgets for categories like groceries, entertainment, savings, etc., to keep your spending in check.
        3. **Explore Reports**: Access detailed financial reports and visualizations to better understand your financial situation.

        We are committed to helping you manage your finances with ease. Let's get started!

        **Your financial well-being is just a few clicks away.**
    """
    )


if __name__ == "__main__":
    home_layout()
