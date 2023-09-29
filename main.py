import streamlit as st
from page_analytics import dashboard_page
from page_predict import predict_page
from page_call_to_action import call_to_action_page
from page_parameters import parameters_page
from page_feedback import feedback_page
from dataframe import df
import pandas as pd
import streamlit as st
#from streamlit_option_menu import option_menu

# Defina o tamanho da tela da web e o título
st.set_page_config(
    page_title="Stock ON Dashboard",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="expanded"
)

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

with st.sidebar:
    st.image("StockON.png")
    
    options = ['Analytics', 'Modelo de Previsão', 'Call to Action', 'Parâmetros', 'Feedback', 'Logoff']
    selected = st.selectbox('', options, index=0)
 
if selected == 'Analytics':
    dashboard_page(df)
elif selected == 'Modelo de Previsão':
    predict_page(df)
elif selected == "Call to Action":
    call_to_action_page(df)
elif selected == 'Parâmetros':
    parameters_page(df)
elif selected == 'Feedback':
    feedback_page(df)
elif selected == 'Logoff':
    "Gerenciamento de acesso em desenvolvimento."

# Executar o aplicativo
if __name__ == '__main__':
    st.set_option('deprecation.showPyplotGlobalUse', False)
