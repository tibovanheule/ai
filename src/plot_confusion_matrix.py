import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sn


def plot():
    array = [[0.65, 0.35], [0.58, 0.42]]
    df_cm = pd.DataFrame(array, index=[i for i in "01"], columns=[i for i in "01"])
    plt.figure(figsize=(10, 7))
    sn.heatmap(df_cm, annot=True)
    plt.show()
