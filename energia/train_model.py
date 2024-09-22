import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

# Exemplo de dados fictícios - substitua por seus dados reais
data = {
    'consumo_kwh': [150, 300, 200, 450, 500],
    'localizacao': ['sudeste', 'nordeste', 'sul', 'sudeste', 'nordeste'],
    'fonte_energia': ['hidreletrica', 'termica', 'solar', 'termica', 'eolica'],
    'horario_consumo': ['pico', 'normal', 'normal', 'pico', 'pico'],
    'estacao_ano': ['verao', 'inverno', 'outono', 'primavera', 'inverno'],
    'pegada_de_carbono': [10.5, 55.2, 22.5, 66.4, 30.5]
}

df = pd.DataFrame(data)

# Definir as variáveis categóricas e numéricas
categorical_features = ['localizacao', 'fonte_energia', 'horario_consumo', 'estacao_ano']
numerical_features = ['consumo_kwh']

# Pipelines para pré-processamento
categorical_transformer = OneHotEncoder(drop='first')
numerical_transformer = StandardScaler()

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Treinando com múltiplos modelos: Regressão Linear, Random Forest, Gradient Boosting
models = {
    'LinearRegression': LinearRegression(),
    'RandomForest': RandomForestRegressor(),
    'GradientBoosting': GradientBoostingRegressor()
}

# Criar pipeline de pré-processamento seguido do modelo de machine learning
for model_name, model in models.items():
    pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('model', model)])

    # Dividir os dados
    X = df.drop('pegada_de_carbono', axis=1)
    y = df['pegada_de_carbono']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Treinar o modelo
    pipeline.fit(X_train, y_train)

    # Avaliação
    y_pred = pipeline.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f'{model_name} MSE: {mse}')

    # Salvar o modelo
    joblib.dump(pipeline, f'modelo_pegada_carbono_{model_name}.pkl')
