import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter #untuk menghilangkan format angka ribuan
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

def sum_groupby(data, groupby, target):
    return data.groupby(groupby)[target].sum()

def template_bar_plot(data_x, data_y, title, x_label, y_label):
    plt.figure(figsize=(12, 6))
    sns.barplot(x=data_x, y=data_y, palette='Set2')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    
    st.pyplot(plt)
    
def format_Plotting(data, title, x_label, y_label, data_thick ,label_thick, thick_rotate):
    plt.figure(figsize=(15, 8))

    ax = sns.barplot(x=data.index, y=data.values, palette='Set2')

    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x):,}'))
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks(ticks=data_thick, labels=label_thick, rotation=thick_rotate)
    
    st.pyplot(plt)
    
def format_plotting_YearMonth(data, title, x_label, y_label, data_thick):
    plt.figure(figsize=(15, 8))
    ax = sns.barplot(x=data['yr'].astype(str) + '-' + data['month'].astype(str), y=data['cnt'], palette='Set2')

    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x):,}'))

    plt.title('Penyewaan bulanan 2011 s.d 2012')
    plt.xlabel('Tahun-Bulan')
    plt.ylabel('Jumlah Total (Jumlah cnt)')
    plt.xticks(rotation=90)
    plt.show()
    
    st.pyplot(plt)


    


page = 0
with st.sidebar:
    st.title('Apa yang ingin kamu lihat?')
    if st.button('Penyewaan hari aktivitas'):
        page = 0
    if st.button('Apa bulan paling banyak penyewaan?'):
        page = 1
    if st.button('Rata-Rata tertinggi penyewaan sepedah 2011 s.d 2012?'):
        page = 2
    
with st.container():
    if page == 0:
        st.title('Banyaknya penyewaan hari aktivitas pada tahun 2011 s.d 2012')
        data = pd.read_csv('./dashboard/clean_dataDay.csv')
        data = sum_groupby(data,'workingday','cnt')
        data_table = data.rename(index={0:'Lainya', 1:'Hari Aktifitas(bekerja)'})
        st.table(data_table)
        format_Plotting(data, 'Banyaknya penyewaan hari aktivitas pada tahun 2011 s.d 2012', 'Tahun-Bulan', 'Banyaknya Penyewaan', data_thick=[0,1], label_thick=['Lainya', 'Hari Aktifitas(bekerja)'], thick_rotate=0)
    if page == 1:
        st.title('Bulan paling banyak penyewaan')
        data = pd.read_csv('./dashboard/clean_dataDay.csv')
        data = sum_groupby(data, ['yr', 'month'], 'cnt')
        
        data = data.sort_values(ascending=True).reset_index()
        
        st.table(data)
        
        format_plotting_YearMonth(data, 'Penyewaan bulanan 2011 s.d 2012', 'Tahun-Bulan', 'Jumlah Total (Jumlah cnt)', data_thick=data['yr'].astype(str) + '-' + data['month'].astype(str))
    if page == 2:
        st.title('Rata-Rata tertinggi penyewaan sepedah 2011 s.d 2012')
        data = pd.read_csv('./dashboard/clean_dataHour.csv')
        
        data_sum = data.groupby('hr')['cnt'].mean()
        # table
        data_table = data_sum.reset_index()
        data_table.columns = ['Jam', 'Rata-Rata Penyewaan']
        st.table(data_table)
        
        data_thick = [i for i in range(0,24)]
        template_bar_plot(data_x = data_sum.index, data_y = data_sum.values, title = 'Rata-Rata Penyewaan Sepeda 2011 s.d 2012', x_label = 'Jam', y_label = 'Rata-Rata Penyewaan')
        
        
        