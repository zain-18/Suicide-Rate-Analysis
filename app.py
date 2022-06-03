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

# Show total Number of Suicides
st.metric(label="Number Suicides from 1987-2016", value=Total_suicide)


# Suicide year wise
st.subheader('Suicide rate per year')
chart = alt.Chart(year_SR_df).mark_bar().encode(
  x=alt.X('year'),
  y=alt.Y('suicides_no')
)
st.altair_chart(chart, use_container_width=True)


# Suicide Rate in gender(col1) suicide rate in age group(col2)
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


# Top 10 Countries with High Suicide Rate'
st.subheader('Top 10 Countries with High Suicide Rate')
country_df=df.groupby('country')['suicides_no'].sum().reset_index()
country_df=country_df.sort_values('suicides_no',ascending=False)
chart = alt.Chart(country_df.head(10)).mark_bar().encode(
  x=alt.X('country',sort=None),
  y=alt.Y('suicides_no')
)
st.altair_chart(chart, use_container_width=True)

# Top 10 Countries with High Suicide Rate in Males and Females'
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


# year wise ratio in countries and gender
Select_year=df.groupby(['year','sex','country'])['suicides_no'].sum().reset_index().sort_values('suicides_no',ascending=False)

year_option = st.selectbox(
     'Select Year',
     sorted(df['year'].drop_duplicates()))

st.subheader('Top 10 Countries Suicide rate in '+str(year_option))

chart = alt.Chart(Select_year[Select_year['year']==year_option].head(10)).mark_bar().encode(
        x=alt.X('country',sort=None),
        y=alt.Y('suicides_no')
    ).interactive()
st.altair_chart(chart, use_container_width=True)



col1,col2=st.columns(2)
with col1:
    st.write('Top 10 countries in {} with a High suicide rate among Males'.format(year_option))
    chart = alt.Chart(Select_year[(Select_year['sex']=='male')&(Select_year['year']==year_option)].head(10)).mark_bar().encode(
        x=alt.X('country',sort=None),
        y=alt.Y('suicides_no')
    )
    st.altair_chart(chart, use_container_width=True)
with col2:
    st.write('Top 10 countries in {} with a High suicide rate among Females'.format(year_option))
    chart = alt.Chart(Select_year[(Select_year['sex']=='female')&(Select_year['year']==year_option)].head(10)).mark_bar().encode(
        x=alt.X('country',sort=None),
        y=alt.Y('suicides_no')
    )
    st.altair_chart(chart, use_container_width=True)



