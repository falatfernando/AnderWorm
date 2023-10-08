import streamlit as st
import pandas as pd
import matplotlib as plt
import seaborn as sns

st.set_page_config(
    page_title= "AnderWorm",
    page_icon= "🪱",
    layout= "wide"
)

page_bg_img = '''
 <style>
 [data-testid="stAppViewContainer"] {
background-color: #000000;
opacity: 0.9;
background-color: #000000;
opacity: 1;
background-image:  repeating-radial-gradient( circle at 0 0, transparent 0, #000000 40px ), repeating-linear-gradient( #0f0f1155, #0f0f11 );}
 </style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)
st.sidebar.write('Our prediction model is still under development.')

st.header('Gene Expression Predictions')
st.write('Our data analysis using the current dataset reflected on no significant correlation between the variables at all.')
st.write('We are working on undestanding better the problem and metagenomics concepts.')
st.write('Out studies resulted in the correlations as displayed below.')
st.title('Correlation Matrix')
st.image('https://i.imgur.com/uzuM4jW.png', use_column_width=True)
st.write('As no significant correlations were detected between the variables, no machine learning implementation were proceeded at the present moment.')