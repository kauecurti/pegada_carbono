Projeto de Cálculo da Pegada de Carbono para Consumo de Energia

Este projeto foi desenvolvido com Django e Django Rest Framework, integrando funcionalidades para calcular a pegada de carbono baseada no consumo de energia. O sistema utiliza variáveis como localização, fonte de energia, horário de consumo, e estação do ano para realizar os cálculos automaticamente e retornar os resultados via API.

Funcionalidades Principais

1. Cálculo Automático da Pegada de Carbono

Com base no consumo de energia em kWh, a pegada de carbono é calculada automaticamente considerando:

Fonte de Energia: Hidrelétrica, Solar, Eólica, Térmica, etc.

Horário de Consumo: Horário de pico ou normal.

Localização: Sudeste, Nordeste, Sul (com diferentes coeficientes de emissão).

Estação do Ano: Verão, Inverno, Primavera, Outono.

A fórmula é ajustada para cada região e tipo de fonte de energia.

1. Integração com API para Criação e Atualização de Contas de Energia

A API aceita requisições POST e PUT para criar e atualizar registros de consumo de energia.

A pegada de carbono é recalculada automaticamente a cada atualização.

1. Validação de Dados

Validação automática para garantir que todos os dados necessários (consumo, localização, fonte de energia) sejam fornecidos corretamente.

1. Estrutura Modular para Expansão

O projeto foi estruturado de forma modular para facilitar a criação de outros aplicativos para calcular a pegada de carbono de outros consumos, como água ou lixo.

Instalação do Projeto

Pré-requisitos

Python 3.8+

Django 3.0+

Django Rest Framework

Passos de Instalação

Clone o Repositório


git clone https://github.com/seu-projeto.git

cd seu-projeto

Crie e Ative um Ambiente Virtual


python3 -m venv venv

source venv/bin/activate  # No Windows use: venv\Scripts\activate

Instale as Dependências


pip install -r requirements.txt

Configure as Variáveis de Ambiente Crie um arquivo .env na raiz do projeto e adicione as seguintes variáveis:


SECRET\_KEY=sua\_secret\_key\_aqui

DEBUG=True

Execute as Migrações


python manage.py makemigrations

python manage.py migrate

Inicie o Servidor


python manage.py runserver

Estrutura do Projeto



projeto\_pegada/

│

├── energia/                     # App responsável pelo cálculo da pegada de carbono de energia

│   ├── \_\_init\_\_.py

│   ├── admin.py

│   ├── apps.py

│   ├── migrations/

│   ├── models.py                # Modelo ContaEnergia

│   ├── serializers.py           # Serializador ContaEnergia

│   ├── tasks.py                 # Lógica para tarefas Celery (se aplicável)

│   ├── views.py                 # API para cálculo de pegada de carbono

│   ├── urls.py                  # URLs da API

│   └── tests.py

├── projeto\_pegada/              # Diretório principal do projeto

│   ├── \_\_init\_\_.py

│   ├── settings.py              # Configurações do projeto

│   ├── urls.py                  # URLs do projeto

│   ├── wsgi.py

│   ├── asgi.py

├── manage.py                    # Script de gerenciamento do Django

├── requirements.txt             # Lista de dependências do projeto

└── README.md                    # Documentação do projeto

Explicação das Funcionalidades

1. Conta de Energia (Modelos)

O modelo ContaEnergia é a peça central do cálculo da pegada de carbono com base no consumo de energia.

Atributos do Modelo:

id\_conta: Identificador único para a conta de energia.

consumo\_kwh: Consumo em kWh.

localizacao: Localização geográfica do consumidor.

fonte\_energia: Fonte de energia utilizada (hidrelétrica, solar, térmica, etc.).

horario\_consumo: Se o consumo foi realizado em horário de pico ou horário normal.

estacao\_ano: Estação do ano correspondente ao consumo (verão, inverno, etc.).

pegada\_de\_carbono: Valor calculado da pegada de carbono com base nas variáveis fornecidas.

1. Serializer

O ContaEnergiaSerializer é responsável por transformar os dados do modelo em JSON para uso na API. Ele também recalcula a pegada de carbono ao criar ou atualizar uma conta de energia.

create: Cria uma nova conta de energia e calcula a pegada de carbono.

update: Atualiza os dados de uma conta existente e recalcula a pegada de carbono.

1. API

A API foi construída com Django Rest Framework e permite realizar as operações de criar e atualizar contas de energia.

POST /api/energia: Cria uma nova conta de energia.

PUT /api/energia/{id\_conta}: Atualiza uma conta de energia existente e recalcula a pegada de carbono.

1. Expansão para Outros Apps (Água, Lixo, etc.)

Se você deseja expandir este projeto para calcular a pegada de carbono de outros consumos (como água ou lixo), basta criar novos apps no Django e seguir uma estrutura semelhante à do app energia.

Criando o App para Cálculo de Pegada de Carbono de Água:

Criar o App de Água:


python manage.py startapp agua

Definir o Modelo (agua/models.py):

python

from django.db import models

class ContaAgua(models.Model):

id\_conta = models.CharField(max\_length=100, unique=True)

consumo\_litros = models.FloatField()  # Consumo em litros de água

localizacao = models.CharField(max\_length=100)

estacao\_ano = models.CharField(max\_length=50, choices=[('verao', 'Verão'), ('inverno', 'Inverno'), ('outono', 'Outono'), ('primavera', 'Primavera')])

pegada\_de\_carbono = models.FloatField(null=True, blank=True)

def calcular\_pegada\_de\_carbono(self):

\# Adicione a lógica de cálculo para água

fator\_emissao = 0.002  # Exemplo: 0.002 kg CO2 por litro de água consumida

self.pegada\_de\_carbono = self.consumo\_litros \* fator\_emissao

return self.pegada\_de\_carbono

Serializador para Água (agua/serializers.py):

python

from rest\_framework import serializers

from .models import ContaAgua

class ContaAguaSerializer(serializers.ModelSerializer):

class Meta:

model = ContaAgua

fields = ['id\_conta', 'consumo\_litros', 'pegada\_de\_carbono']

Definir as Views e URLs (agua/views.py e agua/urls.py), seguindo a mesma lógica do app energia.

Registrar o App em settings.py:

python

INSTALLED\_APPS = [

...,

'energia',

'agua',  # Novo app para água

]

Como Expandir para Cálculos de Lixo

O processo para adicionar um app para o cálculo da pegada de carbono do lixo segue o mesmo fluxo que o cálculo de energia e água. Basta definir um novo modelo e lógica de cálculo baseada no peso ou volume de lixo gerado, por exemplo, kg CO2 por tonelada de lixo.

Exemplo de Requisição para API

Criar uma Conta de Energia (POST):

json

{

"id\_conta": "12345",

"consumo\_kwh": 350,

"localizacao": "sudeste",

"fonte\_energia": "hidreletrica",

"horario\_consumo": "pico",

"estacao\_ano": "inverno"

}

Atualizar uma Conta de Energia (PUT):

json

{

"consumo\_kwh": 500,

"fonte\_energia": "solar",

"horario\_consumo": "normal",

"estacao\_ano": "verao"

}

Conclusão

Este projeto oferece uma base sólida para calcular a pegada de carbono para diferentes tipos de consumo (energia, água, lixo, etc.). A estrutura modular facilita a expansão para outros consumos, bastando criar novos apps e seguir o padrão definido.
