# Webscraping do site Books To Scrape

Este projeto é gerenciado pelo Poetry e tem como objetivo coletar dados de livros do site [Books To Scrape](http://books.toscrape.com/) utilizando técnicas de webscraping. Os dados coletados incluem a categoria, nome do livro, preço e o status em estoque. Em seguida, esses dados são salvos em um arquivo CSV que é armazenado em um bucket da AWS S3. Além disso, o script está agendado e sendo executado pelo serviço Lambda Function da AWS.

## Pré-requisitos

Para executar este projeto, você precisará ter o seguinte instalado em sua máquina:

- Python 3.x
- Poetry
- Bibliotecas Python: `beautifulsoup4`, `requests` e `boto3`
- Serveless framework

Além disso, você também precisará de uma conta na AWS com as permissões necessárias para criar e executar funções Lambda, criar um bucket S3 e configurar um trigger para a função Lambda.

## Como executar

1. Clone este repositório em sua máquina.
2. No diretório raiz do projeto, execute o seguinte comando para instalar as dependências:

   ```bash
   poetry install

3. Configure as suas credenciais da AWS no seu ambiente de desenvolvimento. Você pode fazer isso criando um arquivo ~/.aws/credentials e adicionando as suas credenciais. Veja aqui para mais informações.

4. No arquivo bucket_name.py, configure as variáveis bucket_name com o nome do seu bucket.

5. execute o seguinte comando para rodar o script localmente:
 
   ```bash
   poetry run python handler.py

6. Para fazer o deploy da função Lambda, execute os seguintes comandos:

   ```bash
   sls deploy

7. Por fim, você pode configurar um trigger para a função Lambda que execute o script periodicamente, conforme necessário. Por exemplo, você pode criar um evento CloudWatch que execute a função Lambda a cada 24 horas.
