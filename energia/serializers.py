from rest_framework import serializers
from .models import ContaEnergia

class ContaEnergiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContaEnergia
        fields = ['id_conta', 'consumo_kwh', 'pegada_de_carbono']
