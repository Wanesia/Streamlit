import os
import pandas as pd
import streamlit as st

data_path = os.path.join('data', 'Cars.csv')

@st.cache_data
def load_data():
    try:
        data = pd.read_csv(data_path)
    except FileNotFoundError:
        st.error(f"File not found at {data_path}")
        return pd.DataFrame()
    except pd.errors.EmptyDataError:
        st.error("Data file is empty")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"An error occurred while loading data: {e}")
        return pd.DataFrame()

    # Fixing column names (deleted whitespaces and changed to lowercase)
    data.columns = data.columns.str.strip().str.lower()
    # Convert year and month columns to datetime
    data['year'] = pd.to_datetime(data['year'], format='%Y')
    data['month'] = pd.to_datetime(data['month'], format='%b')

    return data