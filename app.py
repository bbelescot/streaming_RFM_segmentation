import streamlit as st
import pandas as pd

st.title("A quick yet powerful user segmentation using RFM", )
st.image('The-Key-to-Successful-Segmentations.jpg')
st.markdown('''
# Introduction
Customer segmentation is at the core of a lot of nowadays businesses as it is crucial to understand how users interact with a given service, and identify tomorrow's churners and high value customers.
There are endless ways to segment a service user base, but most techniques act as a black box and are hard to understand or explain.
The purpose of this little example is to present you an **easy** and **yet powerful** way to segment users regarding their level of interaction and value towards content.
''')
st.markdown('''

## RFM segmentation
RFM segmentation is based on three indicators, described as follows:
- **Recency**: translates for how long a user didn't interact with the platform
- **Frequency**: translates the user frequency of interactiong with the platform
- **Measurement**: translates the interest of the user towards the content on the platform

All together, these indicators allow to have an overview of the nature and types of interaction of a user with a service.

Given these raw data, the main idea of **simple** RFM segmentation is to qualify the performance of each of these metrics for each of the users by awarding a score that translates how good the value is compared to other customers.
This part relies on statistical analyses using distribution of values and quantiles, it will be explained in more details later on.

To compute these three indicators it is necessary to define:
- a time window on which we will track and qualify user behaviour 
- what is an interaction

# Example for a streaming platform

## Problem definition 

Let's suppose we are a big streaming platform and have thousands of users. Let's first define the problem by concretly applying RFM indicators to our use case:
- interactions will be defined as the fact to play a content 
- users will be qualified given their activities within the last 28 days: periodicity is important in content consumption, for better generalization and to introduce less bias on days, it's a common practice to look at an integer number of weeks rather than more symbolic time windows such as a month or 30 days.
- Recency values will go from 0 (played a content today = best) to -28 (played 28 days ago)
- Frenquency will go from 1 (played a content only on one of the 28 days) to 28 (played every day)
- Measurement will be the measure of the average watch session time in hours (from 0 to any possible value)

## Raw data
Let's directly dive in by looking at some randomly generated R,F,M values for users of a streaming platform on the last 28 days:
''')

df = pd.read_csv("RFM_dataset.csv")

st.dataframe(df)
st.markdown('''
If we look at the first sample that corresponds to **user_0**, we can see that his **r_value** is equal to 0, which means that he played a content today. His **f_value** is equal to 21 meaning that out of the 28 last days, he played a content on 21 distinct days which is pretty high. Finally, his average play session reaches around 80 minutes, which can be infered as 1 typical full-length movie or 2 tv series episodes.
From these numbers it appears that this user is pretty active as he was connected today and watched very frequently for a good session average time. However, from the raw numbers, it is hard to understand how this user compares with the rest of the user base.

## RFM scores

Now the idea is to go from a lot of values, which all together are hard to analyse and compare, to a set of scoring for each user and metric translating how good the value is compared to others.
This is quite easy to do using pandas built-in quantile cut function *qcut()* and describes as follows: 
''')

with st.echo():
    #Define quantiles: here 4 quartiles are used
    quantiles = [0,.25,.5,.75,1] 
    #Define a score for each quantile, where higher is better
    scores = [1,2,3,4] 
    #Apply these transformations raw values on the dataframe and save in new R,F,M columns
    df['R'], R_splits = pd.qcut(df['r_value'], q=quantiles, labels=scores, retbins=True)
    df['F'], F_splits = pd.qcut(df['f_value'], q=quantiles, labels=scores, retbins=True)
    df['M'], M_splits = pd.qcut(df['m_value'], q=quantiles, labels=scores, retbins=True)

st.markdown('''
Let's now look at the newly created R,F,M scoring columns on a few samples and see which score was awarded to each user and metric:
''')

if st.button('Tap me to try'):
    st.markdown(''' 
    And here goes the RFM scores:
    ''')
    st.dataframe(df.astype('object').head(3))




