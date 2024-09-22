Projeto de Cálculo da Pegada de Carbono com Machine Learning e Firebase

Este projeto usa Django com Celery para consumir periodicamente dados do Firebase, calcular a pegada de carbono usando um modelo de Machine Learning e atualizar os resultados no Firebase. O modelo de Machine Learning é treinado para prever a pegada de carbono com base em dados de consumo de energia, localização, tipo de fonte de energia e outras variáveis.

Requisitos
Python 3.6+
Django 3.0+
Firebase Admin SDK
Celery
Redis (para filas de tarefas do Celery)
scikit-learn (para o modelo de Machine Learning)
Instalação
Clone o repositório:


git clone https://github.com/seuprojeto/calc-pegada-carbono.git
cd calc-pegada-carbono
Crie e ative um ambiente virtual:


python3 -m venv venv
source venv/bin/activate
Instale as dependências:


pip install -r requirements.txt
Configure as credenciais do Firebase:
Baixe o arquivo de credenciais do Firebase e coloque no diretório raiz do projeto, nomeando-o como firebase-adminsdk.json.
Crie as migrações e o banco de dados:


python manage.py makemigrations
python manage.py migrate
Arquitetura do Projeto
Django: Usado como o framework web principal para gerenciar a API e a lógica do backend.
Celery: Usado para processar tarefas em segundo plano. Aqui ele é usado para verificar periodicamente novos registros no Firebase e calcular a pegada de carbono.
Firebase: Usado como o banco de dados para armazenar os dados de consumo de energia e a pegada de carbono.
scikit-learn: Usado para treinar um modelo de Machine Learning que prevê a pegada de carbono com base em dados de consumo.
Como Funciona
O Firebase armazena registros de consumo de energia, mas sem a pegada de carbono calculada.
O Celery é configurado para periodicamente verificar o Firebase e calcular a pegada de carbono para novos registros usando um modelo de Machine Learning.
O modelo de Machine Learning (treinado com dados históricos) é carregado, e a previsão da pegada de carbono é feita com base em variáveis como:
Consumo de energia (kWh)
Localização
Fonte de energia (hidrelétrica, térmica, solar, etc.)
Horário de consumo (pico/normal)
Estação do ano (verão, inverno, etc.)
O resultado é salvo no Firebase, atualizando o registro original com a pegada de carbono calculada.
Execução
Executar o Servidor Django

Inicie o servidor Django:



python manage.py runserver
Executar o Celery Worker

Para processar as tarefas, rode o worker do Celery:



celery -A projeto_pegada worker --loglevel=info
Executar o Celery Beat

Para agendar a tarefa de consulta periódica no Firebase, rode o Celery Beat:



celery -A projeto_pegada beat --loglevel=info
Arquivos Principais
projeto_pegada/celery.py

Este arquivo configura o Celery para que ele possa processar tarefas em segundo plano e agendar execuções periódicas.

app = Celery('projeto_pegada'): Inicializa o Celery para o projeto.
app.config_from_object('django.conf
', namespace='CELERY'): Lê as configurações do Celery a partir do arquivo settings.py.
app.autodiscover_tasks(): Descobre automaticamente tarefas definidas nos apps do Django (neste caso, no app energia).
energia/tasks.py

Este arquivo define a tarefa verificar_firebase, que é agendada pelo Celery para rodar periodicamente.

verificar_firebase(): Esta função consulta o Firebase para encontrar novos registros de consumo de energia que ainda não têm a pegada de carbono calculada. Ela processa esses registros e usa o modelo de Machine Learning para calcular a pegada de carbono, atualizando os resultados no Firebase.
db.collection('contasEnergia'): Acessa a coleção no Firebase que armazena os dados das contas de energia.
modelo_pegada.predict(): Usa o modelo de Machine Learning para fazer a previsão da pegada de carbono.
conta_ref.update(): Atualiza o registro no Firebase com o valor da pegada de carbono.
energia/views.py

Este arquivo contém a lógica da API para calcular a pegada de carbono, embora no fluxo final ela seja usada pelo Celery.

CalcularPegadaAPIView: Classe que define a API para calcular e salvar a pegada de carbono no Firebase. Esta API pode ser chamada diretamente, mas agora o foco é automatizar via Celery.
post(): Recebe os dados via requisição POST, processa as informações, faz o cálculo da pegada de carbono e atualiza o Firebase com o resultado.
train_model.py

Este script é usado para treinar o modelo de Machine Learning que será usado para calcular a pegada de carbono. Ele carrega os dados de treinamento, treina um Random Forest Regressor e salva o modelo em um arquivo .pkl que será carregado posteriormente no Django.

X_train, X_test, y_train, y_test = train_test_split(): Divide os dados em conjuntos de treino e teste.
model.fit(): Treina o modelo com os dados de treino.
joblib.dump(): Salva o modelo treinado em um arquivo .pkl.
Configuração do Firebase
Para configurar o Firebase, siga os passos abaixo:

Crie um projeto no Firebase Console.
Navegue até Configurações do Projeto > Contas de Serviço e clique em Gerar nova chave privada. Isso irá baixar um arquivo JSON.
Renomeie o arquivo JSON para firebase-adminsdk.json e coloque-o na raiz do projeto.
O Firebase será usado tanto para buscar novos registros de consumo quanto para salvar as previsões da pegada de carbono.
Dependências
Django: Framework web utilizado para gerenciar a API e a lógica backend.
Firebase Admin SDK: Usado para interagir com o banco de dados Firestore no Firebase.
Celery: Utilizado para tarefas em segundo plano e agendamento de tarefas periódicas.
Redis: Usado como o broker de mensagens do Celery para gerenciar as filas de tarefas.
scikit-learn: Usado para treinar e carregar o modelo de Machine Learning.
joblib: Usado para salvar e carregar o modelo treinado.
Agendamento de Tarefas
O Celery Beat é responsável por agendar a tarefa verificar_firebase, que é executada periodicamente. No arquivo settings.py, o agendamento está configurado para rodar a cada 60 segundos:

python

CELERY_BEAT_SCHEDULE = {
    'verificar_firebase_periodicamente': {
        'task': 'energia.tasks.verificar_firebase',
        'schedule': 60.0,  # Executa a cada 60 segundos
    },
}
Conclusão
Este projeto automatiza o cálculo da pegada de carbono de registros de consumo de energia no Firebase, usando Machine Learning para prever os resultados e Celery para verificar periodicamente novos registros. Ele pode ser expandido para incluir mais variáveis no modelo de ML, aumentar a frequência de verificações ou melhorar a interface com o Firebase.