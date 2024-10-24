import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout= 'wide')

st.title('DASHBOARD DE INDICADORES')

def formata_numero(valor, prefixo=''):
    for unidade in ['', 'mil']:
        if valor < 1000:
            return f'{prefixo} {valor:.2f} {unidade}'
        valor /= 1000
    return f'{prefixo} {valor:.2f} milhões'

# Carregar os dados
dados = pd.read_csv('dados/case_cientistaiii.csv')
dados['dt_referencia'] = pd.to_datetime(dados['dt_referencia'])

# Agrupar os dados por cluster e somar o valor
valor_cluster = dados.groupby('cluster')['valor'].sum()

# Dividir a página em colunas
coluna1, coluna2 = st.columns(2)

# Gráfico de linhas

fig_valor_data = px.line(dados, 
                        x="dt_referencia", 
                        y="valor", 
                        title='Valor ao longo do tempo',
                        color='des_indicador',
                        range_y=(0, dados['valor'].max()),
                        line_dash='des_indicador'
                        )

# Gráfico de barras com base no cluster, já ordenado pelos valores
fig_valor_cluster = px.bar(valor_cluster.sort_values(ascending=False).reset_index(), 
                    text_auto=True,
                    labels={'index': 'Cluster', 'value': 'Valor'})
fig_valor_cluster.update_layout(showlegend=False)

# Exibir as métricas e o gráfico
with coluna1:
    st.metric('Valor total: ', formata_numero(dados['valor'].sum(), 'R$'))
    st.plotly_chart(fig_valor_data, use_container_width=True)
    
with coluna2:
    st.plotly_chart(fig_valor_cluster, use_container_width=True)
