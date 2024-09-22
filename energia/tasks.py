from celery import shared_task
import firebase_admin
from firebase_admin import credentials, firestore
import joblib
import os

# Inicializando o Firebase
cred = credentials.Certificate('firebase-adminsdk.json')
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

# Carregar o modelo de Machine Learning treinado
modelo_path = os.path.join(os.path.dirname(__file__), 'modelo_pegada_carbono.pkl')
modelo_pegada = joblib.load(modelo_path)

@shared_task
def verificar_firebase():
    """
    Esta tarefa será executada periodicamente para consultar o Firebase,
    calcular a pegada de carbono para novos registros e atualizar os dados no Firebase.
    """
    # Buscando registros no Firebase onde a pegada de carbono ainda não foi calculada
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

        # Prepara os dados de entrada para o modelo
        input_dados = [
            consumo_kwh,
            1 if localizacao == 'sudeste' else 0,
            1 if fonte_energia == 'termica' else 0,
            1 if horario_consumo == 'pico' else 0,
            1 if estacao_ano == 'inverno' else 0
        ]

        # Calcula a pegada de carbono usando o modelo de ML
        pegada_de_carbono = modelo_pegada.predict([input_dados])[0]

        # Atualiza o registro no Firebase com o valor da pegada de carbono
        conta_ref = db.collection('contasEnergia').document(id_conta)
        conta_ref.update({
            'pegada_de_carbono': pegada_de_carbono
        })

        print(f'Pegada de carbono calculada para a conta {id_conta}: {pegada_de_carbono}')
