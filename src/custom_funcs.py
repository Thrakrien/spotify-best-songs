import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import optuna
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error


def corr_matrix(df):
    """
    Calcula e plota uma matriz de correlação de Pearson.

    Args:
        df (pandas.DataFrame): DataFrame a ter os dados plotados

    Returns:
        None
    """
    correlation = df.corr(method='pearson',
                          numeric_only=True)
    mask = np.triu(np.ones_like(correlation,dtype=bool))
    mask[0,2]=True
    plt.figure(figsize=(16, 6))
    plt.title('Correlation')
    sns.heatmap(correlation,
                mask=mask,
                annot=True,
                cmap='coolwarm',
                vmin=-1,
                vmax=1)
    plt.show()


def histogram(df,column,title):
    """
    Plota um histograma.

    Args:
        df (pandas.DataFrame): DataFrame a ser observado.

        column (pandas.Series): Coluna a ter os dados plotados.

        title (str): Título do gráfico.

    Returns:
        None
    """
    plt.title(title)
    sns.histplot(data=df[column])
    plt.show()


def comparative(df,x,y):
    """
    Plota um gráfico de dispersão com a linha de tendência.

    Args:
        df (pandas.DataFrame): DataFrame a ser observado.

        x (pandas.Series): Dados que serão dispostos no eixo X.

        y (pandas.Series): Dados que serão dispostos no eixo Y.
    
    Returns:
        None
    """
    sns.lmplot(data=df,x=x,y=y)
    plt.show()


def objective(trial):
    # Definindo os hiperparâmetros para otimização
    learning_rate = trial.suggest_float("learning_rate", 0.01, 0.2, log=True)
    n_estimators = trial.suggest_int("n_estimators", 100, 1000, step=100)
    max_depth = trial.suggest_int("max_depth", 3, 10)
    min_samples_split = trial.suggest_int("min_samples_split", 2, 10)
    min_samples_leaf = trial.suggest_int("min_samples_leaf", 1, 10)

    # Cria e treina o modelo com os hiperparâmetros sugeridos pelo Optuna
    model = GradientBoostingRegressor(
        learning_rate=learning_rate,
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        min_samples_leaf=min_samples_leaf,
        random_state=42,
    )
    model.fit(X_train, y_train)

    # Calcula a métrica de erro no conjunto de teste
    y_pred = model.predict(X_test)
    mse = mean_absolute_error(y_test, y_pred)

    return mse


def optimize():
    # Define o estudo do Optuna
    study = optuna.create_study(direction="minimize")

    # Inicia a otimização dos hiperparâmetros
    study.optimize(objective, n_trials=100)

    # Obtém os melhores hiperparâmetros e o menor valor da métrica
    best_params = study.best_params
    best_value = study.best_value

    print("Melhor valor da métrica:", best_value)
    print("Melhores hiperparâmetros:", best_params)


if __name__ == "__main__":
    optimize()