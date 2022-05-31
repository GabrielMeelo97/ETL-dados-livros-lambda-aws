import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from tempfile import NamedTemporaryFile
from datetime import datetime
import json
import boto3
import logging
from os import environ as env



logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def request_inicial():
    url = 'https://books.toscrape.com/catalogue/page-1.html'
    response = requests.get(url)
    soup = bs(response.text)
    return soup

def buscar_categorias(soup):
    categorias_full = []
    for categoria in soup.find_all('li'):
        try:
            print(categoria.find('a').get('href'))
            categorias_full.append(categoria.find('a').get('href'))
        except:
            print('erro')
    return categorias_full


def acertar_categorias(lista):
    categorias = []
    for i in lista:
        print(i)
        if len(i) > 27 and i[:8] == 'category':
            categorias.append(i)
    return categorias

def acerta_url(url):
    paginas = range(1,1000000000000000000000000000000)
    numero_paginas = 0
    for i in paginas:
        url_2 = url.replace('index','page-{}.html')
        livro_response = requests.get(url_2.format(5))
        if livro_response.ok == True:
            numero_paginas = numero_paginas + 1
        else:
            break
    if numero_paginas >= 1:
        return url_2,numero_paginas
    else: 
        return url,numero_paginas


def request_api(url,categoria):
    livro_response = requests.get(url)
    livros = bs(livro_response.text)
    dados = []
    for livro in livros.find_all('li',{'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'}):
        nome_produto = livro.find('h3').find('a').get('title')
        print(nome_produto)
        preco = livro.find('p',{'class':'price_color'}).text[2:]
        estoque = livro.find('p',{'class':'instock availability'}).text.strip()
        pontuacao = str(livro.find('article',{'class':'product_pod'}).find('p'))[:30].split('"')[1].replace('star-rating ','')
        dados.append([categoria,nome_produto,preco,estoque,pontuacao])
    return dados


def coleta_dados(categorias):
    dados_livros = []
    for categoria in categorias:
        url = 'https://books.toscrape.com/catalogue/'+ categoria
        url_validada,paginas = acerta_url(url)
        cagoteria_nome = categoria[15:].split('_')[0]
        if paginas >= 1:
            for i in paginas:
                lista_dados = request_api(url_validada.format(i),cagoteria_nome)
                dados_livros.append(lista_dados)
        else:
            lista_dados = request_api(url,cagoteria_nome)     
            dados_livros.append(lista_dados)                                      
    return dados_livros

def cria_dataframe(dados):
    logger.info(f"Concatenando coleta das categorias e paginas")
    for i,k in enumerate(dados):
        if i == 0:
            df_livros = pd.DataFrame(k,columns=['categoria','nome','preco','status_estoque','estrelas'])
        else: 
            df_livros = pd.concat([df_livros,pd.DataFrame(k,columns=['categoria','nome','preco','status_estoque','estrelas'])], axis = 0)
    return df_livros



def save_bucket(df_livros):
    tempfile = NamedTemporaryFile(delete=False)
    df_livros.to_json(tempfile, orient ='records')
    now = datetime.now().strftime("%Y-%m-%d")
    s3 = boto3.client("s3")
    logger.info("Salvando json no bucket..")
    s3.put_object(Key=f'bronze/landing-date={now}/livros.json', Body=tempfile,Bucket = 'livros-scraping')
    return 'Arquivo inserido'

def main(event,context):
    soup = request_inicial()
    categorias_full = buscar_categorias(soup)
    lista_categorias = acertar_categorias(categorias_full)
    resutaldo_coleta = coleta_dados(lista_categorias)
    df_livros = cria_dataframe(resutaldo_coleta)
    save_bucket(df_livros)
    return df_livros