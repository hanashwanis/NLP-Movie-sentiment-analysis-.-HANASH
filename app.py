import streamlit as st
from textblob import TextBlob
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
st.set_page_config(page_title="Movie Sentiment Pro", layout="wide")
st.title("🎬 Movie Review Sentiment Pro")
tab1, tab2 = st.tabs(["Single Review Analysis", "Bulk CSV Upload"])
with tab1:
    user_review = st.text_area("Paste a Movie Review:", height=150)
    
    col1, col2 = st.columns(2)
    
    if st.button("Analyze & Generate Visuals"):
        if user_review.strip():
            blob = TextBlob(user_review)
            score = blob.sentiment.polarity
            
            with col1:
                st.subheader("Sentiment Result")
                if score > 0: st.success(f"Positive 😊 ({score:.2f})")
                elif score < 0: st.error(f"Negative 😞 ({score:.2f})")
                else: st.warning("Neutral 😐")
            
            with col2:
                st.subheader("Word Cloud")
                wordcloud = WordCloud(background_color="#0E1117", colormap="magma").generate(user_review)
                fig, ax = plt.subplots()
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis("off")
                st.pyplot(fig)
        else:
            st.warning("Please enter text first.")
with tab2:
    st.subheader("Upload multiple reviews")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        if 'review' in df.columns:
            df['sentiment'] = df['review'].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
            st.bar_chart(df['sentiment'])
            st.write(df)
            st.download_button(
                label="Download Analyzed Results",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name='sentiment_results.csv',
                mime='text/csv',
            )
        else:
            st.error("CSV must contain a column named 'review'")