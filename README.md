<br />
<div align="center">
<h3 align="center">personal-finance-app</h3>

  <p align="center">
    A tool for tracking and managing personal finances via CSV file.
  </p>
</div>

---

### Overview

`Personal Finance App` is a tool designed to help users track, analyze, and manage their personal finances. It supports uploading CSV files containing transactions, categorizing expenses, and generating insightful financial summaries for better decision-making.


### Features

- Upload CSV files with transaction data.

- Generate financial reports and summaries.

- Track spending trends and savings goals.

---

### Installation Guide (Non-Docker)

Follow these steps to set up the project locally:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/dhaboav/personal-finance-app.git
    ```

2. **Install Python dependencies:**

    Install the required Python packages using `pip`:

    ```bash
    pip install -r requirments.txt
    ```

3. **Set up the environment file:**

    Copy the `.env.example` file to `.env` to configure environment variables:

    - **On Windows:**

        ```bash
        copy .env.example .env
        ```

    - **On macOS/Linux:**

        ```bash
        cp .env.example .env
        ```
