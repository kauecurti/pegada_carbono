import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib

# Exemplo de dados: você pode carregar seus dados reais aqui
# dataframe = pd.read_csv('seus_dados.csv')
data = {
    'consumo_kwh': [150, 300, 200, 450, 500],
    'localizacao': ['sudeste', 'nordeste', 'sul', 'sudeste', 'nordeste'],
    'fonte_energia': ['hidreletrica', 'termica', 'solar', 'termica', 'eolica'],
    'horario_consumo': ['pico', 'normal', 'normal', 'pico', 'pico'],
    'estacao_ano': ['verao', 'inverno', 'outono', 'primavera', 'inverno'],
    'pegada_de_carbono': [10.5, 55.2, 22.5, 66.4, 30.5]
}

df = pd.DataFrame(data)

# Transformando variáveis categóricas em variáveis dummy (one-hot encoding)
df = pd.get_dummies(df, columns=['localizacao', 'fonte_energia', 'horario_consumo', 'estacao_ano'], drop_first=True)

# Separando features (X) e target (y)
X = df.drop('pegada_de_carbono', axis=1)
y = df['pegada_de_carbono']

# Dividindo os dados em treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinando o modelo
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Fazendo previsões
y_pred = model.predict(X_test)

# Avaliando o modelo
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Salvando o modelo
joblib.dump(model, 'modelo_pegada_carbono.pkl')
