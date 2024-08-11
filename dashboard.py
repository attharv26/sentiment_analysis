import streamlit as st 
import pandas as pd
import plotly.express as px
from string import punctuation
from textblob import TextBlob
import time

def polarity_calculator(review: str):
    text = TextBlob(review)
    return text.sentiment[0] 

def subjectivity_calculator(review: str):
    text = TextBlob(review)
    return text.sentiment[1] 

def sentiment_identifier(polarity):
    if polarity > 0: return 'positive'
    if polarity < 0: return 'negative'
    if polarity == 0: return 'neutral'

#loading data
@st.cache_data
def load_data():
    df = pd.read_excel('oneplus_reviews.xlsx')
    df=df.drop_duplicates(subset='review')
    df.titles = df.titles.astype('str')
    df.model = df.model.astype('str')
    df.review = df.review.astype('str')
    rating_extractor= lambda txt: float(txt.split('out')[0])
    df['rating'] = df.titles.apply(rating_extractor)
    average_rating = df['rating'].sum()/len(df.rating)
    color_extractor = lambda colour: colour.split('Size')[0].replace('Colour', '').strip(punctuation+ ' ')
    df['color']=df.model.apply(color_extractor)
    storage_extractor = lambda txt:int(txt.split('Size')[1].split(',')[1].strip(punctuation+'GB Storage'))
    df['storage']=df.model.apply(storage_extractor)
    ram_extractor = lambda txt: int(txt.split('Size')[1].split(',')[0].strip(punctuation+'GB RAM'))
    df['RAM'] = df.model.apply(ram_extractor)
    df['polarity'] = df.review.apply(polarity_calculator)
    df['subjectivity'] = df.review.apply(subjectivity_calculator)
    df['sentiment'] = df.polarity.apply(sentiment_identifier)
    #most_sold_variant = int(df.mode()['storage'][0])
    #most_sold_color = df.mode()['color'][0]
    return df

st.set_page_config(layout='wide', page_title='Product Sentiment Analysis', page_icon='📊')

#loading thr data
with st.spinner('loading data.....'):
    df=load_data()
    time.sleep(1)
    
# creating ui

c1, c2 = st.columns([3,1])
c1.header('PRODUCT SENTIMENT ANALYSIS📊')
c1.subheader('ONE PLUS NORD CE 3 LITE 5G📱',  divider='red')
c2.image(r"D:\sentiment_analysis\oneplus_logo.jpeg", use_column_width=True )


c1.header('DATA SUMMARY')
sub_c1, sub_c2 = st.columns(2, gap='medium')


sub_c1.header('POLARITY')
sub_c1.scatter_chart(df['polarity'], color= '#FF0000', y_label='POLARITY')
avg_polarity = float(df.polarity.mean())
sub_c1.metric('AVERAGE POLARITY', avg_polarity, f'{sentiment_identifier(avg_polarity)}')


sub_c2.header('SUBJECTIVITY')
sub_c2.scatter_chart(df['subjectivity'],color='#00FF00', y_label='SUBJECTIVITY')
avg_subjectivity = float(round(df.subjectivity.mean(),2))
sub_c2.metric('AVERAGE SUBJECTIVITY',avg_subjectivity, f'{round(avg_subjectivity*100, 2)}%')

sub_c1.subheader('CUSTOMER RATINGS', divider='red')
cdf = df.groupby('rating').size().reset_index(name='count')
rating_chart = px.pie(cdf, names=cdf.rating, values='count', 
                    title="OUT OF 5",  
                    height=500)
sub_c1.plotly_chart(rating_chart, use_container_width=True)

average_rating = round(df['rating'].sum()/len(df.rating), 2)
sub_c1.metric('AVERAGE RATING',str(average_rating) +'⭐/5')

sub_c2.subheader('SENTIMENT OVERVIEW', divider='red')
sdf = df.groupby('sentiment').size().reset_index(name='count')
color_map = {
    'positve': 'white',
    'negative': 'black',
    'neutral': 'grey'}
sentiment_chart = px.pie(sdf, names=sdf.sentiment, values='count',  
                    height=500,
                    color = 'sentiment',
                    color_discrete_map=color_map )
sub_c2.plotly_chart(sentiment_chart, use_container_width=True)
genral_sentiment = df.mode()['sentiment'][0].upper()
sub_c2.metric('GENERAL SENTIMENT','' , genral_sentiment )

st.divider()
st.text('DATA USED AS OF AUGUST 2024')

