import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sn


def plot():
    array = [[0.96, 0.04], [0.74, 0.26]]
    df_cm = pd.DataFrame(array, index=[i for i in "01"], columns=[i for i in "01"])
    plt.figure(figsize=(10, 7))
    sn.heatmap(df_cm, annot=True)
    plt.show()
