import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def corr_matrix(df):
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
    plt.title(title)
    sns.histplot(data=df[column])
    plt.show()

def comparative(df,x,y):
    sns.lmplot(data=df,x=x,y=y)
    plt.show()
