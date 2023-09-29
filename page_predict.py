import streamlit as st
import plotly.express as px
from dataframe import df
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def predict_page(df):

    # Cálculo dos BigNumbers
    total_forecast_15d = df['FORECAST 15D'].sum()
    total_forecast_30d = df['FORECAST 30D'].sum()
    total_forecast_60d = df['FORECAST 60D'].sum()

    col1, col2, col3 = st.columns(3)
    with col1:
        col1.metric('Previsão 15D', "{:,.0f}".format(total_forecast_15d))
        st.markdown("""
            <hr style='border:1px solid "#808080"; background-color: #808080; height:1px;'>
        """, unsafe_allow_html=True)
    with col2:
        col2.metric('Previsão 30D', "{:,.0f}".format(total_forecast_30d))
        st.markdown("""
            <hr style='border:1px solid "#808080"; background-color: #808080; height:1px;'>
        """, unsafe_allow_html=True)
    with col3:
        col3.metric('Previsão 60D', "{:,.0f}".format(total_forecast_60d))
        st.markdown("""
            <hr style='border:1px solid "#808080"; background-color: #808080; height:1px;'>
        """, unsafe_allow_html=True)
           
    # Dados fictícios
    dates = pd.date_range(start="2023-01-01", end="2023-06-30", freq='M')
    assertiveness = np.random.normal(0.85, 0.03, len(dates))

    # Criando o dataframe
    df2 = pd.DataFrame({
        'Date': dates,
        'Assertiveness': assertiveness
    })

    # Calculando a média
    mean_assertiveness = np.mean(assertiveness) * 100  # Convertendo para porcentagem

    # Configurando layout do Streamlit
    # st.markdown('<h1 style="font-size: 18px">Assertividade do Modelo</h1>', unsafe_allow_html=True)
    #st.title('Assertividade do Modelo')
    
    colu1, colu2 = st.columns([3,2])
    # with colu1:
    #     # Mostrando o "big number"
    #     st.markdown(f'<h2 style="color:green; float: left;">{mean_assertiveness:.1f}%</h2>', unsafe_allow_html=True)

    #     # Gráfico de linha
    #     fig = px.line(df2, x='Date', y='Assertiveness', labels={'Assertiveness': 'Assertividade (%)'}, title='Visão Mensal: Resultado Modelo (Jan-Jun)')
    #     fig.update_yaxes(tickformat=".2%")  # Formatação para mostrar em porcentagem
    #     fig.update_layout(width=800, height=400)  # Ajuste do tamanho do gráfico
        
    #     st.plotly_chart(fig)
    
    with colu1:
    # Filtros
        with st.expander("Filtros", expanded=False):
            # Converte para datetime e lista datas únicas
            df['DATE'] = pd.to_datetime(df['DATE'])
            date = df['DATE'].dt.strftime('%Y-%m-%d').unique().tolist()

            categories = df['CATEGORY'].unique().tolist()
            regioes = df['REGIAO'].unique().tolist()
            uf = df['UF'].unique().tolist()
            skus = df['SKU'].unique().tolist()

            # Primeira linha de filtros com 3 colunas
            col1, col2 = st.columns(2)
            with col1:
                selected_date = st.selectbox('Data:', ['Todas'] + date)
            with col2:
                selected_category = st.selectbox('Categoria:', ['Todas'] + categories)
            
            col3, col4 = st.columns(2)
            with col3:
                selected_regioes = st.selectbox('Região:', ['Todas'] + regioes)
            with col4:
                selected_uf = st.selectbox('UF:', ['Todas'] + uf)

            col5, = st.columns([1])
            with col5:
                selected_sku = st.selectbox('SKU:', ['Todos'] + skus)

        # Aplica os filtros ao dataframe
        if selected_date != 'Todas':
            df = df[df['DATE'] == selected_date]
        if selected_category != 'Todas':
            df = df[df['CATEGORY'] == selected_category]
        if selected_regioes != 'Todas':
            df = df[df['REGIAO'] == selected_regioes]
        if selected_uf != 'Todas':
            df = df[df['UF'] == selected_uf]
        if selected_sku != 'Todos':
            df = df[df['SKU'] == selected_sku]

    st.markdown("""
                <hr style='border:1px solid "#808080"; background-color: #808080; height:1px;'>
                """, unsafe_allow_html=True)

    # Mostrando o "big number"
    st.markdown("##### Modelo de Previsão (próx. 90 dias)")
    # Definindo dados fictícios para as métricas
    suggestions_data = {
        "Alta Criticidade": ("15.647", "-3%"),
        "Média Criticidade": ("8.756", "-2%"),
        "Baixa Criticidade": ("3.456", "-1%"),
    }

    # Criando colunas para os big numbers
    cols = st.columns(3)

    # Iterando pelos dados e criando os big numbers com subindicadores
    for index, (metric_name, values) in enumerate(suggestions_data.items()):
        principal_value, variation = values
        cols[index].metric(metric_name, principal_value, variation)

    st.markdown("<small>*Obs: o nível de criticidade dos produtos foi determinado através do valor agregado e a quantidade de estoque.</small>", unsafe_allow_html=True)
    # Agrupar por data e criticidade
    grouped = df.groupby(['DATE', 'CRITICIDADE']).sum()['SALE'].reset_index()

    # Lista para armazenar as previsões
    all_forecasts = []

    # Loop por cada nível de criticidade para fazer previsões separadas
    for crit in grouped['CRITICIDADE'].unique():
        monthly_sales = grouped[grouped['CRITICIDADE'] == crit]

        X = np.array(range(len(monthly_sales))).reshape(-1, 1)
        y = monthly_sales['SALE']

        model = LinearRegression()
        model.fit(X, y)

        # Previsão para os próximos 3 meses
        for i in range(3):
            next_month = np.array([[len(monthly_sales) + i]])
            rupture_forecast = model.predict(next_month)[0]

            new_date = (monthly_sales['DATE'].iloc[-1] + pd.DateOffset(months=i+1))
            all_forecasts.append({'DATE': new_date, 'SALE': rupture_forecast, 'CRITICIDADE': crit})

    # Convertendo lista de previsões em DataFrame e combinando com dados originais
    forecast_df = pd.DataFrame(all_forecasts)
    combined_df = pd.concat([grouped, forecast_df])

    # Adicionar uma coluna de tipo (Real ou Projetado)
    combined_df['Type'] = ['Real' if i < len(grouped) else 'Projetado' for i in range(len(combined_df))]
    color_map_pastel = {
        "Baixa": "#A8E6CF",  # Verde pastel
        "Média": "#FFD3B6",  # Amarelo pastel
        "Alta": "#FFAAA5"    # Vermelho pastel
}
    st.write('---') #1
    
    # Gráfico geral de previsão de demanda por mês
    combined_df=combined_df.sort_values(by=['CRITICIDADE'])
    fig = px.bar(combined_df, x='DATE', y='SALE', color='CRITICIDADE', title=f'Previsão de Demanda', 
                labels={'SALE': 'Vendas'}, 
                category_orders={"DATE": sorted(combined_df['DATE'].unique())},
                color_discrete_map=color_map_pastel)

    fig.update_layout(barmode='stack')
    st.plotly_chart(fig, use_container_width=True)

    # Agrupar por data e criticidade
    grouped = df.groupby(['DATE', 'CRITICIDADE']).sum()['Ruptura'].reset_index()

    # Lista para armazenar as previsões
    all_forecasts = []

    # Loop por cada nível de criticidade para fazer previsões separadas
    for crit in grouped['CRITICIDADE'].unique():
        monthly_sales = grouped[grouped['CRITICIDADE'] == crit]

        X = np.array(range(len(monthly_sales))).reshape(-1, 1)
        y = monthly_sales['Ruptura']

        model = LinearRegression()
        model.fit(X, y)

        # Previsão para os próximos 3 meses
        for i in range(3):
            next_month = np.array([[len(monthly_sales) + i]])
            rupture_forecast = model.predict(next_month)[0]

            new_date = (monthly_sales['DATE'].iloc[-1] + pd.DateOffset(months=i+1))
            all_forecasts.append({'DATE': new_date, 'Ruptura': rupture_forecast, 'CRITICIDADE': crit})

    # Convertendo lista de previsões em DataFrame e combinando com dados originais
    forecast_df = pd.DataFrame(all_forecasts)
    combined_df = pd.concat([grouped, forecast_df])

    # Adicionar uma coluna de tipo (Real ou Projetado)
    combined_df['Type'] = ['Real' if i < len(grouped) else 'Projetado' for i in range(len(combined_df))]
    color_map_pastel = {
        "Baixa": "#A8E6CF",  # Verde pastel
        "Média": "#FFD3B6",  # Amarelo pastel
        "Alta": "#FFAAA5"    # Vermelho pastel
}
    st.write('---')

    # Gráfico geral de previsão de demanda por mês
    combined_df=combined_df.sort_values(by=['CRITICIDADE'])
    fig = px.bar(combined_df, x='DATE', y='Ruptura', color='CRITICIDADE', title=f'Previsão de Ruptura', 
                labels={'Ruptura': 'Ruptura'}, 
                category_orders={"DATE": sorted(combined_df['DATE'].unique())},
                color_discrete_map=color_map_pastel)

    fig.update_layout(barmode='stack')
    st.plotly_chart(fig, use_container_width=True)

    #Novo gráfico
    grouped = df.groupby(['DATE', 'CATEGORY', 'CRITICIDADE']).mean()['Ruptura'].reset_index()

    # Lista para armazenar as previsões
    all_forecasts = []

    # Loop por cada nível de criticidade e categoria para fazer previsões separadas
    for crit in grouped['CRITICIDADE'].unique():
        for cat in grouped['CATEGORY'].unique():
            monthly_sales = grouped[(grouped['CRITICIDADE'] == crit) & (grouped['CATEGORY'] == cat)]

            X = np.array(range(len(monthly_sales))).reshape(-1, 1)
            y = monthly_sales['Ruptura']

            model = LinearRegression()
            model.fit(X, y)

            # Previsão para os próximos 3 meses
            for i in range(3):
                next_month = np.array([[len(monthly_sales) + i]])
                rupture_forecast = model.predict(next_month)[0]

                new_date = (monthly_sales['DATE'].iloc[-1] + pd.DateOffset(months=i+1))
                all_forecasts.append({'DATE': new_date, 'Ruptura': rupture_forecast, 'CRITICIDADE': crit, 'CATEGORY': cat})

    # Convertendo lista de previsões em DataFrame e combinando com dados originais
    forecast_df = pd.DataFrame(all_forecasts)
    combined_df = pd.concat([grouped, forecast_df])

    # Filtrando somente dados projetados e somando por categoria
    projected_df = combined_df[combined_df['DATE'] >= new_date].groupby(['CATEGORY', 'CRITICIDADE']).sum().reset_index()

    color_map_pastel = {
        "Baixa": "#A8E6CF",  # Verde pastel
        "Média": "#FFD3B6",  # Amarelo pastel
        "Alta": "#FFAAA5"    # Vermelho pastel
    }

    st.write('---')
    
    # Gráfico de ruptura projetada por categoria e criticidade
    fig = px.bar(projected_df, x='CATEGORY', y='Ruptura', color='CRITICIDADE', title=f'Previsão de Ruptura por Categoria - 90 dias', 
                labels={'Ruptura': 'Ruptura'}, 
                color_discrete_map=color_map_pastel)

    fig.update_layout(barmode='stack')
    st.plotly_chart(fig, use_container_width=True)

    st.write("""
    *Análise ChatGPT:* A demanda por itens de alta criticidade tende aumentar, principalmente de produtos como celulares, contudo, como temos grandes compras previstas para estes e outros itens os números de ruptura irão cair. De qualquer forma, é importante garantir que as mercadorias sejam entregues, conforme previsão para que não tenhamos casos de ruptura com produtos de alta criticidade.
    """)
    
    st.write('#### Pergunte sobre os dados ao ChatGPT')
    prompt = st.text_input("Digite abaixo")  
    if prompt:
        st.write(f"Resposta: {prompt}")
