from time import strptime
import pandas as pd
import streamlit as st
def do_stuff_on_page_load():
    st.set_page_config(layout="wide", page_title="VEAS BG")
do_stuff_on_page_load()
from datetime import date, datetime, timedelta

from urllib.error import URLError
import numpy as np
import matplotlib.pyplot as plt
import typing_extensions
import pyjokes
import jokes
import os
import time
from os.path import getmtime
from openexchangerate import OpenExchangeRates
from other import other
from get_invent_3021 import invent_opis_3021
from get_invent_303 import invent_opis_303
import xlsxwriter
import xlrd
import plotly.express as px
import base64
from io import BytesIO, StringIO
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from  PIL import Image
import io
import itertools
from st_aggrid import AgGrid, GridUpdateMode, GridOptionsBuilder, JsCode
from isoweek import Week
dnes = datetime.today().strftime('%d.%m.%Y')
dnes_weekday = datetime.today().strftime('%A')
dnes_weekday_bg = {'Monday': 'Понеделник', 'Tuesday': 'Вторник', 'Wednesday': 'Сряда', 'Thursday': 'Четвъртък', 'Friday': 'Петък', 'Saturday': 'Събота', 'Sunday': 'Неделя'}
den = dnes_weekday_bg[dnes_weekday]


with st.sidebar:
    choose = option_menu(f'{dnes}, {den}', ['Портфейл на поръчките'],
                         icons=['paperclip','paperclip','paperclip'],
                         menu_icon="calendar3", default_index=0,
                         styles={
        "st": {"padding": "5!important", "background-color": "#F0F2F6"},
        "icon": {"color": "black", "font-size": "20px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#fff"},
        "nav-link-selected": {"background-color": "#FF4B4B"},
    }
    )


st.markdown(""" <style> .font {font-size:30px ; font-family: 'Century Gothic'; color: #777777;}</style> """, unsafe_allow_html=True)
st.markdown(""" <style> .font2 {font-size:13px ; font-family: 'Century Gothic';}</style> """, unsafe_allow_html=True)
st.markdown(""" <style> .font3 {font-size:13px ; font-family: 'Century Gothic'; color: #031891;}</style> """, unsafe_allow_html=True)


# file_POO = 'sdzu.csv'
# @st.cache(allow_output_mutation=True)
# def load_sales():
#     df_sales = pd.read_csv(file_POO)
#     return df_sales

if choose == 'Портфейл на поръчките':
    @st.cache(allow_output_mutation=True)
    def load_sales():
        df_sales = pd.read_csv(file_POO)
        return df_sales
    
    st.write('<p class="font">Портфейл на поръчките</p>', unsafe_allow_html=True)

    file_POO = st.file_uploader("Избери CSV файла с продажбите:", type=["csv"])
    

    
    if file_POO is not None:

        df_sales = load_sales()


        df_sales['Invoice Date'] = pd.to_datetime(df_sales['Invoice Date'].astype(str), dayfirst=True)
        df_sales['Invoice Date'] = df_sales['Invoice Date'].dt.date

        

        # AgGrid(df_sales, fit_columns_on_grid_load=False, height=400)

        contract = list(set(df_sales['Contract']))
        prod_codes = list(set(df_sales['Prod Code Descript']))


        prod_codes = [x for x in prod_codes if str(x) != 'nan']

        
        # todays week number
        week_number = datetime.today().isocalendar()[1]
        # previous week number
        prev_week_number = week_number - 1

        # # show start date and end date of the previous week
        # start_date_prev_week = datetime.today() - timedelta(days=datetime.today().weekday()) - timedelta(days=7)
        # end_date_prev_week = datetime.today() - timedelta(days=datetime.today().weekday()) - timedelta(days=1)

        with st.form(key='my_form'):

            # # st input week number
            week_number_entered = st.number_input('Избери седмица', value=prev_week_number, min_value=1, max_value=52)
            # if week_number_entered changes then update the start and end date of the previous week
        
            start_date = Week(2022, week_number_entered).monday()
            end_date = Week(2022, week_number_entered).sunday()
            # st.write(start_date, end_date)

            # w = Week(2022,week_number_entered)
            # start_date = Week(w).monday()
            # end_date = Week(w).sunday()


            # start_date = datetime.today() - timedelta(days=datetime.today().weekday()) - timedelta(days=7)
            # end_date = datetime.today() - timedelta(days=datetime.today().weekday()) - timedelta(days=1)

            #start_date to date
            # start_date = start_date.date()
            # end_date = end_date.date()

            selected_dates = [start_date, end_date]
            #aggrid table with df_sales with selected dates
            # AgGrid(df_sales[(df_sales['Invoice Date'] >= start_date) & (df_sales['Invoice Date'] <= end_date)], fit_columns_on_grid_load=False, height=400)

            contract_filter = st.selectbox('Избери дружество', contract)
            prod_code = st.multiselect('Избери продукт', prod_codes, default=['Finished product'])

            df_sales_filtered = df_sales[(df_sales['Invoice Date'] >= start_date) & (df_sales['Invoice Date'] <= end_date) & (df_sales['Contract'] == contract_filter)]
            invoice_no_list = set(df_sales_filtered['Invoice No'])

            df_sales_filtered = df_sales_filtered[df_sales_filtered['Prod Code Descript'].isin(prod_code)]

            submitted = st.form_submit_button("Submit")

            if submitted:
                
                # remove index column from the filtered df_sales and add columns name to the df_sales_filtered
                df_sales_filtered.reset_index(drop=True, inplace=True)
                # create nwe dataframe from the filtered df_sales with columns name from the df_sales_filtered
                df_sales_filtered = df_sales_filtered[df_sales_filtered.columns.values]
                

                # df_sales_filtered[['Invoice Date to list
                # Invoice Date to list
                # invoice_no_list = set(df_sales_filtered['Invoice No'])
                invoice_no_list = list(invoice_no_list)
                invoice_no_list.sort()
                st.write(f'Седмица **{week_number_entered}** от **{start_date}** до **{end_date}**')
                st.write(f'Номера на фактурите (преди филтър "Избери продукт"): **{invoice_no_list}**'.replace('[', '').replace(']', ''))
                # check if items in invoice_no_list are consecutive numbers
                broi = len(invoice_no_list)
                counter = 0
                for i in range(0,broi-1):
                    if invoice_no_list[i+1]- invoice_no_list[i] == 1:
                        counter += 1
                if counter == broi-1:
                    st.success(f'**Номерата на фактурите (преди филтър "Избери продукт") са последователни!**')
                else:
                    st.warning(f'**Номерата на фактурите (преди филтър "Избери продукт") са непоследователни!**')




                df_sales_pivot = pd.pivot_table(df_sales_filtered, values=['Invoiced Qty', 'Delivery Price Own Curr'], index=['Commodity 2', 'Contract'], aggfunc=np.sum, margins=True, margins_name='Total', fill_value=0)


                df_sales_pivot = df_sales_pivot.reset_index()
                
                # round numbers in pivot table to 0 decimals 
                for i in range(len(df_sales_pivot.columns)):
                    if i != 0 and i != 1:
                        df_sales_pivot[df_sales_pivot.columns[i]] = round(df_sales_pivot[df_sales_pivot.columns[i]].astype(float), 0)

                #change position of columns in pivot table
                df_sales_pivot = df_sales_pivot[['Contract', 'Commodity 2', 'Invoiced Qty', 'Delivery Price Own Curr']]
                
                projects_dict_veas = {'VPHBG':'Philips','VEBBG':'EBM','VGRBG':'Grasslin','VSIBG':'Osram Siteco', 'VBLBG':'Osram Backled'}
                projects_dict_vtbh = {}
                projects_dict_vtbp = {}

                for i in df_sales_pivot['Commodity 2']:	
                    #change values in column 'Commodity 2' to projects_dict values if not == 'Total'
                    if i != 'Total':
                        if contract_filter == 'EASBG':
                            # pivot table with EASBG projects only and 'Commodity 2'] == i
                            df_sales_pivot.loc[df_sales_pivot['Commodity 2'] == i, 'Contract'] = projects_dict_veas[i]
                            # change column names df_sales_pivot 
                
                
                
                df_sales_pivot.rename(columns={'Contract':'Project'}, inplace=True)
            

                AgGrid(df_sales_pivot, fit_columns_on_grid_load=True, height=200)                                                                      
                AgGrid(df_sales_filtered, fit_columns_on_grid_load=False, height=400)
           


