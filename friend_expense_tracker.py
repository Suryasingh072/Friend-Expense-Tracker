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
st.markdown("""
<div style="display:flex; justify-content:space-between; align-items:center">
<h1 style='color: #4B0082;'>💸 Friend Expense Tracker</h1>
<form>
<button style="background:#E91E63;color:white;padding:8px 15px;border:none;border-radius:5px;cursor:pointer;" onclick="return false;" id="clearDataBtn">Clear All Data</button>
</form>
</div>
""", unsafe_allow_html=True)

# ---------- Load Data ----------
df = pd.read_csv(DATA_FILE)

# ---------- Clear All Data ----------
if st.button("🗑️ Clear All Data"):
    df = pd.DataFrame(columns=["Name", "Expense", "Description", "Date"])
    df.to_csv(DATA_FILE, index=False)
    st.success("All data cleared ✅")

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

# ---------- Load updated data ----------
df = pd.read_csv(DATA_FILE)

# ---------- Display All Expenses with Remove Buttons ----------
st.subheader("All Expenses")

def remove_expense(index):
    global df
    df = df.drop(index).reset_index(drop=True)
    df.to_csv(DATA_FILE, index=False)
    st.experimental_rerun()

for i, row in df.iterrows():
    col1, col2, col3, col4, col5 = st.columns([2,1,3,2,1])
    col1.write(row['Name'])
    col2.write(row['Expense'])
    col3.write(row['Description'])
    col4.write(row['Date'])
    if col5.button("Remove", key=i):
        remove_expense(i)

# ---------- Summary ----------
st.subheader("Expense Summary per Friend")
summary = df.groupby("Name")["Expense"].sum().reset_index()
st.dataframe(summary)

# ---------- Pie Chart ----------
st.subheader("Expense Distribution")
if not summary.empty:
    fig = px.pie(summary, names="Name", values="Expense", color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig)
