#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  20 14:48:54 2020
@author: MichaelBerger
TO RUN: 
    streamlit run week13_streamlit.py
"""

import streamlit as st

import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import time



@st.cache
def load_hospitals():
    df_hospital_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_hospital_2.csv')
    return df_hospital_2

@st.cache
def load_inatpatient():
    df_inpatient_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_inpatient_2.csv')
    return df_inpatient_2

@st.cache
def load_outpatient():
    df_outpatient_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_outpatient_2.csv')
    return df_outpatient_2


st.title('MB Final Stats Assignment')
st.title('New York State Hospitals')


    
    
# FAKE LOADER BAR TO STIMULATE LOADING    
# my_bar = st.progress(0)
# for percent_complete in range(100):
#     time.sleep(0.1)
#     my_bar.progress(percent_complete + 1)
  

st.write('Welcome, *Professor!* :sunglasses:') 
  
# Load the data:     
df_hospital_2 = load_hospitals()
df_inpatient_2 = load_inatpatient()
df_outpatient_2 = load_outpatient()


hospitals_ny = df_hospital_2[df_hospital_2['state'] == 'NY']


#Bar Chart
st.subheader('Hospital Per County - NY')
bar1 = hospitals_ny['county_name'].value_counts().reset_index()
st.dataframe(bar1)

st.markdown('The majority of hospitals in NY are located in New York County or Manhattan, followed by Suffolk County')


st.subheader('With a PIE Chart:')
fig = px.pie(bar1, values='county_name', names='index')
st.plotly_chart(fig)

st.markdown('To get a better view of the Pie Chart open the full screen view')


st.subheader('Map of NY Hospital Locations')

hospitals_ny_gps = hospitals_ny['location'].str.strip('()').str.split(' ', expand=True).rename(columns={0: 'Point', 1:'lon', 2:'lat'}) 	
hospitals_ny_gps['lon'] = hospitals_ny_gps['lon'].str.strip('(')
hospitals_ny_gps = hospitals_ny_gps.dropna()
hospitals_ny_gps['lon'] = pd.to_numeric(hospitals_ny_gps['lon'])
hospitals_ny_gps['lat'] = pd.to_numeric(hospitals_ny_gps['lat'])

st.map(hospitals_ny_gps)

st.markdown('You can see that most of the Hospital Congestion is located in New York City and Long Island')

#Timeliness of Care
st.subheader('NY Hospitals - Readmission National Comparison')
bar2 = hospitals_ny['readmission_national_comparison'].value_counts().reset_index()
fig2 = px.bar(bar2, x='index', y='readmission_national_comparison')
st.plotly_chart(fig2)

st.markdown('Based on this above bar chart, we can see the majority of hospitals in the NY area fall below the national\
        average as it relates to Readmission Rates')



#Drill down into INPATIENT and OUTPATIENT just for Stony Brook & SouthSide 
st.title('STONY BROOK HOSPITAL vs SOUTHSIDE HOSPITAL')
st.title('STONY BROOK HOSPITAL')

inpatient_ny = df_inpatient_2[df_inpatient_2['provider_state'] == 'NY']

SouthSide_Hospital = inpatient_ny[inpatient_ny['provider_name'] == 'SOUTHSIDE HOSPITAL']

StonyBrook_Hospital = inpatient_ny[inpatient_ny['provider_name'] == 'UNIVERSITY HOSPITAL ( STONY BROOK )']

outpatient_ny = df_outpatient_2[df_outpatient_2['provider_state'] == 'NY']

SouthSide_Hospital_opt = outpatient_ny[outpatient_ny['provider_name'] == 'Southside Hospital']

StonyBrook_Hospital_opt = outpatient_ny[outpatient_ny['provider_name'] == 'University Hospital ( Stony Brook )']


total_inpatient_count_SouthSide = sum(SouthSide_Hospital['total_discharges'])

total_inpatient_count_StonyBrook = sum(StonyBrook_Hospital['total_discharges'])

total_inpatient_count = sum(inpatient_ny['total_discharges'])

total_outpatient_count_SouthSide = sum(SouthSide_Hospital_opt['outpatient_services'])

total_outpatient_count_StonyBrook = sum(StonyBrook_Hospital_opt['outpatient_services'])


st.header('Total Count of Discharges from Stony Brook Hospital: ' )
st.header( str(total_inpatient_count_StonyBrook) )


##Common D/C 

common_discharges = inpatient_ny.groupby('drg_definition')['total_discharges'].sum().reset_index()
common_discharges_SB = StonyBrook_Hospital.groupby('drg_definition')['total_discharges'].sum().reset_index()
common_discharges_SS = SouthSide_Hospital.groupby('drg_definition')['total_discharges'].sum().reset_index()

top10 = common_discharges.head(10)
bottom10 = common_discharges.tail(10)

top10_SS = common_discharges_SS.head(10)
bottom10_SS = common_discharges_SS.tail(10)

top10_SB = common_discharges_SB.head(10)
bottom10_SB = common_discharges_SB.tail(10)

st.header('Stony Brook Inpatient DRGs')
st.dataframe(common_discharges_SB)


col1, col2 = st.beta_columns(2)

col1.header('SB Top 10 DRGs')
col1.dataframe(top10_SB)

col2.header('SB Bottom 10 DRGs')
col2.dataframe(bottom10_SB)

st.subheader('SB Top10 PIE Chart:')
fig = px.pie(top10_SB, values='total_discharges', names='drg_definition')
st.plotly_chart(fig)

st.markdown('To get a better view of the Pie Chart open the full screen view')

StonyBrook_ny = hospitals_ny[hospitals_ny['hospital_name'] == 'SUNY/STONY BROOK UNIVERSITY HOSPITAL']

st.subheader('Stony Brook Hospital - Readmission National Comparison')
bar3 = StonyBrook_ny['readmission_national_comparison'].value_counts().reset_index()
fig2 = px.bar(bar3, x='index', y='readmission_national_comparison')
st.plotly_chart(fig2)

st.markdown('Based on this above bar chart, we can see that Stony Brook Hospital is below the national\
        average as it relates to Readmission Rates')

st.header('Total Count of Outpatient Services from Stony Brook Hospital: ' )
st.header( str(total_outpatient_count_StonyBrook) )

common_outpatient_services_SB = StonyBrook_Hospital_opt.groupby('apc')['outpatient_services'].sum().reset_index()

st.header('Stony Brook Outpatient Services')
st.dataframe(common_outpatient_services_SB)
        
st.subheader('With a PIE Chart:')
fig = px.pie(common_outpatient_services_SB, values='outpatient_services', names='apc')
st.plotly_chart(fig)
st.markdown('To get a better view of the Pie Chart open the full screen view')
     
st.title('SOUTHSIDE HOSPITAL')
st.header('Total Count of Discharges from SouthSide Hospital: ' )
st.header( str(total_inpatient_count_SouthSide) )

st.header('SouthSide Inpatient DRGs')
st.dataframe(common_discharges_SS)


col1, col2 = st.beta_columns(2)

col1.header('SS Top 10 DRGs')
col1.dataframe(top10_SS)

col2.header('SS Bottom 10 DRGs')
col2.dataframe(bottom10_SS)

st.subheader('SS Top10 PIE Chart:')
fig = px.pie(top10_SS, values='total_discharges', names='drg_definition')
st.plotly_chart(fig)

st.markdown('To get a better view of the Pie Chart open the full screen view')

SouthSide_ny = hospitals_ny[hospitals_ny['hospital_name'] == 'NS/LIJ HS SOUTHSIDE HOSPITAL']

st.subheader('SouthSide Hospital - Readmission National Comparison')
bar4 = SouthSide_ny['readmission_national_comparison'].value_counts().reset_index()
fig2 = px.bar(bar4, x='index', y='readmission_national_comparison')
st.plotly_chart(fig2)

st.markdown('Based on this above bar chart, we can see that SouthSide Hospital is below the national\
        average as it relates to Readmission Rates')
        
st.header('Total Count of Outpatient Services from SouthSide Hospital: ' )
st.header( str(total_outpatient_count_SouthSide) )

common_outpatient_services_SS = SouthSide_Hospital_opt.groupby('apc')['outpatient_services'].sum().reset_index()

st.header('SouthSide Outpatient Services')
st.dataframe(common_outpatient_services_SS)

st.subheader('With a PIE Chart:')
fig = px.pie(common_outpatient_services_SS, values='outpatient_services', names='apc')
st.plotly_chart(fig)
st.markdown('To get a better view of the Pie Chart open the full screen view')



st.title('STONY BROOK HOSPITAL vs SOUTHSIDE HOSPITAL FINAL ANALYSIS')
st.text('The hospitals had many Similarities and Differences.')
st.text('Stony Brook Hospital has Discharged almost 3x more patients than SouthSide hospital has within the time of this study.')
st.text('Although both Stony Brook and SouthSide Hospital provided almost the same number of Outpatient services to the Long Island population.')
st.text('Both Hospitals have a very poor Readmission rate as they both fall below national comparison')
st.text('Stony Brook Hospital seems to be one of the most dominant Medical Facilities in Suffolk County')