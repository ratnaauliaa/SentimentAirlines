import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import plotly.express as px

# Set matplotlib backend
import matplotlib
matplotlib.use('Agg')  # Use Agg backend

# Title and introduction
st.title('Tweet Sentiment Analysis')
st.markdown('This application is all about tweet sentiment analysis of airlines. We can analyze reviews of the passengers using this Streamlit app.')

# Sidebar
st.sidebar.title('Sentiment analysis of airlines')
st.sidebar.markdown("🛫 We can analyze passengers' reviews from this application. 🛫")

# Image and caption
image = Image.open('gambar.jpeg')
st.image(image)

# Loading the data
data = pd.read_csv('dataset/datafinal.csv')
label_score = data['label_score']

# Checkbox to show data
if st.checkbox("Show Data"):
    st.write(data.head(50))

# Subheader for Tweets Analyzer
st.sidebar.subheader('Tweets Analyzer')
tweets = st.sidebar.radio('Sentiment Type', ('positif', 'negatif', 'netral'))

# Determine the label_score based on the selected sentiment type
if tweets == 'positif':
    filtered_data = data[data['label_score'] > 5]  # Example: positive sentiment
elif tweets == 'negatif':
    filtered_data = data[data['label_score'] < -5]  # Example: negative sentiment
else:
    filtered_data = data[(data['label_score'] >= -1) & (data['label_score'] <= 1)]  # Example: neutral sentiment

# Check if there are rows matching the selected sentiment
if filtered_data.empty:
    st.warning(f"No data found for sentiment: {tweets}")
else:
    # Sample a single row from the selected sentiment
    sampled_text = filtered_data[['full_text']].sample(3).iat[0, 0]
    st.write(sampled_text)

# Checkbox to display word cloud and sentiment image
if st.sidebar.checkbox("Display Word Cloud"):
    # Generate word cloud
    wordcloud = WordCloud(width=800, height=400, random_state=21, max_font_size=110).generate(' '.join(filtered_data['full_text']))

    # Display word cloud
    st.image(wordcloud.to_image())
    
    # Display sentiment image based on the selection
    select = st.selectbox('Kategori', ['Positif', 'Netral', 'Negatif'], key='sentiment_select')

    if select == "Positif":
        image = Image.open('Positif.png')
        st.image(image)
    elif select == "Negatif":
        image = Image.open('Negatif.png')
        st.image(image)
    else:
        image = Image.open('Netral.png')
        st.image(image)

# Selectbox + visualization
select_viz = st.sidebar.selectbox('Visualization Of Tweets', ['Histogram', 'Pie Chart'], key='viz')
sentiment = data['label'].value_counts()
sentiment = pd.DataFrame({'Sentiment': sentiment.index, 'Tweets': sentiment.values})
st.markdown("### Sentiment count")

if select_viz == "Histogram":
    st.bar_chart(sentiment.set_index('Sentiment'))
else:
    fig = px.pie(sentiment, values='Tweets', names='Sentiment')
    st.plotly_chart(fig)

# Multiselect for Airline tweets by sentiment
st.sidebar.subheader("Airline tweets by sentiment")
choice = st.sidebar.multiselect("Airlines", ('Garuda Indonesia', 'Citilink', 'Batik Air', 'Super Air Jet', 'Pelita Air'), key='airlines_multiselect')
if len(choice) > 0:
    air_data = data[data.airline.isin(choice)]
    fig1 = px.histogram(air_data, x='airline', color='label', labels={'label': 'tweets'}, height=600, width=800)
    st.plotly_chart(fig1)

# Copyright notice
st.markdown(
    """
    ---
    © 2023 Ratna Aulia. 21537141001.
    """
)
