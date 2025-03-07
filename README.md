# research-engineering-intern-assignment
Here's your updated README file with placeholders for an image and a video. You can replace the placeholders with actual links or file paths as needed.

---

# **Social Media Article Analysis Dashboard**

![Dashboard Screenshot] ](https://drive.google.com/drive/folders/1E_vdL0Fk-v8DfM-p5mafkBYLpnT4b1AY?usp=sharing) 

[📺 Watch Demo Video]https://drive.google.com/file/d/1p6SC0gY83MUixJFYiM_nKIpPmlno9atp/view?usp=drive_link

## **Overview**  
The Social Media Article Analysis Dashboard is designed to analyze and visualize trends from social media posts, including engagement metrics, sentiment distribution, and key topics. It helps users explore how a particular topic or URL is discussed online.  

This dashboard is implemented using **Streamlit**, **Pandas**, **Matplotlib**, **Seaborn**, and **NLTK** for sentiment analysis. It processes and visualizes data extracted from social media platforms such as Reddit, Twitter, or news forums.  

---

## **System Design Thought Process**  
The system is structured into three main components:  

### **a. Data Loading and Preprocessing**  
- **Purpose**: Ensure the dataset is structured properly before analysis.  
- **Key Steps**:  
  - Load data from a CSV file.  
  - Validate the presence of expected columns.  
  - Convert the date column to a proper `datetime` format.  
  - Compute sentiment scores using `VADER` sentiment analysis.  
  - Assign sentiment labels (`Positive`, `Neutral`, `Negative`).  

- **Why?** Ensuring data consistency is crucial for accurate visualization.  

---

### **b. Interactive Filtering and Dashboard Structure**  
The dashboard consists of multiple sections that allow users to explore the data dynamically.  

#### **1️⃣ Sidebar for Filters**  
- **Why?** Users can adjust filters to focus on a specific date range.  
- **Implementation**:  
  - A date range selector is used to filter data dynamically.  

#### **2️⃣ Article Summary**  
- **Why?** Gives users a quick understanding of the most relevant article.  
- **Implementation**:  
  - Displays the **title, source, and top hashtags** from the first matching result.  

#### **3️⃣ Engagement Metrics Over Time**  
- **Why?** Helps track how a topic is trending over time.  
- **Implementation**:  
  - A **time-series line graph** using `Matplotlib` to show **likes** and **comments** over time.  
  - **Labeling Change**: Instead of `score` and `num_comments`, we label them as **"Likes"** and **"Comments"** for clarity.  

#### **4️⃣ Sentiment Analysis**  
- **Why?** Shows how people feel about the topic.  
- **Implementation**:  
  - A **pie chart** that visualizes the proportion of positive, neutral, and negative sentiments.  

#### **5️⃣ Word Cloud (Popular Terms)**  
- **Why?** Helps users understand the common words used in discussions.  
- **Implementation**:  
  - A **WordCloud** is generated using the `wordcloud` library from the collected text data.  

#### **6️⃣ Top Comments**  
- **Why?** Shows the most upvoted and relevant comments.  
- **Implementation**:  
  - The top 5 comments with the highest likes are displayed.  

#### **7️⃣ Summary Statistics**  
- **Why?** Gives an overall engagement summary.  
- **Implementation**:  
  - Displays **total likes, total comments, and average upvote ratio**.  

---

## **Enhancements for Better User Experience**  

The dashboard effectively presents:  
- 📊 **Time-series trends** for engagement metrics.  
- 🔥 **Trending words via a word cloud**.  
- 😀 **Sentiment distribution via a pie chart**.  
- 💬 **Top comments** sorted by engagement.  
 

---

## **How to Run the Dashboard Locally**  
1. Clone the repository:  
   ```bash
   git clone https://github.com/your-repo/social-media-dashboard.git
   cd social-media-dashboard
   ```
2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:  
   ```bash
   streamlit run app.py
   ```
4. Open your browser and go to `http://localhost:8501/`.  

---

## **Conclusion**  
This dashboard is an effective tool for social media trend analysis, offering a **user-friendly, data-driven approach** to understanding discussions online. The modular design ensures **scalability** and easy integration with more data sources in the future.  

  

---  

---

Let me know if you need any modifications! 🚀

