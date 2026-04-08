import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Student Performance Dashboard", layout="wide")

st.title("🎓 Student Performance Dashboard")
st.write("Live analysis of 1000+ student records")

# Load data
df = pd.read_csv("StudentsPerformance.csv")

# Create extra columns
df["total score"] = df["math score"] + df["reading score"] + df["writing score"]
df["average score"] = round(df["total score"] / 3, 2)
df["result"] = df["average score"].apply(lambda x: "Pass" if x >= 40 else "Fail")

# KPIs
st.subheader("📊 Key Metrics")
c1, c2, c3 = st.columns(3)
c1.metric("Total Students", len(df))
c2.metric("Average Score", round(df["average score"].mean(), 2))
c3.metric("Pass Percentage", f"{round((df['result'].value_counts()['Pass']/len(df))*100,2)}%")

# Charts
st.subheader("📈 Charts")
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots()
    subject_avg = [
        df["math score"].mean(),
        df["reading score"].mean(),
        df["writing score"].mean()
    ]
    ax.bar(["Math", "Reading", "Writing"], subject_avg)
    ax.set_title("Subject Average")
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots()
    result_counts = df["result"].value_counts()
    ax.pie(result_counts, labels=result_counts.index, autopct="%1.1f%%")
    ax.set_title("Pass vs Fail")
    st.pyplot(fig)

# Raw data
st.subheader("📋 Raw Dataset")
st.dataframe(df)