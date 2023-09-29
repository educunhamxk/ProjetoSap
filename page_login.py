# import streamlit as st
# from streamlit_login_auth_ui.widgets import __login__

# # Defina uma variável my_data para armazenar os dados carregados
# my_data = None

# # Defina uma função para carregar seus dados e use st.cache_data para armazená-los em cache
# @st.cache_data
# def load_data():
#     # Coloque o código para carregar seus dados aqui
#     return my_data

# # Crie uma instância do objeto de autenticação
# __login__obj = __login__(auth_token="courier_auth_token",
#                          company_name="Shims",
#                          width=200, height=250,
#                          logout_button_name='Logout', hide_menu_bool=False,
#                          hide_footer_bool=False,
#                          lottie_url='https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

# LOGGED_IN = __login__obj.build_login_ui()

# if LOGGED_IN == True:
#     # Carregue os dados usando a função de cache
#     my_data = load_data()
#     st.markdown("Your Streamlit Application Begins here!")
