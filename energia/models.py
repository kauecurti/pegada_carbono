from django.db import models

class ContaEnergia(models.Model):
    id_conta = models.CharField(max_length=100, unique=True)  # ID da conta
    consumo_kwh = models.FloatField()  # Consumo em kWh
    localizacao = models.CharField(max_length=100)  # Localização do consumo
    fonte_energia = models.CharField(max_length=100)  # Fonte de energia (ex: hidrelétrica, termelétrica, solar)
    horario_consumo = models.CharField(max_length=50, choices=[('pico', 'Pico'), ('normal', 'Normal')])  # Horário do consumo (pico/normal)
    estacao_ano = models.CharField(max_length=50, choices=[('verao', 'Verão'), ('inverno', 'Inverno'), ('outono', 'Outono'), ('primavera', 'Primavera')])  # Estação do ano
    pegada_de_carbono = models.FloatField(null=True, blank=True)  # Pegada de carbono calculada

    # Método para calcular a pegada de carbono
    def calcular_pegada_de_carbono(self):
        # Fatores de emissão para diferentes tipos de fontes de energia (em kg CO2/kWh)
        fatores_emissao = {
            'hidreletrica': 0.01,  # Hidrelétrica (baixo impacto de carbono)
            'termica': 0.4,        # Termelétrica (combustíveis fósseis)
            'solar': 0.05,         # Energia Solar (baixo impacto de carbono)
            'eolica': 0.02         # Energia Eólica (baixo impacto de carbono)
        }

        # Fator de emissão base, considerando a fonte de energia
        fator_emissao_base = fatores_emissao.get(self.fonte_energia.lower(), 0.092)  # Padrão: média nacional

        # Ajuste de horário: Consumo em horário de pico pode ter um impacto maior
        if self.horario_consumo == 'pico':
            fator_emissao_base *= 1.2  # 20% maior em horários de pico

        # Ajuste de localização (considerando coeficientes regionais)
        coeficientes_localizacao = {
            'sudeste': 1.0,  # Normal
            'nordeste': 0.8,  # Mais energia solar/eólica (menor impacto)
            'sul': 1.1,  # Maior dependência de fontes fósseis no inverno
        }
        coeficiente_local = coeficientes_localizacao.get(self.localizacao.lower(), 1.0)

        # Ajuste por estação do ano (ex: mais consumo de eletricidade no inverno)
        if self.estacao_ano == 'inverno':
            fator_emissao_base *= 1.15  # 15% maior no inverno devido à maior necessidade de aquecimento

        # Calculando a pegada de carbono ajustada
        self.pegada_de_carbono = self.consumo_kwh * fator_emissao_base * coeficiente_local
        return self.pegada_de_carbono

    def __str__(self):
        return f"Conta {self.id_conta} - {self.consumo_kwh} kWh"
