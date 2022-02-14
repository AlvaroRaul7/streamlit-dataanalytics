
import datetime
import streamlit as st
import pandas as pd

st.write("""

# World Grocer Visualization
""")


date = st.date_input(
     "Choose the date",
     datetime.date(2021, 4, 30))


print(date)

date = pd.to_datetime(date)
df = pd.read_csv("./offer_history.csv")
df = df[(pd.to_datetime(df['offerdate']) >= pd.to_datetime("2021-03-13")) & (pd.to_datetime(df['offerdate'])<= date)]
count = df['customer_id'].count()

count_repeaters_exp = df.loc[(df['is_repeater'] == 1) & (df['in_controlgroup'] == 0)].count()

count_repeaters_group = df.loc[(df['is_repeater'] == 1) & (df['in_controlgroup'] == 1)].count()



st.subheader("Total offers sent by date")
st.metric(label="", value=int(count))
   
st.subheader("Total repeaters to date")
col4,col5 = st.columns(2)
with col4:
    st.metric(label="Experiment", value=int(count_repeaters_exp['customer_id']))
with col5:
    st.metric(label="Group", value=int(count_repeaters_group['customer_id']))
df2 = pd.read_csv("./offer_lookup.csv")


# CLV for each customer is calculated as follows: $50 * is_repeater - offervalue

df3 = pd.merge(df, df2, on='offer_id')
df3['CLV']= 50*df3['is_repeater']- df3['offervalue']



st.subheader("Total CLV to date")
st.write("when repeated is true")
count_repeaters_exp_clv = df3.loc[ (df['is_repeater'] == 1) & (df3['in_controlgroup'] == 0)]



count_repeaters_group_clv = df3.loc[ (df['is_repeater'] == 1) & (df3['in_controlgroup'] == 1)]


col6,col7= st.columns(2)

with col6:
    st.metric(label="Experiment", value=int(count_repeaters_exp_clv['CLV'].sum()))
with col7:
    st.metric(label="Experiment", value=int(count_repeaters_group_clv['CLV'].sum()))
df4 = count_repeaters_exp_clv[['offerdate', 'CLV']].rename(columns={'offerdate':'index'}).set_index('index')
df5 = count_repeaters_group_clv[['offerdate', 'CLV']].rename(columns={'offerdate':'index'}).set_index('index')
df4 = df4.rename(columns={"CLV":"CLV EXPERIMENT"})
df5 = df5.rename(columns={"CLV":"CLV GROUP"})

col8, col9 = st.columns(2)
st.subheader("Daily CLV Experiment to date")
st.write("when repeated is true")
st.line_chart(df4)
st.subheader("Daily CLV Group to date")
st.write("when repeated is true")
st.line_chart(df5)
