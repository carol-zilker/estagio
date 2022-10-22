### Importando bibliotecas

import streamlit as st
import pandas as pd
from PIL import Image
from funcoes import *
from datetime import datetime
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Tráfego Aéreo Brasileiro", layout="wide")
#st.markdown("""<style>body{background-color: #034C9F;}</style>""",unsafe_allow_html=True)

#def local_css(file_name):
#    with open(file_name) as f:
#        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

#local_css("style.css")

### Configurando a página



amarelo_ita = '#FFD405'
azul_ita = '#034C9F'
vermelho_ita = '#E11A22'
fonte = 'Sans Sarif'

#local_css("style.css")

### Cabeçalho

cab1, cab2 = st.columns([1,3])

cab1.image('ita.png', width = 300)
titulo="""
<h1 style="font-size:220%; color: #034C9F; font-family: Verdana"> Tráfego Aéreo Brasileiro<br>
</h1>
"""
cab2.markdown(titulo, unsafe_allow_html=True)
subtitulo="""
<h1 style="font-size:90%; color: #000000; font-family:Verdana"> Desenvolvido por Alexandre Fernandes | Estudante de Engenharia Civil-Aeronaútica | Instituto Tecnológico de Aeronáutica<br>
</h1>
"""
cab2.markdown(subtitulo, unsafe_allow_html=True)


### Objetivos do relatório

objetivos="""
<h1 style="font-size:180%; color: #034C9F; font-family:Verdana"> Objetivos<br>
 <hr style= "  display: block;
  margin-top: 0.5em;
  margin-bottom: 0.5em;
  margin-left: auto;
  margin-right: auto;
  border-style: inset;
  border-width: 1.5px;"></h1>
"""
st.markdown(objetivos, unsafe_allow_html=True)

objetivo1 ="""
<h2 style="font-size:100%; color: #000000; font-family:Verdana"> ☞ Analisar a demanda operacional<br>
</h2>
"""

objetivo2 ="""
<h2 style="font-size:100%; color: #000000; font-family:Verdana"> ☞ Estudar a performance<br>
</h2>
"""

st.markdown(objetivo1, unsafe_allow_html=True)
st.markdown(objetivo2, unsafe_allow_html=True)

### Filtros

filtro1, filtro2,filtro3, filtro4 = st.columns((1,1,0.5,0.5))

## Leitura base de dados

microdados = pd.read_csv('base_estagio-2.csv', sep=',')

aeroportos = inserir_linha(pd.DataFrame(data = microdados['Descrição Aeroporto Origem'].unique()),pd.DataFrame({0: 'Selecione o aeroporto'}, index=[-1]))
aeroporto_select = filtro1.selectbox('Aeroporto', aeroportos[0], help = 'Selecione um aeroporto para filtrá-lo')

companhias = inserir_linha(pd.DataFrame(data = microdados['Empresa Aérea'].unique()),pd.DataFrame({0: 'Selecione a companhia aérea'}, index=[-1]))
companhia_select = filtro2.selectbox('Companhia Aérea', companhias[0], help = 'Selecione uma companhia aérea para filtrá-la')

microdados.dt_referencia = pd.to_datetime(microdados.dt_referencia)

start_date_dataframe = microdados.dt_referencia[0]
end_date_dataframe = microdados.dt_referencia[microdados.shape[0] - 1]

start_date = filtro3.date_input('Data inicial', start_date_dataframe, min_value=start_date_dataframe,
                                       max_value=end_date_dataframe)
end_date = filtro4.date_input('Data final', end_date_dataframe, min_value=start_date_dataframe,
                                     max_value=end_date_dataframe)
    
start_date2 = start_date.strftime("%Y-%m-%d")
end_date2 = end_date.strftime("%Y-%m-%d")
    
microdados = microdados.set_index(['dt_referencia'])
    
microdados2 = microdados.loc[start_date2:end_date2]

if (companhia_select != 'Selecione a companhia aérea'):
    microdados3 = microdados2[microdados2['Empresa Aérea'] == companhia_select]
else:
    microdados3 = microdados2

if (aeroporto_select != 'Selecione o aeroporto'):
    microdados4 = microdados3[microdados3['Descrição Aeroporto Origem'] == aeroporto_select]
else:
    microdados4 = microdados3

analise_demanda="""
<h1 style="font-size:180%; color: #034C9F; font-family:Verdana"> Análise da demanda operacional<br>
 <hr style= "  display: block;
  margin-top: 0.5em;
  margin-bottom: 0.5em;
  margin-left: auto;
  margin-right: auto;
  border-style: inset;
  border-width: 1.5px;"></h1>
"""
st.markdown(analise_demanda, unsafe_allow_html=True)

### Resultados chave

resultado1, resultado2, resultado3, resultado4, resultado5 = st.columns((1,1,1,1,1))

if (aeroporto_select == 'Selecione o aeroporto'):

    resultado1.metric(label ='Número de voos', value = int(len(microdados4)))
    resultado2.metric(label ='Número de rotas', value = len(microdados4['sg_icao_destino'].unique()))
    resultado3.metric(label ='Número de passageiros', value = sum(microdados4['nr_passag_pagos']) + sum(microdados4['nr_passag_gratis']))
    resultado4.metric(label ='Média de voos por dia', value = round(int(len(microdados4))/(end_date - start_date).days))
    resultado5.metric(label ='Média de passageiros por dia', value = round((sum(microdados4['nr_passag_pagos']) + sum(microdados4['nr_passag_gratis']))/(end_date - start_date).days))
else:
    metrica1 = microdados3.groupby('nm_aerodromo_origem').count()
    metrica1_1 = metrica1['nm_aerodromo_destino'].mean()
    resultado1.metric(label ='Número de voos', value = int(len(microdados4)), delta = str(round(len(microdados4) - metrica1_1))+' em relação à média')
    metrica2 = microdados3.groupby('nm_aerodromo_origem').nunique('nm_aerodromo_destino')
    metrica2_1 = metrica2['nm_aerodromo_destino'].mean()
    resultado2.metric(label ='Número de rotas', value = len(microdados4['sg_icao_destino'].unique()), delta = str(round(len(microdados4['sg_icao_destino'].unique()) - metrica2_1))+' em relação à média')
    metrica3 = microdados3.groupby('nm_aerodromo_origem').sum()
    metrica3_1 = (metrica3['nr_passag_pagos']+metrica3['nr_passag_gratis']).mean()
    resultado3.metric(label ='Número de passageiros', value = sum(microdados4['nr_passag_pagos']) + sum(microdados4['nr_passag_gratis']), delta = str(round(sum(microdados4['nr_passag_pagos']) + sum(microdados4['nr_passag_gratis']) - metrica3_1))+' em relação à média')
    resultado4.metric(label ='Média de voos por dia', value = round(int(len(microdados4))/(end_date - start_date).days), delta = str(round((len(microdados4) - metrica1_1)/(end_date - start_date).days))+' em relação à média')
    resultado5.metric(label ='Média de passageiros por dia', value = round((sum(microdados4['nr_passag_pagos']) + sum(microdados4['nr_passag_gratis']))/(end_date - start_date).days), delta = str(round((sum(microdados4['nr_passag_pagos']) + sum(microdados4['nr_passag_gratis']) - metrica3_1)/(end_date - start_date).days))+' em relação à média')


### Gráficos - parte 1

grafico1, grafico2 = st.columns(2)

## Aeroporto selecionado

microdados5 = microdados4.groupby(['dt_referencia']).agg({'nm_aerodromo_origem':'count','nr_passag_pagos':'sum','nr_passag_gratis':'sum'}).reset_index()
microdados5['nr_passag_total'] = microdados5['nr_passag_pagos'] + microdados5['nr_passag_gratis']
microdados5['mes_ano'] = microdados5['dt_referencia'].astype(str).str[:7]

microdados6 = microdados5.groupby('mes_ano').sum().reset_index()

# Média

microdados7 = microdados3.groupby(['dt_referencia','nm_aerodromo_origem']).agg({'nm_aerodromo_destino':'count','nr_passag_pagos':'sum','nr_passag_gratis':'sum'}).reset_index()
microdados7['nr_passag_total'] = microdados7['nr_passag_pagos'] + microdados7['nr_passag_gratis']
microdados7['mes_ano'] = microdados7['dt_referencia'].astype(str).str[:7]

microdados8 = microdados7.groupby(['mes_ano','nm_aerodromo_origem']).sum().reset_index()
microdados9 = microdados8.groupby('mes_ano').mean().reset_index()

microdados10 = pd.merge(microdados6, microdados9, on = 'mes_ano', how = 'left')

fig1 = px.bar(microdados10, x = 'mes_ano', y='nm_aerodromo_origem', text_auto='.3s', width=630, color_discrete_sequence = [azul_ita])
fig1.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
fig1.add_scatter(x= microdados10['mes_ano'], y= microdados10['nm_aerodromo_destino'], mode='lines', line=dict(color=vermelho_ita), name='Média')
fig1.update_layout(title_text="Número de voos por mês",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Número de voos', xaxis_title='Mês', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="center",x=0.9))
grafico1.plotly_chart(fig1)

fig2 = px.bar(microdados10, x = 'mes_ano', y='nr_passag_total_x', text_auto='.2s', width=630, color_discrete_sequence = [azul_ita])
fig2.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
fig2.add_scatter(x = microdados10['mes_ano'], y=microdados10['nr_passag_total_y'], mode='lines', line=dict(color=vermelho_ita), name='Média')
fig2.update_layout(title_text="Número de passageiros por mês",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Número de passageiros', xaxis_title='Mês', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="center",x=0.9))
grafico2.plotly_chart(fig2)

### Gráficos - parte 2

grafico3, grafico4 = st.columns(2)

microdados11 = microdados4.groupby(['sg_icao_destino']).count().reset_index()

microdados12 = pd.DataFrame()
microdados12['sg_icao_destino'] = microdados11['sg_icao_destino']
microdados12['nr_voos'] = microdados11['Unnamed: 0']
microdados13 = microdados12.sort_values(by = 'nr_voos', ascending = False).reset_index(drop = False).reset_index(drop = False)
microdados14 = microdados13[microdados13['level_0'] < 10]
microdados15 = microdados14.sort_values(by = 'nr_voos', ascending = True)

fig3 = px.bar(microdados15, x = 'nr_voos', y='sg_icao_destino', text_auto='.3s', width=630, color_discrete_sequence = [azul_ita], orientation = 'h')
fig3.update_layout(title_text="Top 10 aeroportos de destino",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Aeroporto de destino', xaxis_title='Número de voos')
grafico3.plotly_chart(fig3)

microdados16 = microdados4.groupby(['sg_empresa_icao']).count().reset_index()

microdados17 = pd.DataFrame()
microdados17['sg_empresa_icao'] = microdados16['sg_empresa_icao']
microdados17['nr_voos'] = microdados16['Unnamed: 0']
microdados18 = microdados17.sort_values(by = 'nr_voos', ascending = False).reset_index(drop = False).reset_index(drop = False)
microdados19 = microdados18[microdados18['level_0'] < 10]
microdados20 = microdados19.sort_values(by = 'nr_voos', ascending = True)

fig4 = px.bar(microdados20, x = 'nr_voos', y='sg_empresa_icao', text_auto='.2s', width=630, color_discrete_sequence = [azul_ita], orientation = 'h')
fig4.update_layout(title_text="Top 10 companhias aéreas",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Companhia Aérea', xaxis_title='Número de voos')
grafico4.plotly_chart(fig4)

### Gráficos - parte 3

grafico5, grafico6 = st.columns(2)

microdados22 = microdados4.groupby('nm_pais_destino').count().reset_index()
microdados23 = microdados22[microdados22['nm_pais_destino'] != 'BRASIL']
microdados24 = microdados23.sort_values(by = 'nm_aerodromo_destino', ascending = False).reset_index(drop = False).reset_index(drop = False)
microdados25 = microdados24[microdados24['level_0'] < 10]
microdados26 = microdados25.sort_values(by = 'nm_aerodromo_destino', ascending = True)
fig5 = px.bar(microdados26, x = 'nm_aerodromo_destino', y='nm_pais_destino', text_auto='.2s', width=630, color_discrete_sequence = [azul_ita], orientation = 'h')
fig5.update_layout(title_text="Top 10 destinos internacionais",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='País', xaxis_title='Número de voos')
grafico5.plotly_chart(fig5)

microdados27 = microdados4[microdados4['nm_pais_destino'] == 'BRASIL']
microdados28 = microdados27.groupby('sg_uf_destino').count().reset_index()
microdados29 = microdados28.sort_values(by = 'nm_aerodromo_destino', ascending = False).reset_index(drop = False).reset_index(drop = False)
microdados30 = microdados29[microdados29['level_0'] < 10]
microdados31 = microdados30.sort_values(by = 'nm_aerodromo_destino', ascending = True)
fig6 = px.bar(microdados31, x = 'nm_aerodromo_destino', y='sg_uf_destino', text_auto='.2s', width=630, color_discrete_sequence = [azul_ita], orientation = 'h')
fig6.update_layout(title_text="Top 10 destinos nacionais",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Estado', xaxis_title='Número de voos')
grafico6.plotly_chart(fig6)

analise_performance="""
<h1 style="font-size:180%; color: #034C9F; font-family:Verdana"> Estudo da performance<br>
 <hr style= "  display: block;
  margin-top: 0.5em;
  margin-bottom: 0.5em;
  margin-left: auto;
  margin-right: auto;
  border-style: inset;
  border-width: 1.5px;"></h1>
"""
st.markdown(analise_performance, unsafe_allow_html=True)

### TATIC

resultado6, resultado7, resultado8, resultado9, resultado10, resultado11 = st.columns((1,1,1,1,1,1))

grafico7, grafico8 = st.columns(2)

#tatic = pd.read_csv('tatic_tratado.csv', sep = ',')
tatic = pd.read_csv('base_estagio-2.csv', sep=',')


sigla_aeroporto_select = ' '
sigla_companhia_select = ' '

if aeroporto_select != 'Selecione o aeroporto':
    sigla_aeroporto_select = microdados4['sg_icao_origem'][0]

if companhia_select != 'Selecione a companhia aérea':
    sigla_companhia_select = microdados4['sg_empresa_icao'][0]

if sigla_aeroporto_select != ' ':
    tatic1_aux1 = tatic[tatic['Sigla ICAO Aeroporto Origem'] == sigla_aeroporto_select]
else:
    tatic1_aux1 = tatic

if sigla_companhia_select != ' ':
    tatic1_aux2 = tatic1_aux1[tatic1_aux1['Sigla ICAO Empresa Aérea'].str[:3] == sigla_companhia_select]
else:
    tatic1_aux2 = tatic1_aux1

tatic2 = tatic1_aux2
tatic2['Pontualidade Partida'] = ['Não pontual' if s > 15 else 'Pontual' for s in tatic2['Partida Real - Partida Prevista']]
tatic2['mes_ano'] = tatic2['data'].astype(str).str[0:7]
tatic3 = tatic2[tatic2['data'] != '//NaT']
tatic3['data'] = tatic3['data'].astype('datetime64[ns]')
start_date4 = pd.to_datetime(start_date)
tatic4 = tatic3[tatic3['data'] > start_date4]
end_date4 = pd.to_datetime(end_date)
tatic4_aux = tatic4[tatic4['data'] < end_date4]
tatic5 = tatic4_aux.groupby(['Pontualidade Partida','mes_ano']).count().reset_index()
tatic6 = tatic5.groupby(['mes_ano']).sum().reset_index()
tatic7 = pd.merge(tatic5,tatic6, on = 'mes_ano', how = 'left')

tatic7['Pontualidade'] = tatic7['País de origem_x']/tatic7['País de origem_y']
tatic8 = tatic7.sort_values(by = 'Pontualidade Partida', ascending = False)
fig7 = px.bar(tatic8, x = 'mes_ano', y='Pontualidade', width=630, color="Pontualidade Partida", text=[f'{int(i)}%' for i in round(100*tatic8['Pontualidade'],0)],
    color_discrete_map={
        'Pontual': 'green',
        'Não pontual': vermelho_ita})
fig7.update_layout(barmode='stack',title_text="Pontualidade de partida dos voos",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Porcentagem de voos', xaxis_title='Mês')
fig7.layout.yaxis.tickformat = ',.0%'


# Gráfico 8

tatic9 = tatic1_aux2
tatic9['Pontualidade Chegada'] = ['Não pontual' if s > 15 else 'Pontual' for s in tatic9['Chegada Real - Chegada Prevista']]
tatic9['mes_ano'] = tatic9['dt_chegada_real'].astype(str).str[0:7]
tatic10 = tatic9
tatic10['dt_chegada_real'] = tatic10['dt_chegada_real'].astype('datetime64[ns]')
tatic11 = tatic10[tatic10['dt_chegada_real'] > start_date4]
tatic11_aux = tatic11[tatic11['dt_chegada_real'] < end_date4]
tatic12 = tatic11_aux.groupby(['Pontualidade Chegada','mes_ano']).count().reset_index()
tatic13 = tatic12.groupby(['mes_ano']).sum().reset_index()
tatic14 = pd.merge(tatic12,tatic13, on = 'mes_ano', how = 'left')
tatic14['Pontualidade'] = tatic14['País de origem_x']/tatic14['País de origem_y']
if len(tatic14.index) == 0:
    tatic14.rename(columns = {'Pontualidade Chegada_x': 'Pontualidade Chegada'}, inplace = True)
tatic15 = tatic14.sort_values(by = 'Pontualidade Chegada', ascending = False)
fig8 = px.bar(tatic15, x = 'mes_ano', y='Pontualidade', width=630, color="Pontualidade Chegada", text=[f'{int(i)}%' for i in round(100*tatic15['Pontualidade'],0)],
    color_discrete_map={
        'Pontual': 'green',
        'Não pontual': vermelho_ita})
fig8.update_layout(barmode='stack',title_text="Pontualidade de chegada dos voos",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Porcentagem de voos', xaxis_title='Mês')
fig8.layout.yaxis.tickformat = ',.0%'


########

grafico9, grafico10 = st.columns(2)

tatic16 = tatic4_aux.groupby(['Pontualidade Partida','Modelo Equipamento']).count().reset_index()
tatic17 = tatic16.groupby(['Modelo Equipamento']).sum().reset_index()
tatic18 = pd.merge(tatic16,tatic17, on = 'Modelo Equipamento', how = 'left')
tatic18['Pontualidade'] = tatic18['País de origem_x']/tatic18['País de origem_y']
tatic19 = tatic18.sort_values(by = 'Pontualidade Partida', ascending = False)
fig9 = px.bar(tatic19, x = 'Modelo Equipamento', y='Pontualidade', width=630, color="Pontualidade Partida", text=[f'{int(i)}%' for i in round(100*tatic19['Pontualidade'],0)],
    color_discrete_map={
        'Pontual': 'green',
        'Não pontual': vermelho_ita})
fig9.update_layout(barmode='stack',title_text="Pontualidade de partida dos voos",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Porcentagem de voos', xaxis_title='Aeronave')
fig9.layout.yaxis.tickformat = ',.0%'


tatic20 = tatic11_aux.groupby(['Pontualidade Chegada','Modelo Equipamento']).count().reset_index()
tatic21 = tatic20.groupby(['Modelo Equipamento']).sum().reset_index()
tatic22 = pd.merge(tatic20,tatic21, on = 'Modelo Equipamento', how = 'left')
tatic22['Pontualidade'] = tatic22['País de origem_x']/tatic22['País de origem_y']
if len(tatic22.index) == 0:
    tatic22.rename(columns = {'Pontualidade Chegada_x': 'Pontualidade Chegada'}, inplace = True)
tatic23 = tatic22.sort_values(by = 'Pontualidade Chegada', ascending = False)
fig10 = px.bar(tatic23, x = 'Modelo Equipamento', y='Pontualidade', width=630, color="Pontualidade Chegada", text=[f'{int(i)}%' for i in round(100*tatic23['Pontualidade'],0)],
    color_discrete_map={
        'Pontual': 'green',
        'Não pontual': vermelho_ita})
fig10.update_layout(barmode='stack',title_text="Pontualidade de chegada dos voos",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Porcentagem de voos', xaxis_title='Aeronave')
fig10.layout.yaxis.tickformat = ',.0%'


### METAR

grafico11, grafico12 = st.columns(2)
grafico13, grafico14 = st.columns(2)

metar = pd.read_csv('base_estagio-2.csv', sep=',')

if aeroporto_select != 'Selecione o aeroporto':
    sigla_aeroporto_select = microdados4['sg_icao_origem'][0]

if sigla_aeroporto_select != ' ':
    metar2 = metar[metar['aeroporto'] == sigla_aeroporto_select]
else:
    metar2 = metar

metar2['mes_ano'] = metar2['data'].astype(str).str[0:7]
metar2['data'] = metar2['data'].astype('datetime64[ns]')

metar3 = metar2[metar2['data'] > start_date4]
metar4 = metar3[metar3['data'] < end_date4]
metar4_aux = metar4[metar4['temperatura do ar (Nr)'] != ' ']
metar4_aux['temperatura do ar (Nr)'] = metar4_aux['temperatura do ar (Nr)'].astype(int)
metar4_aux['temperatura de orvalho (Nr)'] = metar4_aux['temperatura de orvalho (Nr)'].astype(int)
metar4_aux2 = metar4_aux[metar4_aux['vento (Nr)'] != ' ']
metar4_aux2['vento (Nr)'] = metar4_aux2['vento (Nr)'].astype(int)
metar4_aux2['pressão (Nr)'] = metar4_aux2['pressão (Nr)'].astype(int)
metar5 = metar4_aux2.groupby('hora').mean().reset_index()

tatic24 = tatic4_aux.groupby(['Hora do dia','Pontualidade Partida']).count().reset_index()
tatic25 = tatic4_aux.groupby(['Hora do dia']).count().reset_index()
tatic26 = pd.merge(tatic24,tatic25, on = 'Hora do dia', how = 'left')
tatic26['Pontualidade'] = tatic26['País de origem_x']/tatic26['País de origem_y']
tatic27 = tatic26[tatic26['Pontualidade Partida_x'] != 'Não pontual']
tatic28 = pd.DataFrame()
tatic28['hora'] = tatic27['Hora do dia']
tatic28['Pontualidade'] = tatic27['Pontualidade']

metar6 = pd.merge(metar5, tatic28, on = 'hora', how = 'left')

fig11 = make_subplots(specs=[[{"secondary_y": True}]])
fig11.add_trace(go.Scatter(x=metar6['hora'], y=metar6['Pontualidade'], name="Pontualidade", mode="lines", marker_color = vermelho_ita),secondary_y=True)
fig11.add_trace(go.Bar(x=metar6['hora'], y=metar6['temperatura do ar (Nr)'], name="Temperatura do ar", marker_color = azul_ita, text=round(metar6['temperatura do ar (Nr)'])),secondary_y=False)
fig11.update_layout(title_text="Temperatura do ar média ao longo do dia",title_x=0,margin= dict(l=0,r=10,b=10,t=30),legend=dict(orientation="h",yanchor="bottom",y=0.1,xanchor="center",x=0.6), width=630)
fig11.update_xaxes(title_text="Temperatura do ar")
fig11.update_yaxes(title_text="Temperatura do ar", secondary_y=False)
fig11.update_yaxes(title_text="Pontualidade de Partida", secondary_y=True, range=[0, 1])
fig11.layout.yaxis2.tickformat = ',.0%'


fig12 = make_subplots(specs=[[{"secondary_y": True}]])
fig12.add_trace(go.Scatter(x=metar6['hora'], y=metar6['Pontualidade'], name="Pontualidade", mode="lines", marker_color = vermelho_ita),secondary_y=True)
fig12.add_trace(go.Bar(x=metar6['hora'], y=metar6['temperatura de orvalho (Nr)'], name="Temperatura de orvalho", marker_color = azul_ita, text=round(metar6['temperatura de orvalho (Nr)'])),secondary_y=False)
fig12.update_layout(title_text="Temperatura de orvalho média ao longo do dia",title_x=0,margin= dict(l=0,r=10,b=10,t=30),legend=dict(orientation="h",yanchor="bottom",y=0.1,xanchor="center",x=0.6), width=630)
fig12.update_xaxes(title_text="Temperatura de orvalho")
fig12.update_yaxes(title_text="Temperatura de orvalho", secondary_y=False)
fig12.update_yaxes(title_text="Pontualidade de Partida", secondary_y=True, range=[0, 1])
fig12.layout.yaxis2.tickformat = ',.0%'


fig13 = make_subplots(specs=[[{"secondary_y": True}]])
fig13.add_trace(go.Scatter(x=metar6['hora'], y=metar6['Pontualidade'], name="Pontualidade", mode="lines", marker_color = vermelho_ita),secondary_y=True)
fig13.add_trace(go.Bar(x=metar6['hora'], y=metar6['vento (Nr)'], name="Vento", marker_color = azul_ita, text=round(metar6['vento (Nr)'])),secondary_y=False)
fig13.update_layout(title_text="Vento médio ao longo do dia",title_x=0,margin= dict(l=0,r=10,b=10,t=30),legend=dict(orientation="h",yanchor="bottom",y=0.1,xanchor="center",x=0.6), width=630)
fig13.update_xaxes(title_text="Vento")
fig13.update_yaxes(title_text="Vento", secondary_y=False)
fig13.update_yaxes(title_text="Pontualidade de Partida", secondary_y=True, range=[0, 1])
fig13.layout.yaxis2.tickformat = ',.0%'


fig14 = make_subplots(specs=[[{"secondary_y": True}]])
fig14.add_trace(go.Scatter(x=metar6['hora'], y=metar6['Pontualidade'], name="Pontualidade", mode="lines", marker_color = vermelho_ita),secondary_y=True)
fig14.add_trace(go.Bar(x=metar6['hora'], y=metar6['pressão (Nr)'], name="Pressão", marker_color = azul_ita, text=round(metar6['pressão (Nr)'])),secondary_y=False)
fig14.update_layout(title_text="Pressão ao longo do dia",title_x=0,margin= dict(l=0,r=10,b=10,t=30),legend=dict(orientation="h",yanchor="bottom",y=0.1,xanchor="center",x=0.6), width=630)
fig14.update_xaxes(title_text="Pressão")
fig14.update_yaxes(title_text="Pressão", secondary_y=False, range=[960, 1040])
fig14.update_yaxes(title_text="Pontualidade de Partida", secondary_y=True, range=[0, 1])
fig14.layout.yaxis2.tickformat = ',.0%'


tatic2_aux = tatic
tatic2_aux['Pontualidade Partida'] = ['Não pontual' if s > 15 else 'Pontual' for s in tatic2_aux['Partida Real - Partida Prevista']]
tatic3_aux = tatic2_aux[tatic2_aux['dt_partida_real'] != '//NaT']
tatic3_aux['dt_partida_real'] = tatic3_aux['dt_partida_real'].astype('datetime64[ns]')
tatic4_aux1 = tatic3_aux[tatic3_aux['dt_partida_real'] > start_date4]
tatic4_aux2 = tatic4_aux1[tatic4_aux1['dt_partida_real'] < end_date4]
tatic29 = tatic4_aux2.groupby('Pontualidade Partida').count().reset_index()
tatic30 = tatic29[tatic29['Pontualidade Partida'] == 'Pontual'].reset_index()
tatic31 = tatic29[tatic29['Pontualidade Partida'] == 'Não pontual'].reset_index()


tatic9_aux = tatic
tatic9_aux['Pontualidade Chegada'] = ['Não pontual' if s > 15 else 'Pontual' for s in tatic9_aux['Chegada Real - Chegada Prevista']]
tatic10_aux = tatic9_aux[tatic9_aux['dt_chegada_real'] != '//NaT']
tatic10_aux['dt_chegada_real'] = tatic10_aux['dt_chegada_real'].astype('datetime64[ns]')
tatic11_aux1 = tatic10_aux[tatic10_aux['dt_chegada_real'] > start_date4]
tatic11_aux2 = tatic11_aux1[tatic11_aux1['dt_chegada_real'] < end_date4]
tatic32 = tatic11_aux2.groupby('Pontualidade Chegada').count().reset_index()
tatic33 = tatic32[tatic32['Pontualidade Chegada'] == 'Pontual'].reset_index()
tatic34 = tatic32[tatic32['Pontualidade Chegada'] == 'Não pontual'].reset_index()

if aeroporto_select != 'Selecione o aeroporto':
    sigla_aeroporto_select = microdados4['sg_icao_origem'][0]

if companhia_select != 'Selecione a companhia aérea':
    sigla_companhia_select = microdados4['sg_empresa_icao'][0]

## Filtrando aeroporto
if sigla_companhia_select != ' ':
    tatic35 = tatic4_aux[tatic4_aux['indicativo'].str[:3] == sigla_companhia_select]
    tatic36 = tatic11_aux[tatic11_aux['indicativo'].str[:3] == sigla_companhia_select]
else:
    tatic35 = tatic4_aux
    tatic36 = tatic11_aux

if sigla_aeroporto_select != ' ':
    tatic37 = tatic35[tatic35['adep'] == sigla_aeroporto_select]
    tatic38 = tatic36[tatic36['adep'] == sigla_aeroporto_select]
else:
    tatic37 = tatic35
    tatic38 = tatic36

tatic39 = tatic37.groupby('Pontualidade Partida').count().reset_index()
tatic40 = tatic39[tatic39['Pontualidade Partida'] == 'Pontual'].reset_index()
tatic41 = tatic39[tatic39['Pontualidade Partida'] == 'Não pontual'].reset_index()

tatic42 = tatic38.groupby('Pontualidade Chegada').count().reset_index()
tatic43 = tatic42[tatic42['Pontualidade Chegada'] == 'Pontual'].reset_index()
tatic44 = tatic42[tatic42['Pontualidade Chegada'] == 'Não pontual'].reset_index()

metar_aux = metar.copy()
metar_aux['data'] = metar_aux['data'].astype('datetime64[ns]')

metar2_aux = metar_aux[metar_aux['data'] > start_date4]
metar3_aux = metar2_aux[metar2_aux['data'] < end_date4]
metar4_aux3 = metar3_aux[metar3_aux['temperatura do ar (Nr)'] != ' ']
metar4_aux3['temperatura do ar (Nr)'] = metar4_aux3['temperatura do ar (Nr)'].astype(int)
metar4_aux3['temperatura de orvalho (Nr)'] = metar4_aux3['temperatura de orvalho (Nr)'].astype(int)
metar4_aux4 = metar4_aux3[metar4_aux3['vento (Nr)'] != ' ']
metar4_aux4['vento (Nr)'] = metar4_aux4['vento (Nr)'].astype(int)
metar4_aux4['pressão (Nr)'] = metar4_aux4['pressão (Nr)'].astype(int)

if (aeroporto_select == 'Selecione o aeroporto'):

    resultado6.metric(label ='Pontualidade de Partida', value = str(round(100*tatic30['Número Voo'][0]/(tatic31['Número Voo'][0]+tatic30['Número Voo'][0])))+'%')
    resultado7.metric(label ='Pontualidade de Chegada', value = str(round(100*tatic33['Número Voo'][0]/(tatic34['Número Voo'][0]+tatic33['Número Voo'][0])))+'%')
    resultado8.metric(label ='Temperatura do ar', value = str(round(metar4_aux2['temperatura do ar (Nr)'].mean()))+'ºC')
    resultado9.metric(label ='Temperatura de orvalho', value = str(round(metar4_aux2['temperatura de orvalho (Nr)'].mean()))+'ºC')
    resultado10.metric(label ='Vento', value = round(metar4_aux2['vento (Nr)'].mean()))
    resultado11.metric(label ='Pressão', value = round(metar4_aux2['pressão (Nr)'].mean()))

else:

    resultado6.metric(label ='Pontualidade de Partida', value = str(round(100*tatic40['Número Voo'][0]/(tatic41['Número Voo'][0]+tatic40['Número Voo'][0])))+'%', delta = str(round(100*(tatic40['Número Voo'][0]/(tatic41['Número Voo'][0]+tatic40['Número Voo'][0]) - tatic30['Número Voo'][0]/(tatic31['Número Voo'][0]+tatic30['Número Voo'][0]))))+'% em relação à média')
    resultado7.metric(label ='Pontualidade de Chegada', value = str(round(100*tatic43['Número Voo'][0]/(tatic44['Número Voo'][0]+tatic43['Número Voo'][0])))+'%', delta = str(round(100*(tatic43['Número Voo'][0]/(tatic44['Número Voo'][0]+tatic43['Número Voo'][0]) - tatic33['Número Voo'][0]/(tatic34['Número Voo'][0]+tatic33['Número Voo'][0]))))+'% em relação à média')
    resultado8.metric(label ='Temperatura do ar', value = str(round(metar4_aux2['temperatura do ar (Nr)'].mean()))+'ºC', delta = str(round(metar4_aux2['temperatura do ar (Nr)'].mean() - metar4_aux4['temperatura do ar (Nr)'].mean()))+'ºC em relação à média')
    resultado9.metric(label ='Temperatura de orvalho', value = str(round(metar4_aux2['temperatura de orvalho (Nr)'].mean()))+'ºC', delta = str(round(metar4_aux2['temperatura de orvalho (Nr)'].mean() - metar4_aux4['temperatura de orvalho (Nr)'].mean()))+'ºC em relação à média')
    resultado10.metric(label ='Vento', value = round(metar4_aux2['vento (Nr)'].mean()), delta = str(round(metar4_aux2['vento (Nr)'].mean() - metar4_aux4['vento (Nr)'].mean()))+' em relação à média')
    resultado11.metric(label ='Pressão', value = round(metar4_aux2['pressão (Nr)'].mean()), delta = str(round(metar4_aux2['pressão (Nr)'].mean() - metar4_aux4['pressão (Nr)'].mean()))+' em relação à média')

### Plotando gráficos 7 a 14

grafico7.plotly_chart(fig7)
grafico8.plotly_chart(fig8)
grafico9.plotly_chart(fig9)
grafico10.plotly_chart(fig10)
grafico11.plotly_chart(fig11)
grafico12.plotly_chart(fig12)
grafico13.plotly_chart(fig13)
grafico14.plotly_chart(fig14)