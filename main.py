import os

# For Webapp
import streamlit as st
st.set_option('deprecation.showPyplotGlobalUse', False)

# For EDA
import pandas as pd
import numpy as np

# For Plots
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
matplotlib.use('Agg')

def main():

    st.title("Exploratory Data Analysis")


    st.sidebar.title("Visualization Settings")
    st.sidebar.subheader('Upload Dataset')
    dataset=st.sidebar.file_uploader(label="Upload your csv file.")


    # Read Dataset and Display Columns, shape, Values
    if dataset:
        data=pd.read_csv(dataset)
        
        st.sidebar.header("Options :")

        if st.sidebar.checkbox("Show Dataset"):
            st.subheader("About Dataset")
            num=st.number_input("Select number of Rows",5,key='show_dataset')

            st.dataframe(data.head(num))

            left, right = st.beta_columns(2)
            with left: 
                if st.checkbox("Column Names"):
                    st.write(data.columns)
            with right:
                if st.checkbox("Shape of Dataset"):
                    st.write("Rows :",data.shape[0])
                    st.write("Columns :",data.shape[1])
            
            if st.checkbox("Data Types"):
                st.write(data.dtypes)
                
        # Seprate View, value Count

        if st.sidebar.checkbox("Select Colums to view"):
            all_columns=data.columns.tolist()
            selected_columns=st.multiselect("Select",all_columns)
            n=st.number_input("Select number of observation to view",5,key='observations')
            new_data=data[selected_columns]
            st.dataframe(new_data.head(n))    

            if st.button("Target Value Counts"):
                st.text("Value Count")
                st.write(""" **Note :** For Value Count only first column name for multicolumn will be selected """)
                selected=selected_columns[0]
                st.write(data.loc[:,selected].value_counts())

        # Summary

        if st.sidebar.checkbox("Summary"):
            st.subheader("Summary")
            st.write("For Numerical Data")
            st.write(data.describe().T)
            st.write("For Object")
            st.write(data.describe(include='object').T)

        # Plots
        if st.sidebar.checkbox("Plots"):
            st.subheader("Data Visualization")

            # HeatMap
            st.subheader("Heat Map")
            st.write(sns.heatmap(data.corr(),annot=True))
            st.pyplot()

            # Count Plot
            if st.checkbox("Count Plot"):
                st.subheader("Count Plot")
                st.text("Value Counts By Target")
                all_columns_name=data.columns.tolist()
                primary_col=st.selectbox("Select Column to Group By",all_columns_name)
                selected_columns_name=st.multiselect("Select Columns",all_columns_name)
                if st.button("Plot",key='cp'):
                    if selected_columns_name:
                        valuecount_plot=data.groupby(primary_col)[selected_columns_name].count()
                    else:
                        valuecount_plot=data.iloc[:,-1].value_counts()
                    st.write(valuecount_plot.plot(kind='bar'))
                    st.pyplot()

            # Custom Plot
            if st.checkbox("Custom Plots"):
                st.subheader("Custom Plots")
                all_columns_name=data.columns.tolist()
                types=st.selectbox("Select Plot type",['Area Plot','Bar Plot','Line Plot','Histogram','Box Plot','KDE','Pie Plot'])
                selected_columns_name=st.multiselect("Select Columns To Plot",all_columns_name)

                if st.button("Plot"):
                    st.success("{} for {}".format(types,selected_columns_name))

                    if types=='Area Plot':
                        cust_data=data[selected_columns_name]
                        st.area_chart(cust_data)
                    elif types=='Bar Plot':
                        cust_data=data[selected_columns_name]
                        st.bar_chart(cust_data)
                    elif types=='Line Plot':
                        cust_data=data[selected_columns_name]
                        st.line_chart(cust_data)

                    elif types=="Histogram":
                        cust_data=data[selected_columns_name].plot(kind='hist')
                        st.pyplot()
                    
                    elif types=="KDE":
                        cust_data=data[selected_columns_name].plot(kind='kde')
                        st.pyplot()
                    
                    elif types=="Pie Plot":
                        selected=selected_columns_name[0]
                        st.write(""" **Note :** For Pie Plot only first column name for multicolumn will be selected """)
                        cust_data=data.loc[:,selected].value_counts().plot.pie()
                        st.pyplot()

    else:
        st.subheader("A simple Dataset Exploratory Webapp")
        st.text("")
        st.text("")
        st.subheader("""    **Note :**   """)
        st.write("1. Only csv file are accepted as input")
        st.write("2. For value count and pie plot only first column name for multicolumn will be selected")
        st.write("3. For large datasets it may take time to load it")
        st.write("4. The plots can be downloaded in 'SVG' and 'PNG' format ")
        st.write("")

 

    
 
if __name__=="__main__":
    main()





