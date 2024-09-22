from celery import shared_task
import firebase_admin
from firebase_admin import credentials, firestore
import os
from .models import ContaEnergia
from prometheus_client import Counter
import logging

# Inicialize o logger para registrar mensagens de execução e erros
logger = logging.getLogger('django')

# Inicializar o Firebase Admin SDK
cred = credentials.Certificate('firebase-adminsdk.json')  # Certifique-se de que o arquivo está no diretório certo
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Conecte-se ao Firestore
db = firestore.client()

# Contador de previsões (exemplo usando Prometheus)
predictions_counter = Counter('predictions_total', 'Total de previsões feitas')

@shared_task
def verificar_firebase():
    """
    Tarefa que verifica o Firebase periodicamente para encontrar novos registros sem a pegada de carbono calculada.
    """
    try:
        # Acessar a coleção 'contasEnergia' no Firestore
        contas_ref = db.collection('contasEnergia')

        # Filtrar registros onde 'pegada_de_carbono' é None (ou seja, ainda não foi calculada)
        contas_nao_calculadas = contas_ref.where('pegada_de_carbono', '==', None).stream()

        for conta in contas_nao_calculadas:
            dados = conta.to_dict()
            id_conta = dados['id_conta']
            consumo_kwh = dados['consumo_kwh']
            localizacao = dados.get('localizacao', 'sudeste')
            fonte_energia = dados.get('fonte_energia', 'hidreletrica')
            horario_consumo = dados.get('horario_consumo', 'normal')
            estacao_ano = dados.get('estacao_ano', 'verao')

            # Preparando os dados para o cálculo de pegada de carbono
            conta_energia = ContaEnergia(
                id_conta=id_conta,
                consumo_kwh=consumo_kwh,
                localizacao=localizacao,
                fonte_energia=fonte_energia,
                horario_consumo=horario_consumo,
                estacao_ano=estacao_ano
            )

            # Calculando a pegada de carbono
            pegada_de_carbono = conta_energia.calcular_pegada_de_carbono()

            # Atualizando o registro no Firebase
            conta_ref = contas_ref.document(id_conta)
            conta_ref.update({
                'pegada_de_carbono': pegada_de_carbono
            })

            # Atualizando métricas (opcional)
            predictions_counter.inc()

            # Log de sucesso
            logger.info(f"Pegada de carbono calculada para a conta {id_conta}: {pegada_de_carbono}")

    except Exception as e:
        # Em caso de erro, registrar o erro
        logger.error(f"Erro ao verificar o Firebase ou calcular a pegada de carbono: {e}")
