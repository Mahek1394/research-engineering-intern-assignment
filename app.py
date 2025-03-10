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

# File Upload
uploaded_file = st.file_uploader("Upload Social Media Data", type="csv")

@st.cache_data
def load_data(file):
    try:
        df = pd.read_csv(file)
        expected_columns = {'date', 'subreddit', 'title', 'selftext', 'score', 'num_comments', 'upvote_ratio', 'hashtags', 'sentiment_score', 'sentiment_label'}
        missing_columns = expected_columns - set(df.columns)
        if missing_columns:
            st.error(f"Missing expected columns: {missing_columns}")
            return None
        
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df["selftext"].fillna("", inplace=True)
        
        if "sentiment_score" not in df.columns or "sentiment_label" not in df.columns:
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

# Sidebar Filters
st.sidebar.header("🔍 Filters")
min_date, max_date = df["date"].min(), df["date"].max()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])
filtered_df = df[(df["date"] >= pd.to_datetime(date_range[0])) & (df["date"] <= pd.to_datetime(date_range[1]))]

# Dashboard Title
st.title("🗒️ Social Media Analysis Dashboard")

# Article Overview
st.subheader("📰 Article Summary")
if not filtered_df.empty:
    article_info = filtered_df.iloc[0]
    st.write(f"**Title:** {article_info['title']}")
    st.write(f"**Subreddit:** {article_info['subreddit']}")
    st.write(f"**Top Hashtags:** {article_info['hashtags']}")
    st.write("\n")
    
    st.markdown("### 📖 Storytelling Insight")
    st.write("Social media posts often act as digital narratives, reflecting the pulse of public sentiment and engagement. The selected post, from the subreddit `{}`, has gained traction, attracting high levels of discussion and engagement. Hashtags like `{}` indicate the trending themes within the community.".format(article_info['subreddit'], article_info['hashtags']))
else:
    st.warning("No articles found for the selected date range.")

# Engagement Metrics
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
    
    st.markdown("### 📊 Analysis of Trends")
    st.write("Engagement metrics provide insight into how content resonates with the audience. A steady rise in `Likes` and `Comments` suggests strong user interaction. Spikes may indicate viral moments or controversies that triggered widespread discussions.")
else:
    st.warning("No data available for engagement trends.")

# Sentiment Analysis
st.subheader("📊 Sentiment Distribution")
if not filtered_df.empty:
    sentiment_counts = filtered_df["sentiment_label"].value_counts()
    fig_sentiment, ax_sentiment = plt.subplots()
    ax_sentiment.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', colors=['green', 'gray', 'red'])
    plt.title("Sentiment Breakdown")
    st.pyplot(fig_sentiment)
    
    st.markdown("### 🧐 Understanding Sentiments")
    st.write("Analyzing sentiment distribution helps in identifying whether the audience's response is predominantly positive, negative, or neutral. A dominance of `Positive` sentiment suggests user appreciation, while `Negative` sentiment could indicate controversies or dissatisfaction.")
else:
    st.warning("No sentiment data available.")

# Word Cloud
st.subheader("☁️ Word Cloud (Popular Terms)")
text_data = " ".join(filtered_df["selftext"].dropna())
if text_data.strip():
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)
    fig_wc, ax_wc = plt.subplots(figsize=(8, 4))
    ax_wc.imshow(wordcloud, interpolation="bilinear")
    ax_wc.axis("off")
    st.pyplot(fig_wc)
    
    st.markdown("### 🔍 Key Discussion Points")
    st.write("The Word Cloud highlights frequently used words, offering a glimpse into dominant discussion topics. Recurring words indicate themes that users are focusing on, shaping the overall narrative.")
else:
    st.warning("No text data available for Word Cloud.")

# Engagement Summary
st.subheader("🎯 Summary Statistics")
if not filtered_df.empty:
    st.write(f"**Total Score (Likes Equivalent):** {filtered_df['Likes'].sum():,}")
    st.write(f"**Total Comments:** {filtered_df['Comments'].sum():,}")
    st.write(f"**Average Upvote Ratio:** {filtered_df['upvote_ratio'].mean():.2f}")
    
    st.markdown("### 🏆 Final Insights")
    st.write("From an engagement standpoint, this dataset highlights the power of social media in shaping discussions. By examining trends, sentiments, and engagement levels, we can understand user behavior and potential impact areas.")
else:
    st.warning("No engagement data available.")

st.success("Dashboard Successfully Loaded!")
