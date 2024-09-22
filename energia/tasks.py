from celery import shared_task
import firebase_admin
from firebase_admin import credentials, firestore
import joblib
import os
from .models import HistoricoPegada
from prometheus_client import Counter
import logging
import smtplib
logger = logging.getLogger('django')

# Inicializar Firebase
cred = credentials.Certificate(os.getenv('FIREBASE_CREDENTIALS'))
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Carregar o modelo de ML treinado
modelo_path = os.path.join(os.path.dirname(__file__), 'modelo_pegada_carbono.pkl')
modelo_pegada = joblib.load(modelo_path)

# Contador de métricas (Prometheus)
predictions_counter = Counter('predictions_total', 'Total de previsões feitas')

def enviar_notificacao_erro(mensagem):
    server = smtplib.SMTP(os.getenv('SMTP_SERVER'), 587)
    server.starttls()
    server.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PASSWORD'))
    server.sendmail(os.getenv('SMTP_USER'), os.getenv('ADMIN_EMAIL'), mensagem)
    server.quit()

@shared_task
def verificar_firebase():
    """
    Esta tarefa verifica periodicamente o Firebase para calcular a pegada de carbono
    para novos registros e atualiza o Firebase com os resultados.
    """
    try:
        contas_ref = db.collection('contasEnergia')
        contas_nao_calculadas = contas_ref.where('pegada_de_carbono', '==', None).stream()

        for conta in contas_nao_calculadas:
            dados = conta.to_dict()
            id_conta = dados['id_conta']
            consumo_kwh = dados['consumo_kwh']
            localizacao = dados.get('localizacao', 'sudeste')
            fonte_energia = dados.get('fonte_energia', 'hidreletrica')
            horario_consumo = dados.get('horario_consumo', 'normal')
            estacao_ano = dados.get('estacao_ano', 'verao')

            # Preparando os dados para o modelo
            input_dados = [
                consumo_kwh,
                1 if localizacao == 'sudeste' else 0,
                1 if fonte_energia == 'termica' else 0,
                1 if horario_consumo == 'pico' else 0,
                1 if estacao_ano == 'inverno' else 0
            ]

            # Previsão usando o modelo de ML
            pegada_de_carbono = modelo_pegada.predict([input_dados])[0]

            # Atualiza o Firebase
            conta_ref = db.collection('contasEnergia').document(id_conta)
            conta_ref.update({
                'pegada_de_carbono': pegada_de_carbono
            })

            # Armazenar no banco de dados (PostgreSQL)
            HistoricoPegada.objects.create(
                id_conta=id_conta,
                consumo_kwh=consumo_kwh,
                pegada_de_carbono=pegada_de_carbono,
                modelo_utilizado='RandomForest'
            )

            # Incrementar métrica do Prometheus
            predictions_counter.inc()
        
        logger.info(f"Pegada de carbono calculada para {id_conta}")

    except Exception as e:
        logger.error(f"Erro ao processar Firebase: {e}")
        enviar_notificacao_erro(f"Erro ao processar Firebase: {e}")
