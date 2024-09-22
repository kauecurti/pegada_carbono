from django.db import models

class ContaEnergia(models.Model):
    id_conta = models.CharField(max_length=100, unique=True)  # ID da conta
    consumo_kwh = models.FloatField()  # Consumo em kWh
    localizacao = models.CharField(max_length=100)  # Localização do consumo
    fonte_energia = models.CharField(max_length=100)  # Fonte de energia
    horario_consumo = models.CharField(max_length=50, choices=[('pico', 'Pico'), ('normal', 'Normal')])  # Horário do consumo
    estacao_ano = models.CharField(max_length=50, choices=[('verao', 'Verão'), ('inverno', 'Inverno'), ('outono', 'Outono'), ('primavera', 'Primavera')])  # Estação do ano
    pegada_de_carbono = models.FloatField(null=True, blank=True)  # Pegada de carbono calculada

    # Método para calcular a pegada de carbono
    def calcular_pegada_de_carbono(self):
        # Fatores de emissão (kg CO2/kWh)
        fatores_emissao = {
            'hidreletrica': 0.01,
            'termica': 0.4,
            'solar': 0.05,
            'eolica': 0.02
        }

        # Fator de emissão base
        fator_emissao_base = fatores_emissao.get(self.fonte_energia.lower(), 0.092)

        # Ajuste de horário
        if self.horario_consumo == 'pico':
            fator_emissao_base *= 1.2

        # Ajuste de localização
        coeficientes_localizacao = {
            'sudeste': 1.0,
            'nordeste': 0.8,
            'sul': 1.1
        }
        coeficiente_local = coeficientes_localizacao.get(self.localizacao.lower(), 1.0)

        # Ajuste por estação do ano
        if self.estacao_ano == 'inverno':
            fator_emissao_base *= 1.15

        # Calculando a pegada de carbono
        self.pegada_de_carbono = self.consumo_kwh * fator_emissao_base * coeficiente_local
        return self.pegada_de_carbono
