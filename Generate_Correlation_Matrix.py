import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys

try:
    df = pd.read_csv('Normalized_Political_2.csv')
    df.head()
    plt.figure(figsize=(9,6))
    sns.heatmap(df.corr(), annot=True, cmap=plt.cm.Reds)
    print(df.corr())
    plt.show()
except ValueError:  #raised if `y` is empty.
    pass
