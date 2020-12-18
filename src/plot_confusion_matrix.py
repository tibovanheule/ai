import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sn
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

import db



def plot():
    """  plot a confusion matrix

    """
    array = [[0.96,  0.04], [ 0.70,  0.30]]
    df_cm = pd.DataFrame(array, index=[i for i in "01"], columns=[i for i in "01"])
    plt.figure(figsize=(10, 7))
    sn.set(font_scale=2.0)
    sn.heatmap(df_cm, annot=True)
    plt.show()

    array = [[0.96,  0.04], [0.74,  0.26]]
    df_cm = pd.DataFrame(array, index=[i for i in "01"], columns=[i for i in "01"])
    plt.figure(figsize=(10, 7))
    sn.set(font_scale=2.0)
    sn.heatmap(df_cm, annot=True)
    plt.show()


def accaracy():
    """  to recalculate accuracy

    """
    array = list()
    with open("predictions/logistic_regression_char_predictions", "r") as f:
        for i in f.readline():
            array.append(int(i))
    print(array)
    dbobj = db.DB()
    data = [i[0] for i in dbobj.db_load_tweet()]
    hate = [i[0] for i in dbobj.db_load_hate()]
    x_train, x_test, y_train, y_test = train_test_split(data, hate, train_size=0.7, random_state=42)
    print(accuracy_score(array, y_test, normalize=True))
