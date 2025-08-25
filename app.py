import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

# -----------------------
# Page Setup
# -----------------------
st.set_page_config(page_title="Survey Data Dashboard", layout="wide")
st.title("📊 Survey Data Visualization Dashboard")

# -----------------------
# CSV Upload or Sample Data
# -----------------------
uploaded_file = st.file_uploader("अपनी Survey CSV फाइल अपलोड करें", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ CSV फाइल अपलोड हो गई!")
else:
    st.warning("⚠ कोई फाइल अपलोड नहीं हुई। सैंपल डेटा इस्तेमाल हो रहा है।")
    np.random.seed(42)
    n = 100
    df = pd.DataFrame({
        'Age Group': np.random.choice(['18-25', '26-35', '36-45', '46+'], n),
        'Gender': np.random.choice(['Male', 'Female', 'Other'], n),
        'Satisfaction': np.random.choice(['Very Satisfied', 'Satisfied', 'Neutral', 'Dissatisfied', 'Very Dissatisfied'], n),
        'Rating': np.random.randint(1, 6, n),
        'Preferred Platform': np.random.choice(['Website', 'Mobile App', 'In-Store'], n)
    })

# -----------------------
# Filters
# -----------------------
st.sidebar.header("🔍 Filters")
age_filter = st.sidebar.multiselect("Age Group", options=df['Age Group'].unique(), default=df['Age Group'].unique())
gender_filter = st.sidebar.multiselect("Gender", options=df['Gender'].unique(), default=df['Gender'].unique())

filtered_df = df[(df['Age Group'].isin(age_filter)) & (df['Gender'].isin(gender_filter))]

st.subheader("📄 Filtered Data")
st.dataframe(filtered_df.head())

# -----------------------
# Download Button
# -----------------------
csv_download = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("⬇️ Download Filtered Data", data=csv_download, file_name="filtered_survey.csv", mime="text/csv")

# -----------------------
# Charts
# -----------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Age Group Distribution")
    fig_age = px.histogram(filtered_df, x='Age Group', color='Age Group', title='Age Group Count', text_auto=True)
    st.plotly_chart(fig_age, use_container_width=True)

with col2:
    st.subheader("Gender Distribution")
    fig_gender = px.pie(filtered_df, names='Gender', title='Gender Share', hole=0.3)
    st.plotly_chart(fig_gender, use_container_width=True)

st.subheader("Customer Satisfaction Levels")
fig_satisfaction = px.bar(filtered_df, x='Satisfaction', color='Satisfaction', title='Satisfaction Breakdown')
st.plotly_chart(fig_satisfaction, use_container_width=True)

# Extra Chart: Rating Distribution
st.subheader("Rating Distribution")
fig_rating = px.histogram(filtered_df, x='Rating', nbins=5, title='Rating Frequency', color_discrete_sequence=['#636EFA'])
st.plotly_chart(fig_rating, use_container_width=True)

st.success("✅ Dashboard Ready! Filters का इस्तेमाल करके डेटा Explore करें।")

