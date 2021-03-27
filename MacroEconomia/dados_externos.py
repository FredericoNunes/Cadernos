import requests
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
class DadosIbge():
    
    def contasnacionaispm():

        url = "https://apisidra.ibge.gov.br/values/t/1846/n1/all/v/all/p/all/c11255/90707,93404,93405,93406,93407,93408,102880/d/v585%200"
        
        payload = {}
        headers = {
          'Content-Type': 'application/json'
        }
        
        response = requests.request("GET", url, headers=headers, data = payload)
        response = response.json()
        
        ibge_data = pd.DataFrame(response)
        ibge_data['V'][1:] = [int(valor) for valor in ibge_data['V'][1:]]
        ibge_data = ibge_data.pivot(index='D3C',
                             columns='D4N',
                             values='V')
        ibge_data = ibge_data.drop(columns=['Setores e subsetores'],index=['Trimestre (Código)'])

        
        dti = pd.date_range('1996-06-01', periods=len(ibge_data.index), freq='Q')
        ibge_data = ibge_data.set_index(dti)
        ibge_data = ibge_data.rename_axis('Trimestre')
        return ibge_data
    
    def ipcamensal():
        
        
        url = "https://apisidra.ibge.gov.br/values/t/1737/n1/all/v/63/p/last%20294/d/v63%202"
        payload = {}
        headers = {'Content-Type': 'application/json'}
        response = requests.request("GET", url, headers=headers, data = payload)
        response = response.json()
        ibge_data = pd.DataFrame(response)
        ibge_data['V'][1:] = [float(valor) for valor in ibge_data['V'][1:]]
        ibge_data = ibge_data.pivot(index='D3C',
                            columns='D2N',
                            values='V')
        ibge_data = ibge_data.drop(columns=['Variável'],index=['Mês (Código)'])
        dti = pd.date_range('1996-08-01', periods=len(ibge_data.index), freq='M')
        ibge_data = ibge_data.set_index(dti)
        ibge_data = ibge_data.rename_axis('Mensal')
        return ibge_data
        
        
    def plotContasNacionais():
        df_contasNacionais = DadosIbge.contasnacionaispm()
        
        plotContasNacionais = plt.figure(constrained_layout=True,figsize=(15,12))
        gs = plotContasNacionais.add_gridspec(4, 4)
        pib = plotContasNacionais.add_subplot(gs[0, :])
        pib.set_title('PIB a Preços de Mercado')
        pib.plot(df_contasNacionais['PIB a preços de mercado'])
        
        consumoFamilias = plotContasNacionais.add_subplot(gs[1, :2])
        consumoFamilias.set_title('Despesa de consumo das famílias')
        consumoFamilias.plot(df_contasNacionais['Despesa de consumo das famílias'])
        
        consumoGoverno = plotContasNacionais.add_subplot(gs[1, 2:])
        consumoGoverno.set_title('Despesa de consumo da administração pública')
        consumoGoverno.plot(df_contasNacionais['Despesa de consumo da administração pública'])
        
        FBKF = plotContasNacionais.add_subplot(gs[2, :2])
        FBKF.set_title('Formação bruta de capital fixo')
        FBKF.plot(df_contasNacionais['Formação bruta de capital fixo'])
        
        estoque = plotContasNacionais.add_subplot(gs[2, 2:])
        estoque.set_title('Variação de estoque')
        estoque.plot(df_contasNacionais['Variação de estoque'])
        
        exportacao = plotContasNacionais.add_subplot(gs[-1, :2])
        exportacao.set_title('Exportação de bens e serviços')
        exportacao.plot(df_contasNacionais['Exportação de bens e serviços'])
        
        importacao = plotContasNacionais.add_subplot(gs[-1, 2:])
        importacao.set_title('Importação de bens e serviços (-)')
        importacao.plot(df_contasNacionais['Importação de bens e serviços (-)'])
     
