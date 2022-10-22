import pandas as pd
import streamlit as st

def inserir_linha(df, linha):
    df = df.append(linha, ignore_index=False)
    df = df.sort_index().reset_index(drop=True)
    return df

def check_data(df2):
    df = df2.rename(columns = {'dt_referencia':'date'}, inplace = True)
    # Transformamos a coluna date, que anteriormente era texto para formato datetime
    df.dt_referencia = pd.to_datetime(df.date)
    
    # Atribuimos a essas variáveis o dia inicial e final do dataframe completo
    start_date_dataframe = df.date[0]
    end_date_dataframe = df.date[df.shape[0] - 1]
    
    # Atribuimos a essas variáveis o filtro de data, passando como parâmetros
    # nome do campo, data selecionada ao clicar pela primeira vez, valores mínimos e máximos permitidos
    start_date = st.sidebar.date_input('Dia inicial', start_date_dataframe, min_value=start_date_dataframe,
                                       max_value=end_date_dataframe)
    end_date = st.sidebar.date_input('Dia final', end_date_dataframe, min_value=start_date_dataframe,
                                     max_value=end_date_dataframe)
    
    # Exibimos um aviso exibindo a data inicial e final selecionadas
    st.sidebar.success('Data inicial: `%s`\n\nData final: `%s`' % (start_date, end_date))
    
    # Convertemos as datas para o formato YYYY-MM-DD
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    
    # Transformamos o index do dataframe para as datas, visto que somente possuímos uma entrada por dia
    # e também para realizarmos o filtro no comando a seguir
    df = df.set_index(['date'])
    
    # Realizamos um filtro com o comando loc passando a data inicial e final selecionadas anteriormente
    # nos filtros, e passamos o dataframe filtrado para a variável df
    df = df.loc[start_date:end_date]
    
    # Retornamos o método com a variável df modificada pelo filtro
    return df