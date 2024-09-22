from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ContaEnergia
from .serializers import ContaEnergiaSerializer
import firebase_admin
from firebase_admin import credentials, firestore

# Inicializando o Firebase
cred = credentials.Certificate('firebase-adminsdk.json')  # Caminho para o arquivo JSON do Firebase
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()  # Conectando ao Firestore

class CalcularPegadaAPIView(APIView):
    def post(self, request):
        dados = request.data
        id_conta = dados.get('id_conta')
        consumo_kwh = dados.get('consumo_kwh')
        localizacao = dados.get('localizacao')
        fonte_energia = dados.get('fonte_energia')
        horario_consumo = dados.get('horario_consumo')
        estacao_ano = dados.get('estacao_ano')

        if not all([id_conta, consumo_kwh, localizacao, fonte_energia, horario_consumo, estacao_ano]):
            return Response({'error': 'Dados incompletos.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Cria ou atualiza o registro no banco de dados Django
            conta, created = ContaEnergia.objects.update_or_create(
                id_conta=id_conta,
                defaults={
                    'consumo_kwh': consumo_kwh,
                    'localizacao': localizacao,
                    'fonte_energia': fonte_energia,
                    'horario_consumo': horario_consumo,
                    'estacao_ano': estacao_ano
                }
            )

            # Calcula a pegada de carbono usando o método do modelo
            conta.calcular_pegada_de_carbono()
            conta.save()

            # Salva o cálculo no Firebase
            doc_ref = db.collection('contasEnergia').document(id_conta)
            doc_ref.set({
                'id_conta': id_conta,
                'consumo_kwh': consumo_kwh,
                'pegada_de_carbono': conta.pegada_de_carbono,
                'localizacao': localizacao,
                'fonte_energia': fonte_energia,
                'horario_consumo': horario_consumo,
                'estacao_ano': estacao_ano
            })

            # Serializa e retorna os dados
            serializer = ContaEnergiaSerializer(conta)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

        """ 
        
        from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ContaEnergia
from .serializers import ContaEnergiaSerializer
import joblib
import os

# Carregando o modelo de ML treinado
modelo_path = os.path.join(os.path.dirname(__file__), 'modelo_pegada_carbono.pkl')
modelo_pegada = joblib.load(modelo_path)

# Mapeamento para transformar as categorias em variáveis dummies (one-hot encoding)
categorias = {
    'localizacao': {'sudeste': 0, 'nordeste': 0, 'sul': 0},
    'fonte_energia': {'hidreletrica': 0, 'termica': 0, 'solar': 0, 'eolica': 0},
    'horario_consumo': {'pico': 0, 'normal': 0},
    'estacao_ano': {'verao': 0, 'inverno': 0, 'outono': 0, 'primavera': 0},
}

# API para calcular e salvar a pegada de carbono com o modelo de ML
class CalcularPegadaAPIView(APIView):
    def post(self, request):
        dados = request.data
        id_conta = dados.get('id_conta')
        consumo_kwh = dados.get('consumo_kwh')
        localizacao = dados.get('localizacao')
        fonte_energia = dados.get('fonte_energia')
        horario_consumo = dados.get('horario_consumo')
        estacao_ano = dados.get('estacao_ano')

        if not all([id_conta, consumo_kwh, localizacao, fonte_energia, horario_consumo, estacao_ano]):
            return Response({'error': 'Dados incompletos.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Preparando os dados para previsão (transformando as variáveis categóricas)
            input_dados = [
                consumo_kwh,
                categorias['localizacao'].get(localizacao.lower(), 0),
                categorias['fonte_energia'].get(fonte_energia.lower(), 0),
                categorias['horario_consumo'].get(horario_consumo.lower(), 0),
                categorias['estacao_ano'].get(estacao_ano.lower(), 0),
            ]

            # Fazendo a previsão da pegada de carbono com o modelo de ML
            pegada_de_carbono = modelo_pegada.predict([input_dados])[0]

            # Cria ou atualiza o registro no banco de dados Django
            conta, created = ContaEnergia.objects.update_or_create(
                id_conta=id_conta,
                defaults={
                    'consumo_kwh': consumo_kwh,
                    'pegada_de_carbono': pegada_de_carbono
                }
            )

            # Serializa e retorna os dados
            serializer = ContaEnergiaSerializer(conta)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
        """