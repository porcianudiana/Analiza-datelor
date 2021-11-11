import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np


def nan_replace(t):
    assert isinstance(t, pd.DataFrame)
    variabile = list(t.columns)
    for variabila in variabile:
        if any(t[variabila].isna()):
            if is_numeric_dtype(t[variabila]):
                t[variabila].fillna(t[variabila].mean(), inplace=True)
            else:
                modulul = t[variabila].mode()[0]
                t[variabila].fillna(modulul, inplace=True)


def vot_categorii(t):
    assert isinstance(t, pd.Series)
    k = np.argmax(t.iloc[1:]) + 1
    s = pd.Series(data={
        "Localitatea": t.iloc[0],
        "Categoria": t.index[k]
    })
    return s
