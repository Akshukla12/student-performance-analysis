import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title="Student Performance Analysis", layout="wide")

# Title
st.title("🎓 Student Performance Data Analysis")
st.markdown("Analyzing academic performance trends across 1,000+ students")

# Load data
df_original = pd.read_csv("StudentsPerformance.csv")
df_original['total score'] = df_original['math score'] + df_original['reading score'] + df_original['writing score']
df_original['average score'] = round(df_original['total score'] / 3, 2)
df_original['result'] = df_original['average score'].apply(lambda x: 'Pass' if x >= 40 else 'Fail')

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filter Data")
gender_filter = st.sidebar.selectbox("Gender", ["All", "male", "female"])
lunch_filter = st.sidebar.selectbox("Lunch Type", ["All"] + list(df_original['lunch'].unique()))
prep_filter = st.sidebar.selectbox("Test Preparation", ["All"] + list(df_original['test preparation course'].unique()))
edu_filter = st.sidebar.selectbox("Parental Education", ["All"] + list(df_original['parental level of education'].unique()))

# Apply filters
df = df_original.copy()
if gender_filter != "All":
    df = df[df['gender'] == gender_filter]
if lunch_filter != "All":
    df = df[df['lunch'] == lunch_filter]
if prep_filter != "All":
    df = df[df['test preparation course'] == prep_filter]
if edu_filter != "All":
    df = df[df['parental level of education'] == edu_filter]

# --- KPI Metrics ---
st.subheader("📊 Key Metrics")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Students", len(df))
col2.metric("Avg Math", round(df['math score'].mean(), 2))
col3.metric("Avg Reading", round(df['reading score'].mean(), 2))
col4.metric("Avg Writing", round(df['writing score'].mean(), 2))
col5.metric("Pass Rate", f"{round((df['result']=='Pass').sum()/len(df)*100, 1)}%")

st.markdown("---")

# --- Row 1 Charts ---
st.subheader("📈 Performance Overview")
col1, col2, col3 = st.columns(3)

with col1:
    fig, ax = plt.subplots()
    subjects = ['Math', 'Reading', 'Writing']
    averages = [df['math score'].mean(), df['reading score'].mean(), df['writing score'].mean()]
    ax.bar(subjects, averages, color=['#4C72B0', '#DD8452', '#55A868'])
    ax.set_title('Average Score by Subject')
    ax.set_ylim(0, 100)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots()
    result_counts = df['result'].value_counts()
    ax.pie(result_counts, labels=result_counts.index, autopct='%1.1f%%', colors=['#55A868', '#C44E52'])
    ax.set_title('Pass vs Fail')
    st.pyplot(fig)

with col3:
    fig, ax = plt.subplots()
    gender_avg = df.groupby('gender')['average score'].mean()
    ax.bar(gender_avg.index, gender_avg.values, color=['#8172B2', '#C44E52'])
    ax.set_title('Avg Score by Gender')
    ax.set_ylim(0, 100)
    st.pyplot(fig)

st.markdown("---")

# --- Row 2 Charts ---
st.subheader("📉 Deep Dive Analysis")
col1, col2, col3 = st.columns(3)

with col1:
    fig, ax = plt.subplots()
    prep_avg = df.groupby('test preparation course')['average score'].mean()
    ax.bar(prep_avg.index, prep_avg.values, color=['#4C72B0', '#DD8452'])
    ax.set_title('Test Prep Impact on Score')
    ax.set_ylim(0, 100)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots()
    edu_avg = df.groupby('parental level of education')['average score'].mean().sort_values()
    ax.barh(edu_avg.index, edu_avg.values, color='#4C72B0')
    ax.set_title('Parental Education Impact')
    ax.set_xlim(0, 100)
    st.pyplot(fig)

with col3:
    fig, ax = plt.subplots()
    ax.hist(df['average score'], bins=20, color='#4C72B0', edgecolor='white')
    ax.set_title('Score Distribution')
    ax.set_xlabel('Average Score')
    ax.set_ylabel('Number of Students')
    st.pyplot(fig)

st.markdown("---")

# --- Correlation Heatmap ---
st.subheader("🔗 Score Correlation Heatmap")
fig, ax = plt.subplots(figsize=(6, 4))
corr = df[['math score', 'reading score', 'writing score', 'average score']].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)

st.markdown("---")

# --- Insights ---
st.subheader("💡 Key Insights")
col1, col2, col3 = st.columns(3)
with col1:
    st.success("📚 Test prep students scored **72.67** vs **65.04** without it — 7.6 point gap")
with col2:
    st.success("👥 Group E was top performing ethnicity with **72.75** average")
with col3:
    st.success("🎓 Master's degree parents → **73.60** avg vs High school → **63.10**")

st.markdown("---")

# --- Download Button ---
st.subheader("⬇️ Download Filtered Report")

@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(df)
st.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name='filtered_student_report.csv',
    mime='text/csv'
)

st.markdown("---")

# --- Raw Data ---
st.subheader("📋 Raw Data")
st.dataframe(df)