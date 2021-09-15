import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("A quick yet powerful user segmentation using RFM" )

'''

# Introduction
Customer segmentation is at the core of a lot of nowadays businesses as it is crucial to understand how users interact with a given service, and identify tomorrow's churners and high value customers.
There are endless ways to segment a service user base, but most techniques act as a black box and are hard to understand or explain.
The purpose of this post is to present you an **easy** and **yet powerful** way to segment users regarding their level of interaction and value towards content.

This article is a quick overview of the concept and applications. If you'd wish to learn more: reach me out on [LinkedIn](https://www.linkedin.com/in/baptistebelescot/) as I might write a far more detailed and documented article about RFM documentation on Medium in the near future.

## RFM segmentation
RFM segmentation is based on three indicators, described as follows:
- **Recency**: translates for how long a user didn't interact with the platform
- **Frequency**: translates the user interaction frequency with the platform
- **Measurement**: translates the interest of the user towards the service and content on the platform

All together, these indicators allow to have an overview of the nature and types of interaction of a user with a service.

Given these raw data, the main idea of **simple** RFM segmentation is to qualify the performance of each of these metrics for each of the users by awarding a score that translates how good the value is compared to other customers.
This part relies on statistical analyses using distribution of values and quantiles, it will be explained in more details later on.

To compute these three indicators it is necessary to define:
- a time window on which we will track and qualify user behaviour 
- what is an interaction with our app/service

# Applied use case to a streaming service

## Problem definition 

Let's suppose we are a big streaming platform and have thousands of users. Let's first define the problem by concretly applying RFM indicators to our use case:
- interactions will be defined as the fact to play a content 
- users will be qualified given their activities within the last 28 days: periodicity is important in content consumption, for better generalization and to introduce less bias on days, it's a common practice to look at an integer number of weeks rather than more symbolic time windows such as a month or 30 days.
- Recency values will go from 0 (played a content today = best) to -28 (played 28 days ago)
- Frenquency will go from 1 (played a content only on one of the 28 days) to 28 (played every day)
- Measurement will be the measure of the average watch session time in minutes (from 0 to any possible value)

## Raw data
Let's directly dive in by looking at some randomly generated R,F,M values for users of a streaming platform on the last 28 days:
'''

st.sidebar.title("Who am I? ")
st.sidebar.markdown('''
Hi, my name is Baptiste and I'm a Data Scientist with 2-3 years of experience.

I have experience working in media and (biomedical) research.

If you have any question or spot a bug (this whole page is still in *beta* and more features will be added in the future), do not hesitate to reach me out on [LinkedIn](https://www.linkedin.com/in/baptistebelescot/).

Code of this webapp and datasets are available on my [GitHub](https://github.com/bbelescot/streaming_RFM_segmentation).

## Optional parameters
Read the whole post first and then come back here to play with parameters :)
''')

df = pd.read_csv("RFM_dataset.csv")

if st.sidebar.button("Reset dataset to demo file"):
    df = pd.read_csv("RFM_dataset.csv")

quantiles = st.sidebar.select_slider(
    label='Number of quantiles to use for RFM scores', options=[2, 3, 4, 5], value=4)

scores = np.linspace(1, quantiles, quantiles).astype(int)
df['m_value'] = df['m_value'].apply(lambda x: int(x*60))

st.dataframe(df)
'''
If we look at the sample **0**, we can see that his *r_value* is equal to 0, which means that he played a content today. His *f_value* is equal to 21 meaning that out of the 28 last days, he played a content on 21 distinct days which is pretty high. Finally, his average play session reaches around 80 minutes, which can be infered as 1 typical full-length movie or 2 tv series episodes.

From these numbers it appears that this user is pretty active as he was connected today and watched very frequently for a good session average time. However, from the raw numbers, it is hard to understand how this user compares with the rest of the user base.

## RFM scores

Now the idea is to go from a lot of values, which all together are hard to analyse and compare, to a set of scoring for each user and metric translating how good the value is compared to others.
This is quite easy to do using pandas built-in quantile cut function *qcut()* and describes as follows: 
'''

with st.echo():
    @st.cache()
    def compute_RFM(df, quantiles, scores):
        df['R'], R_splits = pd.qcut(
            df['r_value'], q=quantiles, labels=scores, retbins=True)
        df['F'], F_splits = pd.qcut(
            df['f_value'], q=quantiles, labels=scores, retbins=True)
        df['M'], M_splits = pd.qcut(
            df['m_value'], q=quantiles, labels=scores, retbins=True)
        df['RFM_score'] = df.apply(lambda row: row.R + row.F + row.M, axis=1)
        df['RFM_class'] = df.apply(lambda row: str(
            int(row.R)) + str(int(row.F)) + str(int(row.M)), axis=1)
        return df, R_splits, F_splits, M_splits

'''
Let's now look at the newly created R,F,M scoring columns on a few samples and see which score was awarded to each user and metric:
### RFM scores
'''

df_RFM, R_splits, F_splits, M_splits = compute_RFM(df, quantiles, scores)
st.dataframe(df_RFM.astype('object').sample(5))

'''
We now have for each line, i.e each user, a comprehensive scoring for recency, frenquency and measurement with 1 being the lowest score and the number of quantiles the highest. 
With this view it is easy to analyse the user behaviour and track his **strengths** and **weaknesses** by looking at individual R, F and M scores. 

The compound RFM_score gives an overall view, the higher the better and more balanced and versatile the user is towards our tracking and performance metrics.'''

fig, ax = plt.subplots(figsize=(10, 4))
ax.set_xlabel('RFM_score')
ax.set_ylabel('Number of users')
df_RFM['RFM_score'].value_counts().sort_index().plot(
    kind='bar', ax=ax, title='Number of users per RFM_score')
st.pyplot(fig)

'''Finally a RFM_class is awarded. It can be used for clustering (note that in the case of a lot of quantiles there will be *quantiles x quantiles x quantiles* classes, it is hence necessary to 
gather similar classes together to reduce dimensions or to compare these classes with another metric, such as churn rate, to find similar clusters). '''

fig2, ax2 = plt.subplots(figsize=(15, 5))
ax2.set_xlabel('RFM_class')
ax2.set_ylabel('Number of users')
df_RFM['RFM_class'].value_counts().sort_index().plot(
    kind='bar', ax=ax2, title='Number of users per RFM_class')
st.pyplot(fig2)

'''In the case of 4 quantiles, the best cluster will be the 444, corresponding to people that consumed content recently, on a frenquent basis and with a lot of interest (long sessions). But other segments
are also intersting, if we look at the 144 for instance, it corresponds to people who had a high frequency and interest in the service but didn't connect for quite a long time: these are very valuable 
users that might churn and for which we should act fast not to loose them! Another intersting cluster would be the 441 corresponding to frequent and recent users but that don't usually stay long to consume content: are they 
struggling finding the content they like?

These are the kind of questions you should ask yourself, for each of the clusters. The main idea being: let's have a product/marketing action targeted for each cluster!

Earlier, we talked about the importance of segments explainability. Because a statistical method was applied it is possible to look at threshold conditions that led to metrics scores (1,2, ...).
Let's display the actual threshold values to which each score corresponds in our use case: 
'''


@st.cache()
def compute_RFM_splits(R_splits, F_splits, M_splits):
    return pd.DataFrame([R_splits[:-1], F_splits[:-1],
                         M_splits[:-1]], index=['R', 'F', 'M'], columns=scores)


st.dataframe(compute_RFM_splits(R_splits, F_splits, M_splits))

'''
Based on these thresholds, it is now easy to understand the type of frequency a user should meet to be part of our best or second best cluster, or the number of days after which, users fall into the lowest recency group that if confronted with churn rate leads to a X times more chance of churn.

## Now it's time to try on your own data!

Define the R,F,M definitions that fit your problem (time window, action to be tracked, ...), compute the raw values using basic Python scripts or SQL, prepare a csv file that meets ReadMe expectations (consult on [GitHub](https://github.com/bbelescot/streaming_RFM_segmentation)) and charge it below to compute RFM scores and classes! 
'''

uploaded_file = st.file_uploader(
    "Upload your own RFM value csv that respect guidelines")
if uploaded_file is not None:
    dfp = pd.read_csv(uploaded_file)[['r_value', 'f_value', 'm_value']]
    '''### RFM scores'''
    dfp_RFM, Rp_splits, Fp_splits, Mp_splits = compute_RFM(
        dfp, quantiles, scores)
    st.dataframe(dfp_RFM.astype('object'))
    '''### RFM thresholds'''
    st.dataframe(compute_RFM_splits(Rp_splits, Fp_splits, Mp_splits))
