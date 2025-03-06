import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Exploratory Data Analysis Tool")
st.write("Welcome! Upload a CSV file to explore your data.")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        # ----- PREVIEW DATA ----- #
        df = pd.read_csv(uploaded_file)
        st.write("Preview of your data:")
        st.dataframe(df.tail())

        # ----- SUMMARY STATISTICS ----- #
        st.subheader("Summary Statistics")
        st.write(df.describe())  # Shows count, mean, std, min, max, etc.

        # ----- MISSING VALUES ----- #
        st.subheader("Missing Values")
        missing_data = df.isnull().sum()
        st.write(missing_data[missing_data > 0])  # Only show columns with missing values
        if missing_data.sum() == 0:
            st.write("No missing values found!")

        # ----- VISUALIZATION ----- #
        st.subheader("Visualizations")
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        if len(numeric_cols) > 0:
            col_to_plot = st.selectbox("Select a column to visualize", numeric_cols)
            fig, ax = plt.subplots()
            sns.histplot(df[col_to_plot].dropna(), ax=ax)
            st.pyplot(fig)

            # ----- CORRELATION HEATMAP ----- #
            st.subheader("Correlation Heatmap")
            if len(numeric_cols) > 1:
                corr = df[numeric_cols].corr()
                fig, ax = plt.subplots()
                sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
                st.pyplot(fig)
            else:
                st.write("Need at least 2 numeric columns for a correlation heatmap.")
        else:
            st.write("No numeric columns available for visualization.")
    except Exception as e:
        st.error(f"Error loading file: {e}")