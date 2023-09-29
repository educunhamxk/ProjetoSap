# import streamlit as st
# import  streamlit_toggle as tog

# def parameters_page(df):
#     st.markdown('<h1 style="font-size: 30px">(Feature em Dev)</h1>', unsafe_allow_html=True)
#     st.write("""
#              Objetivo feature: O modelo de previsão poderá receber _inputs_ e parametros de negócio, como:
#              - Incentivos fiscais
#              - Prazo de recebimento da indústria
#              - Gestão de portifólio (ciclo de vida do produto)
#              """)

import streamlit as st
import pandas as pd

def parameters_page(df):
    st.markdown('<h1 style="font-size: 30px">(Feature em Dev)</h1>', unsafe_allow_html=True)
    
    st.write("""
             Objetivo feature: O modelo de previsão poderá receber _inputs_ e parametros de negócio, como:
             - Incentivos fiscais
             - Prazo de recebimento da indústria
             - Gestão de portifólio (ciclo de vida do produto)
             """)

    st.write("---")
             
    uploaded_file = st.file_uploader("", type=['csv'], key="2")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write(df)

        st.write('---')
