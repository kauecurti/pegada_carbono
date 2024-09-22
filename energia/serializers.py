from rest_framework import serializers
from .models import ContaEnergia

class ContaEnergiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContaEnergia
        fields = [
            'id_conta', 
            'consumo_kwh', 
            'localizacao', 
            'fonte_energia', 
            'horario_consumo', 
            'estacao_ano', 
            'pegada_de_carbono'
        ]
        read_only_fields = ['pegada_de_carbono']  # Torna a pegada de carbono somente leitura

    def create(self, validated_data):
        # Criar uma nova conta de energia
        conta_energia = ContaEnergia.objects.create(**validated_data)
        # Calcular a pegada de carbono ao salvar
        conta_energia.calcular_pegada_de_carbono()
        conta_energia.save()
        return conta_energia

    def update(self, instance, validated_data):
        # Atualiza a conta de energia com novos dados
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        # Recalcular a pegada de carbono ao atualizar
        instance.calcular_pegada_de_carbono()
        instance.save()
        return instance
