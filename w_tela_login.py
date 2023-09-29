import streamlit as st
import urllib.request

# Função para processar o login
def process_login(username, password):
    # Aqui você pode verificar as credenciais do usuário
    # Por exemplo, verificar se o nome de usuário e senha são válidos
    # Se as credenciais estiverem corretas, você pode retornar True para indicar que o usuário está logado
    # Caso contrário, retorne False
    return True

# Verifique se o usuário está logado
is_logged_in = False

# Se o usuário não estiver logado, exiba a tela de login
if not is_logged_in:
    st.title("Login")
    username = st.text_input("Nome de Usuário")
    password = st.text_input("Senha", type="password")
    login_button = st.button("Login")

    if login_button:
        # Processar o login quando o botão for clicado
        is_logged_in = process_login(username, password)

# Se o usuário estiver logado, exiba o conteúdo principal
if is_logged_in:
    # Carregar os dados
    github_csv_url = 'https://raw.githubusercontent.com/TabathaLarissa/TesteUpload/main/Mock_Data.csv'
    response = urllib.request.urlopen(github_csv_url)

    # Lê os dados CSV em um DataFrame
    import pandas as pd
    df = pd.read_csv(response)

    # Calcular o total de vendas
    total_sale = df['SALE'].sum()

    # Exibir o conteúdo principal após o login
    st.write(f"Bem-vindo, {username}!")
    st.write(f"Total de Vendas: {total_sale}")

    # Código HTML para o modal (caso ainda seja necessário)
    modal_code = """
    <div>
    <!-- Button trigger modal -->
    <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#exampleModal">
    Hydralit Components Experimental Demo!
    </button>

    <!-- Modal -->
    <div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog" role="document">
    <div class="modal-content">
    <div class="modal-header">
    <h5 class="modal-title" id="exampleModalLabel">Modal Popup Form!</h5>
    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
        <span aria-hidden="true">&times;</span>
    </button>
    </div>
    <div class="modal-body">
    <div class="container">
    <h2>Pure JS+HTML Form</h2>
    <form class="form-horizontal" action="/">
    <div class="form-group">
    <label class="control-label col-sm-2" for="email">Email:</label>
    <div class="col-sm-10">
    <input type="email" class="form-control" id="email" placeholder="Enter email" name="email">
    </div>
    </div>
    <div class="form-group">
    <label class="control-label col-sm-2" for="pwd">Password:</label>
    <div class="col-sm-10">          
    <input type="password" class="form-control" id="pwd" placeholder="Enter password" name="pwd">
    </div>
    </div>
    <div class="form-group">        
    <div class="col-sm-offset-2 col-sm-10">
    <div class="checkbox">
        <label><input type="checkbox" name="remember"> Remember me</label>
    </div>
    </div>
    </div>
    <div class="form-group">        
    <div class="col-sm-offset-2 col-sm-10">
    <button type="submit" class="btn btn-default">Submit</button>
    </div>
    </div>
    </form>
    </div>
    </div>
    <div class="modal-footer">
    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
    <button type="button" class="btn btn-primary">Save changes</button>
    </div>
    </div>
    </div>
    </div>
    </div>
    """
    # Apresentar o modal usando o código HTML (se necessário)
    st.markdown(modal_code, unsafe_allow_html=True)

    # Obter parâmetros de consulta (se necessário)
    query_param = st.experimental_get_query_params()
    if query_param:
        st.write('We captured these values from the experimental modal form using JavaScript + HTML + Streamlit + Hydralit Components.')
        st.write(query_param)
