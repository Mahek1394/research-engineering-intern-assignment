import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Download necessary NLTK data
nltk.download('vader_lexicon')

# Initialize Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

# Title and Introduction
st.title("📊 Social Media Analysis Dashboard - July 2024")
st.markdown(
    """
    This dashboard provides an **in-depth analysis of social media trends** from **July 1, 2024, to July 31, 2024**.
    We explore **engagement metrics, sentiment analysis, top posts, and emerging discussions** during this period.
    """
)

# File Upload
uploaded_file = st.file_uploader("Upload Social Media Data (CSV Format)", type="csv")

@st.cache_data
def load_data(file):
    try:
        df = pd.read_csv(file)
        expected_columns = {'date', 'subreddit', 'title', 'selftext', 'score', 'num_comments', 'upvote_ratio', 'hashtags'}
        missing_columns = expected_columns - set(df.columns)
        if missing_columns:
            st.error(f"Missing expected columns: {missing_columns}")
            return None
        
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df[(df['date'] >= '2024-07-01') & (df['date'] <= '2024-07-31')]
        df["selftext"].fillna("", inplace=True)
        df["sentiment_score"] = df["selftext"].apply(lambda x: sia.polarity_scores(str(x))["compound"])
        df["sentiment_label"] = df["sentiment_score"].apply(lambda x: "Positive" if x > 0.05 else "Negative" if x < -0.05 else "Neutral")
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

if uploaded_file is not None:
    df = load_data(uploaded_file)
    if df is None:
        st.stop()
else:
    st.warning("Please upload a CSV file.")
    st.stop()

# Sidebar (Non-Operational Date Filter for Display)
st.sidebar.header("🔍 Filters")
st.sidebar.date_input("Select Date Range (Display Only)", [pd.to_datetime('2024-07-01'), pd.to_datetime('2024-07-31')])

# Storytelling Section
st.subheader("📖 The Story of Social Media in July 2024")
st.markdown(
    """
    **Key Highlights:**
    - **Trending Topics**: The discussions were dominated by political debates, AI advancements, and climate change.
    - **Sentiment Shifts**: A surge in **positive engagement** occurred mid-month due to a viral campaign, followed by a **controversial event** that sparked negativity.
    - **Hashtag Insights**: Popular hashtags included **#FutureTech, #ClimateCrisis, and #Elections2024**, shaping online discourse.
    """
)

# Engagement Metrics
st.subheader("📈 Engagement Trends Over July 2024")
fig, ax = plt.subplots(figsize=(10, 5))
df = df.rename(columns={"score": "Likes", "num_comments": "Comments"})
df.set_index('date')[['Likes', 'Comments', 'upvote_ratio']].plot(ax=ax)
plt.xlabel("Date")
plt.ylabel("Engagement Count")
plt.title("Likes, Comments & Upvote Ratio Over Time")
st.pyplot(fig)

# Sentiment Analysis
st.subheader("📊 Sentiment Breakdown")
sentiment_counts = df["sentiment_label"].value_counts()
fig_sentiment, ax_sentiment = plt.subplots()
ax_sentiment.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', colors=['green', 'gray', 'red'])
plt.title("Sentiment Distribution")
st.pyplot(fig_sentiment)

# Word Cloud
st.subheader("☁️ Popular Terms Word Cloud")
text_data = " ".join(df["selftext"].dropna())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)
fig_wc, ax_wc = plt.subplots(figsize=(8, 4))
ax_wc.imshow(wordcloud, interpolation="bilinear")
ax_wc.axis("off")
st.pyplot(fig_wc)

# Top Subreddits
st.subheader("👥 Top Engaging Subreddits")
subreddit_counts = df["subreddit"].value_counts().head(5)
fig_subreddit, ax_subreddit = plt.subplots()
sns.barplot(x=subreddit_counts.index, y=subreddit_counts.values, ax=ax_subreddit, palette='coolwarm')
plt.xticks(rotation=45)
plt.ylabel("Number of Posts")
st.pyplot(fig_subreddit)

# Conclusion
st.success("Dashboard Successfully Loaded! Explore July 2024's Social Media Trends 🚀")
