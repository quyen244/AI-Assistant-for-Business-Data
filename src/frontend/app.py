import streamlit as st
import pandas as pd

# Title
st.title("📂 CSV File Upload App")

# Upload file
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    
    # Read file
    df = pd.read_csv(uploaded_file)

    st.success("File uploaded successfully!")

    # Show dataframe
    st.subheader("Preview Data")
    st.dataframe(df)

    # Basic info
    st.subheader("Dataset Info")
    st.write("Rows:", df.shape[0])
    st.write("Columns:", df.shape[1])

    # Numeric summary
    st.subheader("Statistics")
    st.write(df.describe())

    # Categorical summary
    st.subheader("Categorical Columns")
    st.write(df.select_dtypes(include="object").describe())


    # streamlit run src.frontend.app