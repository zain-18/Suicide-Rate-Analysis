from decimal import Decimal

import pandas as pd
import altair as alt
import streamlit as st
from numerize import numerize

st.set_page_config(
     layout="wide")

st.title('Suicide Rate Analysis')
df=pd.read_csv('master_clean.csv')
year_SR_df=df.groupby(df['year'])['suicides_no'].sum().reset_index().sort_values('suicides_no',ascending=False)
Total_suicide=year_SR_df['suicides_no'].sum()
Total_suicide=numerize.numerize(Decimal(float(Total_suicide)))


st.metric(label="Number Suicides from 1987-2016", value=Total_suicide)

st.subheader('Suicide rate per year')
chart = alt.Chart(year_SR_df).mark_bar().encode(
  x=alt.X('year'),
  y=alt.Y('suicides_no')
)
st.altair_chart(chart, use_container_width=True)

col1, col2= st.columns(2)
with col1:
    gender_ratio = df.groupby('sex')['suicides_no'].sum().reset_index()
    st.subheader('Suicide ratio in Gender')
    chart = alt.Chart(gender_ratio).mark_bar().encode(
        x=alt.X('sex'),
        y=alt.Y('suicides_no')
    )
    st.altair_chart(chart, use_container_width=True)
with col2:
    age_df = df.groupby('age')['suicides_no'].sum().reset_index()
    st.subheader('Suicide ratio in age group')
    chart = alt.Chart(age_df).mark_bar().encode(
        x=alt.X('age',sort=None),
        y=alt.Y('suicides_no')
    )
    st.altair_chart(chart, use_container_width=True)

st.subheader('Top 10 Countries with High Suicide Rate')
country_df=df.groupby('country')['suicides_no'].sum().reset_index()
country_df=country_df.sort_values('suicides_no',ascending=False)
chart = alt.Chart(country_df.head(10)).mark_bar().encode(
  x=alt.X('country',sort=None),
  y=alt.Y('suicides_no')
)
st.altair_chart(chart, use_container_width=True)

gender_ratio=df.groupby(['country','sex'])['suicides_no'].sum().reset_index()
gender_ratio=gender_ratio.sort_values('suicides_no',ascending=False)

col1,col2=st.columns(2)
with col1:
    st.write('Top 10 countries with High suicide rate in males')
    chart = alt.Chart(gender_ratio[gender_ratio['sex']=='male'].head(10)).mark_bar().encode(
        x=alt.X('country',sort=None),
        y=alt.Y('suicides_no')
    )
    st.altair_chart(chart, use_container_width=True)
with col2:
    st.write('Top 10 countries with High suicide rate in females')
    chart = alt.Chart(gender_ratio[gender_ratio['sex'] == 'female'].head(10)).mark_bar().encode(
        x=alt.X('country',sort=None),
        y=alt.Y('suicides_no')
    ).interactive()
    st.altair_chart(chart, use_container_width=True)








