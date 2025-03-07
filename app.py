import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from datetime import datetime

# Download necessary NLTK data
nltk.download('vader_lexicon')

# Initialize Sentiment Analyzer
sia = SentimentIntensityAnalyzer()
uploaded_file = st.file_uploader("social_media_data", type="csv")
if uploaded_file is not None:
    try:
        # Use the uploaded_file object directly, not a file path
        df = pd.read_csv(uploaded_file)
        st.write("Data loaded successfully!")
        st.dataframe(df)
    except Exception as e:
        st.error(f"Error loading data: {e}")
else:
    st.info("Please upload a file to continue")
# Load Data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("social_media_data.csv")

        # Ensure required columns exist
        expected_columns = {'date', 'subreddit', 'title', 'selftext', 'score', 
                            'num_comments', 'upvote_ratio', 'hashtags', 'sentiment_score', 'sentiment_label'}
        missing_columns = expected_columns - set(df.columns)
        if missing_columns:
            st.error(f"Missing expected columns: {missing_columns}")
            return None

        # Convert 'date' column to datetime
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

        # Fill NaN values in text columns
        df["selftext"] = df["selftext"].fillna("")

        # Apply sentiment analysis if missing
        if "sentiment_score" not in df.columns or "sentiment_label" not in df.columns:
            df["sentiment_score"] = df["selftext"].apply(lambda x: sia.polarity_scores(str(x))["compound"])
            df["sentiment_label"] = df["sentiment_score"].apply(lambda x: "Positive" if x > 0.05 else "Negative" if x < -0.05 else "Neutral")

        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Load and validate data
df = load_data()
if df is None:
    st.stop()

# Sidebar Filters
st.sidebar.header("🔍 Filters")

# Date range selection
min_date, max_date = df["date"].min(), df["date"].max()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])

# Apply Date Filter
filtered_df = df[(df["date"] >= pd.to_datetime(date_range[0])) & (df["date"] <= pd.to_datetime(date_range[1]))]

# Dashboard Title
st.title("🗒️ Social Media Analysis Dashboard")

# **1️⃣ Article Overview**
st.subheader("📰 Article Summary")
if not filtered_df.empty:
    article_info = filtered_df.iloc[0]
    st.write(f"**Title:** {article_info['title']}")
    st.write(f"**Subreddit:** {article_info['subreddit']}")
    st.write(f"**Top Hashtags:** {article_info['hashtags']}")
else:
    st.warning("No articles found for the selected date range.")

# **2️⃣ Engagement Metrics Over Time**
st.subheader("📈 Engagement Metrics")
if not filtered_df.empty:
    fig, ax = plt.subplots(figsize=(10, 5))
    filtered_df = filtered_df.rename(columns={"score": "Likes", "num_comments": "Comments"})
    filtered_df.set_index('date')[['Likes', 'Comments', 'upvote_ratio']].plot(ax=ax)
    plt.xlabel("Date")
    plt.ylabel("Engagement Count")
    plt.title("Likes, Comments & Upvote Ratio Over Time")
    plt.legend()
    st.pyplot(fig)
else:
    st.warning("No data available for engagement trends.")

# **3️⃣ Sentiment Analysis**
st.subheader("📊 Sentiment Distribution")
if not filtered_df.empty:
    sentiment_counts = filtered_df["sentiment_label"].value_counts()
    fig_sentiment, ax_sentiment = plt.subplots()
    ax_sentiment.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', colors=['green', 'gray', 'red'])
    plt.title("Sentiment Breakdown")
    st.pyplot(fig_sentiment)
else:
    st.warning("No sentiment data available.")

# **4️⃣ Word Cloud (Popular Terms)**
st.subheader("☁️ Word Cloud(Popular Terms)")
text_data = " ".join(filtered_df["selftext"].dropna())
if text_data.strip():
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)
    fig_wc, ax_wc = plt.subplots(figsize=(8, 4))
    ax_wc.imshow(wordcloud, interpolation="bilinear")
    ax_wc.axis("off")
    st.pyplot(fig_wc)
else:
    st.warning("No text data available for Word Cloud.")

# **5️⃣ Key Contributors (Top Subreddits)**
st.subheader("👥 Top Contributing Subreddits")
if not filtered_df.empty:
    subreddit_counts = filtered_df["subreddit"].value_counts().head(5)
    fig_subreddit, ax_subreddit = plt.subplots()
    sns.barplot(x=subreddit_counts.index, y=subreddit_counts.values, ax=ax_subreddit, palette='coolwarm')
    plt.xticks(rotation=45)
    plt.ylabel("Number of Posts")
    plt.title("Top Contributing Subreddits")
    st.pyplot(fig_subreddit)
else:
    st.warning("No subreddit data available.")

# **6️⃣ Top Comments**
st.subheader("💬 Top Comments")
if not filtered_df.empty:
    top_comments = filtered_df.sort_values(by="Likes", ascending=False)[["selftext", "Likes"]].head(5)
    st.table(top_comments)
else:
    st.warning("No comments available.")

# **7️⃣ Engagement Summary**
st.subheader("🎯 Summary Statistics")
if not filtered_df.empty:
    st.write(f"**Total Score (Likes Equivalent):** {filtered_df['Likes'].sum():,}")
    st.write(f"**Total Comments:** {filtered_df['Comments'].sum():,}")
    st.write(f"**Average Upvote Ratio:** {filtered_df['upvote_ratio'].mean():.2f}")
else:
    st.warning("No engagement data available.")

st.success(" Dashboard Successfully Loaded!")
