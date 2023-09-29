from dataframe import df
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def call_to_action_page(df):
    st.markdown('<h1 style="font-size: 30px">(Feature em Dev)</h1>', unsafe_allow_html=True)
    st.write('#### Requisição de Compra ou Rebalanceamento de Estoque')

    # Agrupando e somando a quantidade total por CATEGORY
    grouped = df.groupby("CATEGORY").agg({
        "Qtd repo estoque": sum
    }).reset_index()

    # Convertendo a coluna para int para remover decimais
    grouped["Qtd repo estoque"] = grouped["Qtd repo estoque"].astype(int)

    # Crie colunas baseadas no número de categorias
    cols = st.columns(len(grouped))

    # Definindo dados fictícios para as métricas
    suggestions_data = {
        "Redução de Perda": ("25%", "+3%"),
        "Eficiência no Giro de Estoque": ("2x", "+5%"),
        "Economia em Compras": ("R$10,000", "+7%"),
        "Satisfação do Cliente": ("90%", "+2%")
    }

    # Criando colunas para os big numbers
    cols = st.columns(4)

    # Iterando pelos dados e criando os big numbers com subindicadores
    for index, (metric_name, values) in enumerate(suggestions_data.items()):
        principal_value, variation = values
        cols[index].metric(metric_name, principal_value, variation)

    st.write('---')
    
    st.write('### Ações Recomendadas vs Realizadas')

    # Dados
    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro']
    acoes_recomendadas = [10, 12, 15, 14, 9, 8, 11, 13, 10]
    acoes_realizadas = [8, 11, 14, 10, 7, 6, 9, 11, 9]

    # Criando o DataFrame
    dfa = pd.DataFrame({
        'Mês': meses,
        'Qte Ações recomendadas': acoes_recomendadas,
        'Qtd Ações realizadas': acoes_realizadas
    })

    # Criando o gráfico de barras
    fig = go.Figure()

    # Adicionando ações recomendadas ao gráfico
    fig.add_trace(go.Bar(
        x=dfa['Mês'],
        y=dfa['Qte Ações recomendadas'],
        name='Ações Recomendadas'
    ))

    # Adicionando ações realizadas ao gráfico
    fig.add_trace(go.Bar(
        x=dfa['Mês'],
        y=dfa['Qtd Ações realizadas'],
        name='Ações Realizadas'
    ))

    # Atualizando o layout do gráfico
    fig.update_layout(
        title='',
        xaxis_title='Mês',
        yaxis_title='Quantidade de Ações',
        barmode='group',
        autosize=True,
        legend=dict(
            x=0.5,
            y=1.2,
            xanchor='center',
            orientation='h'
        )
    )

    # Mostrando o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)


    st.write('---')

    st.write('### Método de Aprovação')
    approval_method = st.selectbox('Escolha:', ['Selecione...', 'por Categoria', 'por SKU'])

    if approval_method == 'por Categoria':
        st.write('Selecione as categorias que deseja aprovar.')
        categories = df["CATEGORY"].unique()

        if "category_index" not in st.session_state:
            st.session_state.category_index = 0
        
        # Verificar se o índice da categoria está fora dos limites
        if st.session_state.category_index >= len(categories):
            st.session_state.category_index = 0

        current_category = categories[st.session_state.category_index]
        st.write(f'**Categoria:** {current_category}')
        
        # Convertendo 'Qtd repo estoque' para valor positivo
        repo_value = abs(grouped[grouped["CATEGORY"] == current_category]["Qtd repo estoque"].values[0])
        st.write(f'**Qtd repo estoque:** {repo_value}')

        st.write("Você aprova esta categoria?")
        col1, col2 = st.columns(2)
        if col1.button('Sim'):
            if "approved_categories" not in st.session_state:
                st.session_state.approved_categories = []
            st.session_state.approved_categories.append(current_category)
            st.session_state.category_index += 1
            st.success(f'{current_category} aprovado e enviado ao ERP SAP.')
            
        if col2.button('Não'):
            st.session_state.category_index += 1
            st.write('Não aprovado.')

        if st.session_state.category_index < len(categories):
            st.button('Próximo')

    elif approval_method == 'por SKU':
        if "sku_index" not in st.session_state:
            st.session_state.sku_index = 0

        # Verificar se o índice do SKU está fora dos limites
        if st.session_state.sku_index >= df.shape[0]:
            st.session_state.sku_index = 0

        current_sku = df.iloc[st.session_state.sku_index]
        st.write(f"**SKU:** {current_sku['SKU']}")
        st.write(f"**Categoria:** {current_sku['CATEGORY']}")
        st.write(f"**FORECAST 30D:** {current_sku['FORECAST 30D']}")
        st.write(f"**FORECAST 60D:** {current_sku['FORECAST 60D']}")
        st.write(f"**STOCK:** {current_sku['STOCK']}")
        st.write(f"**BREAK:** {current_sku['BREAK']}")
        
        # Convertendo 'Qtd repo estoque' para valor positivo
        repo_sku_value = abs(current_sku['Qtd repo estoque'])
        st.write(f"**Qtd repo estoque:** {repo_sku_value}")

        st.write("Você aprova este SKU?")
        col1, col2 = st.columns(2)
        if col1.button('Sim'):
            if "approved_skus" not in st.session_state:
                st.session_state.approved_skus = []
            st.session_state.approved_skus.append(current_sku["SKU"])
            st.session_state.sku_index += 1
            st.success(f'SKU {current_sku["SKU"]} aprovado e enviado ao ERP SAP.')
            
        if col2.button('Não'):
            st.session_state.sku_index += 1
            st.write('Não aprovado.')

        if st.session_state.sku_index < df.shape[0]:
            st.button('Próximo')

    st.write('---')
    st.write('### Resultado da Aprovação')

    display_choice = st.selectbox('Visualizar por:', ['Selecione...', 'CATEGORY', 'SKU'])
    if display_choice == 'CATEGORY':
        approved_category_data = [{"CATEGORY": cat, "Qtd repo estoque": abs(df[df["CATEGORY"] == cat]["Qtd repo estoque"].sum())} for cat in st.session_state.approved_categories]
        st.table(approved_category_data)
    elif display_choice == 'SKU':
        if approval_method == 'por Categoria':
            # Get SKUs for approved categories
            approved_category_data = df[df["CATEGORY"].isin(st.session_state.approved_categories)]
            st.table(approved_category_data[["SKU", "Qtd repo estoque"]])
        else:
            approved_sku_data = [{"SKU": sku, "Qtd repo estoque": abs(df[df["SKU"] == sku]["Qtd repo estoque"].sum())} for sku in st.session_state.approved_skus]
            st.table(approved_sku_data)
