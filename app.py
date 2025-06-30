import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="HR Attrition Dashboard", layout="wide")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("EA.csv")
    return df

df = load_data()

# Sidebar filters
st.sidebar.title("Filters")
departments = st.sidebar.multiselect("Select Department", df["Department"].unique(), default=df["Department"].unique())
genders = st.sidebar.multiselect("Select Gender", df["Gender"].unique(), default=df["Gender"].unique())
age_range = st.sidebar.slider("Select Age Range", int(df.Age.min()), int(df.Age.max()), (25, 50))

filtered_df = df[
    (df["Department"].isin(departments)) &
    (df["Gender"].isin(genders)) &
    (df["Age"].between(age_range[0], age_range[1]))
]

st.title("📊 HR Analytics Dashboard - Employee Attrition")

st.markdown("""
This dashboard offers insights into employee attrition using various demographic, performance, and compensation variables. 
Use the filters on the left to customize your analysis.
""")

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total Employees", len(df))
col2.metric("Employees Shown", len(filtered_df))
col3.metric("Attrition Rate", f"{(df['Attrition'].value_counts(normalize=True).get('Yes',0)*100):.2f}%")

# Tabs
tabs = st.tabs(["Overview", "Demographics", "Workplace Factors", "Compensation", "Tenure & Career", "Correlation"])

# Tab 1: Overview
with tabs[0]:
    st.subheader("Attrition by Department")
    fig = px.histogram(filtered_df, x="Department", color="Attrition", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Gender-wise Attrition")
    fig2 = px.pie(filtered_df, names="Gender", color="Attrition", title="Attrition Distribution by Gender")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Attrition by Business Travel")
    fig3 = px.histogram(filtered_df, x="BusinessTravel", color="Attrition", barmode="group")
    st.plotly_chart(fig3, use_container_width=True)

# Tab 2: Demographics
with tabs[1]:
    st.subheader("Age Distribution by Attrition")
    fig = px.box(filtered_df, x="Attrition", y="Age", color="Attrition")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Education Field vs Attrition")
    fig = px.histogram(filtered_df, x="EducationField", color="Attrition", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Marital Status vs Attrition")
    fig = px.histogram(filtered_df, x="MaritalStatus", color="Attrition", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

# Tab 3: Workplace Factors
with tabs[2]:
    st.subheader("Job Role vs Attrition")
    fig = px.histogram(filtered_df, x="JobRole", color="Attrition", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("OverTime Impact on Attrition")
    fig = px.histogram(filtered_df, x="OverTime", color="Attrition", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Environment Satisfaction Levels")
    fig = px.histogram(filtered_df, x="EnvironmentSatisfaction", color="Attrition", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

# Tab 4: Compensation
with tabs[3]:
    st.subheader("Monthly Income vs Attrition")
    fig = px.box(filtered_df, x="Attrition", y="MonthlyIncome", color="Attrition")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Stock Option Level vs Attrition")
    fig = px.histogram(filtered_df, x="StockOptionLevel", color="Attrition", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Percent Salary Hike vs Attrition")
    fig = px.box(filtered_df, x="Attrition", y="PercentSalaryHike", color="Attrition")
    st.plotly_chart(fig, use_container_width=True)

# Tab 5: Tenure & Career
with tabs[4]:
    st.subheader("Years at Company")
    fig = px.histogram(filtered_df, x="YearsAtCompany", color="Attrition", barmode="overlay")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Years Since Last Promotion")
    fig = px.histogram(filtered_df, x="YearsSinceLastPromotion", color="Attrition", barmode="overlay")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Training Times Last Year")
    fig = px.histogram(filtered_df, x="TrainingTimesLastYear", color="Attrition", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

# Tab 6: Correlation
with tabs[5]:
    st.subheader("Correlation Heatmap")
    st.markdown("This matrix helps identify strong positive or negative relationships among numeric features.")
    corr_matrix = filtered_df.select_dtypes(include='number').corr()
    fig, ax = plt.subplots(figsize=(14, 10))
    sns.heatmap(corr_matrix, annot=False, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

    st.subheader("Attrition Count Table")
    st.write(filtered_df['Attrition'].value_counts())

