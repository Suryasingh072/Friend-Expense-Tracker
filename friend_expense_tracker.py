import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import os

# ---------- CSV file ----------
DATA_FILE = "expenses.csv"
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Name", "Expense", "Description", "Date"])
    df.to_csv(DATA_FILE, index=False)

# ---------- App Header ----------
st.set_page_config(page_title="💸 Friend Expense Tracker", layout="wide")
st.markdown("<h1 style='text-align:center; color: #4B0082;'>💸 Friend Expense Tracker</h1>", unsafe_allow_html=True)

# ---------- Sidebar: Add Expense ----------
st.sidebar.header("Add New Expense")
name = st.sidebar.text_input("Friend Name")
expense = st.sidebar.number_input("Expense Amount", min_value=0)
desc = st.sidebar.text_input("Description")
date = st.sidebar.date_input("Date", datetime.today())

if st.sidebar.button("Add Expense"):
    if name and expense > 0:
        new_data = pd.DataFrame([[name, expense, desc, date]], columns=["Name","Expense","Description","Date"])
        df = pd.read_csv(DATA_FILE)
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.sidebar.success(f"Added {expense} by {name} ✅")
    else:
        st.sidebar.error("Please enter valid name and amount!")

# ---------- Load Data ----------
df = pd.read_csv(DATA_FILE)
st.subheader("All Expenses")
st.dataframe(df)

# ---------- Summary ----------
st.subheader("Expense Summary per Friend")
summary = df.groupby("Name")["Expense"].sum().reset_index()
st.dataframe(summary)

# ---------- Pie Chart ----------
st.subheader("Expense Distribution")
fig = px.pie(summary, names="Name", values="Expense", color_discrete_sequence=px.colors.qualitative.Set3)
st.plotly_chart(fig)
