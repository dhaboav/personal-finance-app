import streamlit as st


def upload_data_layout():
    st.title("Upload Your Data")
    st.write("Please upload your CSV containing your personal finance data.")

    uploaded_file = st.file_uploader("Choose a file", type="csv")


if __name__ == "__main__":
    upload_data_layout()
