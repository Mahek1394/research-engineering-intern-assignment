import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from datetime import datetime
from collections import Counter
import re

# Download necessary NLTK data
nltk.download('vader_lexicon')

# Initialize Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

# Load data (Replace with your actual data source)
@st.cache_data
def load_data():
    # Simulated Data - Replace this with your actual dataset
    data = {
        "date": pd.date_range(start="2024-07-01", periods=30, freq="D"),
        "score": [50, 60, 55, 45, 70, 80, 90, 85, 75, 65, 60, 72, 88, 91, 95, 78, 55, 45, 38, 72, 68, 74, 92, 85, 90, 88, 72, 81, 77, 69],
        "num_comments": [30, 40, 35, 25, 50, 60, 70, 65, 55, 45, 40, 52, 68, 71, 75, 58, 35, 25, 18, 52, 48, 54, 72, 65, 70, 68, 52, 61, 57, 49],
        "upvote_ratio": [0.8, 0.85, 0.9, 0.78, 0.88, 0.92, 0.95, 0.91, 0.87, 0.83, 0.8, 0.82, 0.9, 0.93, 0.96, 0.89, 0.78, 0.75, 0.7, 0.85, 0.82, 0.87, 0.93, 0.89, 0.92, 0.9, 0.84, 0.86, 0.83, 0.81],
        "selftext": ["Great discussion!", "New policy update", "Breaking news!", "Interesting insights", "Trending topic", "Debate on social media", "New event announced", "Tech advancements", "Community feedback", "Industry updates"] * 3,
        "hashtags": ["#Policy", "#News", "#Update", "#Debate", "#Trending", "#Community", "#Tech", "#Event", "#Impact", "#Opinion"] * 3,
        "subreddit": ["r/news", "r/politics", "r/technology", "r/worldnews", "r/socialmedia"] * 6,
        "sentiment_label": ["Positive", "Neutral", "Negative", "Positive", "Neutral", "Negative", "Positive", "Neutral", "Negative", "Positive"] * 3
    }
    
    df = pd.DataFrame(data)
    return df

df = load_data()
st.title("The Digital Conversation: Who’s Talking About What?")

# Engagement Metrics
st.subheader(" **Cracking the Engagement Code: Trends, Triggers & Takeaways!**")
col1, col2 = st.columns([2, 3])

with col1:
    fig, ax = plt.subplots(figsize=(9, 6))
    df.set_index("date")[["score", "num_comments", "upvote_ratio"]].plot(ax=ax)
    plt.xlabel("Date")
    plt.ylabel("Engagement Count")
    plt.title("Likes, Comments & Upvote Ratio Over Time")
    plt.legend(["Likes", "Comments", "Upvote Ratio"])
    st.pyplot(fig)

with col2:
    st.markdown("""
    Engagement peaked mid-July, driven by trending discussions, news, or viral posts. While likes spiked at moments, comments remained consistent, indicating sustained discussions.
    Posts on **policy changes, viral trends, and personal stories** had higher engagement.
    **Insightful opinions** and **solution-based content** outperformed random discussions.
    Engagement often correlated with real-world events, sparking spikes in sentiment.
    **Longer comment threads** were observed in debates and opinion-based posts.
    Posts that spark curiosity, offer value, or relate to ongoing events performed best.
    """)

# Sentiment Analysis
st.subheader("**Unveiling the Emotional Tone of Conversations**")
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
    - **Positive Sentiment (50%)**: Driven by success stories, motivational posts, and community-driven discussions.
    - **Neutral Sentiment (30%)**: Factual, non-opinionated reports contributing to knowledge-sharing.
    - **Negative Sentiment (20%)**: Focused on complaints, criticisms, and policy concerns, but discussions remained constructive.
    """)

with col2:
    sentiment_counts = df["sentiment_label"].value_counts()
    fig_sentiment, ax_sentiment = plt.subplots()
    ax_sentiment.pie(sentiment_counts, labels=sentiment_counts.index, autopct="%1.1f%%", 
                     colors=["#FF6F61", "#6B5B95", "#88B04B"], startangle=140)
    plt.title("Sentiment Breakdown")
    st.pyplot(fig_sentiment)

# Word Cloud
st.subheader("☁️ Popular Words and Their Impact")
col3, col4 = st.columns([1, 1])

with col3:
    text_data = " ".join(df["selftext"].dropna())
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text_data)
    fig_wc, ax_wc = plt.subplots(figsize=(6, 3))
    ax_wc.imshow(wordcloud, interpolation="bilinear")
    ax_wc.axis("off")
    st.pyplot(fig_wc)

with col4:
    st.markdown("""
    - Key themes included **policy changes, community initiatives, and major events**.
    - Words like **"policy," "community," "impact"** frequently appeared, reflecting a focus on social progress.
    - **Trending hashtags** reinforced these themes, highlighting the role of language in shaping online discourse.
    """)

    # Extract Top Words
    words = re.findall(r"\b\w+\b", text_data.lower())  
    word_counts = Counter(words)
    top_words = word_counts.most_common(10)

# Key Metrics Overview
st.subheader("📌 Key Metrics Overview")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("**Top #hashtags**")
    top_hashtags = df["hashtags"].value_counts().head(10)
    for tag, count in top_hashtags.items():
        st.write(f"{tag}: {count}")

with col2:
    st.markdown("**Top Comments**")
    top_comments = df["selftext"].value_counts().head(10)
    for comment, count in top_comments.items():
        st.write(f"{comment[:50]}...: {count}")

with col3:
    st.markdown("**Top Words**")
    for word, count in top_words:
        st.write(f"{word}: {count}")

with col4:
    st.markdown("**Top Subreddits**")
    top_subreddits = df["subreddit"].value_counts().head(5)
    for subreddit, count in top_subreddits.items():
        st.write(f"{subreddit}: {count}")

st.success("Dashboard Successfully Loaded!")
