import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("🏏 IPL Data Visualization Dashboard (2008–2020)")

# Load dataset directly from GitHub
url = "IPL.csv"
df = pd.read_csv(url)
st.success("Dataset loaded from GitHub!")

# Sidebar - File uploader
uploaded_file = st.sidebar.file_uploader("Upload your own IPL CSV", type=['csv'])
if uploaded_file:
    df = pd.read_csv(uploaded_file)

# Sidebar Filters
st.sidebar.header("Filter the data")
team = st.sidebar.multiselect("Select Team", options=df['batting_team'].dropna().unique(), default=None)
year = st.sidebar.selectbox("Select Year", options=sorted(df['year'].dropna().unique(), reverse=True))

# Filtered Data
filtered_df = df.copy()
if team:
    filtered_df = filtered_df[(filtered_df['batting_team'].isin(team)) | (filtered_df['bowling_team'].isin(team))]
if year:
    filtered_df = filtered_df[filtered_df['year'] == year]

st.subheader("Filtered Match Data")
st.dataframe(filtered_df)

# Summary Statistics
st.subheader("📊 Summary Stats")
st.write("Total Matches:", filtered_df.shape[0])
st.write("Average Win by Runs:", filtered_df['team_runs'].mean())
st.write("Median Win by Wickets:", filtered_df['team_wicket'].median())

# Bar Chart - Matches per Team
st.subheader("Bar Chart: Matches Played per Team")
matches_played = filtered_df['batting_team'].value_counts() + filtered_df['bowling_team'].value_counts()
matches_played = matches_played.sort_values(ascending=False)
st.bar_chart(matches_played)

# Line Chart - Wins Over the Years
st.subheader("Line Chart: Wins per Season")
wins_by_year = filtered_df.groupby('year')['toss_winner'].value_counts().unstack().fillna(0)
st.line_chart(wins_by_year)

# Pie Chart - Toss Decision
st.subheader("Pie Chart: Toss Decisions")
toss_data = filtered_df['toss_decision'].value_counts()
fig1, ax1 = plt.subplots()
ax1.pie(toss_data, labels=toss_data.index, autopct='%1.1f%%')
st.pyplot(fig1)

# Download Filtered Data
st.subheader("📥 Download Filtered Data")
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("Download CSV", data=csv, file_name='filtered_data.csv', mime='text/csv')
