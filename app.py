import streamlit as st
import pandas as pd

st.title("[IN DEV - BETA] Streaming service: quick user segmentation")
st.markdown('''

## RFM segmentation is based on three indicators:
- **Recency**: for how long a user didn't interact with the plateform
- **Frequency**: the user frequency of interactiong with the plateform
- **Measurement**: any kind of measurement that qualifies the interest of the user with the content available on the plateform
All together these indicators allow to have an overview of the nature and types of interaction of a user with a service.
Given these raw continuous data, the main idea of **simple** RFM segmentation is to qualify the performance of each of these metric for each of the users by awarding a score given a set of quantiles.
This part will be explained in more details later on.


## To compute these three indicators it is necessary to define:
- a time window on which we'll track user behaviour 
- what is an interaction

## Based on these principles, in the case of a streaming platform, a quick and easy way to perform the segmentation is the following:
- interactions will be defined as the fact to watch a content 
- users will be qualified given their activities within the last 28 days: periodicity is important in media consumption, for better generalization and to introduce less bias on days, it's a common practice to look at an integer number of weeks rather than more symbolic time windows such as a month or 30 days.
- Recency values will go from 0 (watched a content today = best) to -28 (watched 28 days ago)
- Frenquency will go from 1 (watched a content only on one of the 28 days) to 28 (watched every day)
- Measurement will be the measure of the average watch session time in hours (from 0 to any possible value)

# TO BE CONTINUED

''')


st.header("Raw data")


df = pd.read_csv("RFM_dataset.csv")
st.markdown('''
Let's look at some (randomly generated) data with r, f and m values.
''')
st.dataframe(df)
st.markdown('''
Now the idea is to go from a lot of values, which all together are hard to analyse and compare, to a set of scoring for each user and metric translating how good the value is compared to others.
This is quite easy to do using pandas buil-in quantile cut function *qcut()* and describes as follows: 
''')
st.code('''
quantiles = [0,.25,.5,.75,1] #define quantiles: here quartiles
RFM_labels = [1,2,3,4] #define a score for each quantile, where higher is better

#Apply these transformations raw values on the dataframe and save in new R,F,M columns
df['R'], R_splits = pd.qcut(df['r_value'], q=quantiles, labels=RFM_labels, retbins=True)
df['F'], F_splits = pd.qcut(df['f_value'], q=quantiles, labels=RFM_labels, retbins=True)
df['M'], M_splits = pd.qcut(df['m_value'], q=quantiles, labels=RFM_labels, retbins=True)
''')
st.markdown('''
Let's now looks at the newly created R,F,M scoring columns on a few samples:
''')

quantiles = [0,0.25,0.5,0.75,1] #define quantiles: here quartiles
RFM_labels = [1,2,3,4] #define a score for each quantile, where higher is better

#Apply these transformations raw values on the dataframe and save in new R,F,M columns
df['R'], R_splits = pd.qcut(df['r_value'], q=quantiles, labels=RFM_labels, retbins=True)
df['F'], F_splits = pd.qcut(df['f_value'], q=quantiles, labels=RFM_labels, retbins=True)
df['M'], M_splits = pd.qcut(df['m_value'], q=quantiles, labels=RFM_labels, retbins=True)

if st.button('Tap me to try'):
    st.dataframe(df.astype('object'))




