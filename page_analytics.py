import pandas as pd
import streamlit as st
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import random
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.patches as patches

def dashboard_page(df):

    # Adicione o estilo CSS para o card
    st.markdown("""
    <style>
    .card {
        border: 1px solid #f0f0f0;
        border-radius: 5px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 1rem;
        background-color: white;
        height: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("Dashboard de Estoque")
    #Gráfico 1
    estoque_atual_lista = []

    df_produtos = pd.read_csv("df_produtos.csv")
    df_estoque = pd.read_csv("df_estoque.csv")
    df_estoque_minimo = pd.read_csv("df_estoque_minimo.csv")
    df_lead_times = pd.read_csv("df_lead_times.csv")
    previsoes = pd.read_csv("previsoes.csv")
    demanda = []
    
    

    for produto_id in df_produtos['Produto_ID'].unique():
        estoque_atual = df_estoque[df_estoque['Produto_ID'] == produto_id]['Quantidade_Estoque'].values[-1] * 30
        estoque_atual_lista.append(estoque_atual)
        lead_time = df_lead_times[df_lead_times['Produto_ID'] == produto_id]['Lead_Time_Dias'].mean()
        demanda_durante_lead_time = sum(previsoes[str(produto_id)][:int(lead_time)-1])
        demanda.append([produto_id, demanda_durante_lead_time])

    df_demanda_lead_time = pd.DataFrame(demanda, columns=['Produto_ID', 'Demanda_Durante_Lead_Time'])
    df_produtos['Estoque_Atual'] = estoque_atual_lista
    df_comparacao = pd.merge(df_produtos, df_estoque_minimo, on='Produto_ID')
    df_comparacao = pd.merge(df_comparacao, df_demanda_lead_time, on='Produto_ID')
    df_comparacao['Produto_ID'] = df_comparacao['Produto_ID'].astype(str)


    #1)
    # Calculando a porcentagem de produtos acima do estoque mínimo
    produtos_acima_minimo = df_comparacao[df_comparacao['Estoque_Atual'] > df_comparacao['Estoque_Minimo']].shape[0]
    total_produtos = df_comparacao.shape[0]
    percentage = 100 - ((produtos_acima_minimo / total_produtos) * 100)

    #2)
    # Calculando a eficiência
    total_estoque_atual = df_comparacao['Estoque_Atual'].sum()
    total_estoque_minimo = df_comparacao['Estoque_Minimo'].sum()
    # Se o total do estoque atual for igual ao estoque mínimo, a eficiência é 100%
    # Se o total do estoque atual for o dobro do estoque mínimo, a eficiência é 50%
    # Eficiência é definida como (total do estoque mínimo / total do estoque atual) * 100
    eficiencia_estoque = (total_estoque_minimo / total_estoque_atual) * 10

    #3)
    # Cruzando as informações usando Produto_ID
    # Primeiro, vamos ordenar o df_estoque pela coluna Data.
    df_estoque = df_estoque.sort_values(by='Data', ascending=True)

    # Pegando o último registro de cada Produto_ID
    df_estoque_ultimo = df_estoque.drop_duplicates(subset='Produto_ID', keep='last')
    df_completo = pd.merge(df_estoque_minimo, df_estoque_ultimo, on='Produto_ID', how='left')
    df_completo = pd.merge(df_completo,df_produtos, on='Produto_ID', how='left')

    # 1. Calculando a quantidade descoberta de estoque
    df_completo['Quantidade_Descoberta'] = df_completo['Estoque_Minimo'] - df_completo['Quantidade_Estoque']
    # Mantemos apenas os valores onde a Quantidade_Descoberta é positiva (indicando uma falta real)
    df_completo['Quantidade_Descoberta'] = df_completo['Quantidade_Descoberta'].apply(lambda x: x if x > 0 else 0)

    # 2. Calculando a perda estimada por produto
    df_completo['Valor_Venda'] = df_completo['Custo_Unitario'] * 1.25
    df_completo['Perda_Estimada'] = df_completo['Quantidade_Descoberta'] * df_completo['Valor_Venda']

    # 3. Somando todas as perdas estimadas para obter a perda total
    perda_total = df_completo['Perda_Estimada'].sum()


    col1, col2, col3 = st.columns(3)
    with col1:
        percentage_display = "{:,.0f}%".format(percentage)
        change = "-2,5%"
        custom_metric_html = f"""
            <div style="border: 1px solid lightgray; padding: 10px; border-radius: 5px; text-align: center;">
                <p style="font-size: 16px; margin-bottom: 10px;">% Produtos abaixo do estoque mín.</p>
                <h2 style="margin: 0;">{percentage_display}</h2>
                <p style="color: {'red' if '-' in change else 'green'};">{change}</p>
            </div>
        """
        st.markdown(custom_metric_html, unsafe_allow_html=True)
        
        # st.markdown("""
        #     <hr style='border:1px solid "#808080"; background-color: #808080; height:1px; text-align: center;'>
        # """, unsafe_allow_html=True)
    
    # st.markdown("""
    #     <hr style='border:1px solid "#808080"; background-color: #808080; height:1px;'>
    # """, unsafe_allow_html=True)
    with col2:
        percentage_display = "{:,.0f}%".format(eficiencia_estoque)
        change = "-4,5%"
        custom_metric_html = f"""
            <div style="border: 1px solid lightgray; padding: 10px; border-radius: 5px; text-align: center;">
                <p style="font-size: 16px; margin-bottom: 10px;">% Eficiência do Estoque</p>
                <h2 style="margin: 0;">{percentage_display}</h2>
                <p style="color: {'red' if '-' in change else 'green'};">{change}</p>
            </div>
        """
        st.markdown(custom_metric_html, unsafe_allow_html=True)
        
        # st.markdown("""
        #     <hr style='border:1px solid "#808080"; background-color: #808080; height:1px; text-align: center;'>
        # """, unsafe_allow_html=True)
    with col3:
        number_display = "R$ {:,.0f}".format(perda_total)
        change = "-4,5%"
        custom_metric_html = f"""
            <div style="border: 1px solid lightgray; padding: 10px; border-radius: 5px; text-align: center;">
                <p style="font-size: 16px; margin-bottom: 10px;">Perda Estimada com Ruptura</p>
                <h2 style="margin: 0;">{number_display}</h2>
                <p style="color: {'red' if '-' in change else 'green'};">{change}</p>
            </div>
        """
        st.markdown(custom_metric_html, unsafe_allow_html=True)
        
        # st.markdown("""
        #     <hr style='border:1px solid "#808080"; background-color: #808080; height:1px; text-align: center;'>
        # """, unsafe_allow_html=True)



    def plot_graph(df_comparacao):
        fig, ax = plt.subplots(figsize=(18, 6))

        # Defina uma largura para as barras
        bar_width = 0.3

        # Crie uma lista de posições no eixo x para cada barra
        x_positions = np.arange(len(df_comparacao['Nome_Produto']))

        # Primeiro, plotamos o Estoque Mínimo como base
        bars2 = ax.bar(x=x_positions, height=df_comparacao['Estoque_Minimo'], width=bar_width, label='Estoque Mínimo', alpha=0.5, color='#d45071', edgecolor='black')

        # Em seguida, plotamos o Estoque Atual com um deslocamento
        bars1 = ax.bar(x=x_positions + bar_width - 0.05, height=df_comparacao['Estoque_Atual'], width=bar_width, label='Estoque Atual', alpha=0.6, color='#509bd4', edgecolor='black')

        # Por fim, plotamos a Projeção Vendas com outro deslocamento
        bars3 = ax.bar(x=x_positions + 2*(bar_width - 0.05), height=df_comparacao['Demanda_Durante_Lead_Time'], width=bar_width, label='Projeção Vendas', alpha=0.5, color='orange', edgecolor='black')

        # Ajusta os rótulos do eixo x para alinhar corretamente com as barras
        ax.set_xticks(x_positions + bar_width)
        ax.set_xticklabels(df_comparacao['Nome_Produto'], fontsize=17)

        #plt.ylabel('Quantidade de Estoque', fontsize=14, fontweight='bold')
        plt.title('Estoque Atual x Estoque Mínimo e Projeção de Vendas', fontsize=22,loc='center')
        plt.legend(loc="upper right", fontsize=16)
        plt.yticks(fontsize=14)
        plt.xlabel('')

        sns.despine(left=True, bottom=True)  # Remove as linhas do eixo
        
        # Adicionar caixa ao redor do gráfico
        for spine in ax.spines.values():
            spine.set_edgecolor('lightgray')
            spine.set_linewidth(1)
        
        plt.tight_layout()
        plt.show()

        #return plt

    # Usando o Streamlit para exibir o gráfico


    # Dividindo a página em duas colunas com proporções 1:4
    # col1, col2 = st.columns([1, 4])

    # Gráfico de progresso dentro do card
    # with col1:

    # Gráfico de comparação dentro do card
    # with col2:
    st.markdown("")
    fig = plot_graph(df_comparacao)
    st.pyplot(fig)
    st.write('#### Análise ChatGPT')
    st.write("""
            Os produtos feijão, açúcar e óleo estão bem abaixo do estoque mínimo e da projeção de vendas. Para o macarrão estamos abaixo do estoque mínimo mas segundo as projeções de vendas vai ser o suficiente para atender a demanda para os próximos dias. Para os demais produtos há muita ineficiência de estoque com quantidades exageradas em relação a demanda histórica e a projeção. Recomendamos que as sugestões de compra sejam efetuadas para os produtos com risco de ruptura para evitar a perda de R$455k.               
            """)

    # Chamada da função


    df['Ruptura'] = (df['BREAK'] / df['SALE'])

    total_sale = df['SALE'].sum()
    total_stock = df['STOCK'].sum()
    total_break = df['BREAK'].sum()
    total_ruptura = df['Ruptura'].sum()




    # Filtros 
    with st.expander("Filtros", expanded=False):

        df['DATE'] = pd.to_datetime(df['DATE'])
        date = df['DATE'].dt.strftime('%Y-%m-%d').unique().tolist()
        
        categories = df['CATEGORY'].unique().tolist()  
        regioes = df['REGIAO'].unique().tolist()        
        uf = df['UF'].unique().tolist()        
        skus = df['SKU'].unique().tolist()
        
        col_date, col_category, col_regioes, col_uf, col_sku = st.columns(5)  # Cria 5 colunas
        
        selected_date = col_date.selectbox('Data:', ['Todas'] + date)
        selected_category = col_category.selectbox('Categoria:', ['Todas'] + categories)
        selected_regioes = col_regioes.selectbox('Regiao:', ['Todas'] + regioes)
        selected_uf = col_uf.selectbox('UF:', ['Todas'] + uf)
        selected_sku = col_sku.selectbox('SKU:', ['Todos'] + skus)

        if selected_category != 'Todas':
            df = df[df['CATEGORY'] == selected_category]

        if selected_date != 'Todas':
            df = df[df['DATE'] == selected_date]

        if selected_regioes != 'Todas':
            df = df[df['REGIAO'] == selected_regioes]

        if selected_uf != 'Todas':
            df = df[df['UF'] == selected_uf]

        if selected_sku != 'Todos':
            df = df[df['SKU'] == selected_sku]

    df['DATE'] = pd.to_datetime(df['DATE'])
    df_monthly = df.resample('M', on='DATE').sum()

    # Combinando dois graficos
    fig = go.Figure()

    # Adiciona o gráfico de barras com a cor azul clara
    fig.add_trace(go.Bar(x=df_monthly.index.strftime('%Y-%m'), y=df_monthly['SALE'], name='Vendas', marker=dict(color='lightblue')))

    # Adiciona o gráfico de linha com a cor azul escuro e com marcadores
    fig.add_trace(go.Scatter(x=df_monthly.index.strftime('%Y-%m'), y=df_monthly['STOCK'], mode='lines+markers', name='Estoque', line=dict(color='gray'), marker=dict(color='gray')))

    fig.update_xaxes(type='category', tickformat='%b %Y', title='')
    fig.update_layout(
        height=500,
        width=200,
        title="",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown('#### Vendas vs Estoque', unsafe_allow_html=True)
        fig.update_layout(margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.write('#### Análise ChatGPT')
        st.write("""
                O volume de estoque tem aumentado consideravelmente por conta da queda nas vendas, com isso os números de ruptura também foram reduzidos e a expectativa para os próximos 3 meses é de queda na demanda e na ruptura.               
                """)
        # Campo de chat input # Apenas para simular o espaço do ChatGPT
        st.write('---')
        st.write('#### Pergunte sobre os dados ao ChatGPT')
        prompt = st.text_input("Digite abaixo")  
        if prompt:
            st.write(f"Resposta: {prompt}")

    st.write('---')

    col3, col4 = st.columns([3, 3])
    # Preparando os dados para a regressão linear
    monthly_sales = df.groupby(df['DATE']).sum()['Ruptura'].reset_index()
    X = np.array(range(len(monthly_sales))).reshape(-1, 1)
    y = monthly_sales['Ruptura']

    model = LinearRegression()
    model.fit(X, y)

    # Previsão para os próximos 3 meses
    next_3_months = np.array(range(len(monthly_sales), len(monthly_sales) + 3)).reshape(-1, 1)
    rupture_forecast = model.predict(next_3_months)

    # Adicionando as previsões ao DataFrame
    for i in range(3):
        new_date = monthly_sales['DATE'].iloc[-1] + pd.DateOffset(months=1)
        monthly_sales = monthly_sales.append({'DATE': new_date, 'Ruptura': rupture_forecast[i]}, ignore_index=True)

    # Adicionar uma coluna de tipo (Real ou Projetado)
    monthly_sales['Type'] = ['Real' if i < len(monthly_sales) - 3 else 'Projetado' for i in range(len(monthly_sales))]

    # Plotando o gráfico de barras
    with col3:
        st.write("#### Ruptura (%) e Projeção")

        fig_break = px.bar(monthly_sales, 
                            x=monthly_sales['DATE'].dt.strftime('%Y-%m'), 
                            y='Ruptura', 
                            labels={'x': 'Mês', 'Ruptura': ''}, 
                            color='Type',
                            color_discrete_map={"Real": "blue", "Projetado": "lightblue"})
        fig_break.update_layout(
            height=500,
            width=200,
            title="",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
            )
        st.plotly_chart(fig_break, use_container_width=True)
    with col4:
        #Projeção vendas
        # Agrupando vendas por mês
        monthly_sales = df.groupby(df['DATE']).sum()['SALE'].reset_index()

        # Preparando dados para regressão linear
        X = np.array(range(len(monthly_sales))).reshape(-1, 1)
        y = monthly_sales['SALE']

        # Ajustando o modelo
        model = LinearRegression().fit(X, y)

        # Prevendo os próximos 3 meses
        future_months = np.array(range(len(monthly_sales), len(monthly_sales) + 3)).reshape(-1, 1)
        predictions = model.predict(future_months)

        # Adicionando as previsões ao dataframe
        for i, prediction in enumerate(predictions):
            next_month = monthly_sales['DATE'].iloc[-1] + pd.DateOffset(months=1)
            monthly_sales = monthly_sales.append({'DATE': next_month, 'SALE': prediction}, ignore_index=True)
        
        st.write("#### Previsão de Demanda (Qtd e produto)")
        # Separando os dados reais e as projeções
        actual_data = monthly_sales[:-3]
        projection_data = monthly_sales[-4:]  # Inclui o último mês de dados reais na projeção

        # Plotando as vendas reais
        fig_total_sale = go.Figure(go.Scatter(x=actual_data['DATE'], y=actual_data['SALE'], mode='lines', name='Vendas Reais'))

        # Adicionando as projeções com linha pontilhada
        fig_total_sale.add_trace(go.Scatter(x=projection_data['DATE'], y=projection_data['SALE'], mode='lines', name='Projeção', line=dict(dash='dash')))

        # Ajustando o eixo y para começar de zero
        fig_total_sale.update_layout(
            yaxis=dict(range=[0, max(monthly_sales['SALE'])*1.1]),  # *1.1 para dar um pouco de espaço acima do valor máximo
            legend=dict(
                xanchor="center",
                x=0.5,
                yanchor="bottom", # "bottom" means the y position is given in terms of the bottom of the legend
                y=1.05            # Positioning it just above the graph
            ),
            margin=dict(t=10, b=10, l=10, r=10)
        )
        st.plotly_chart(fig_total_sale, use_container_width=True)
