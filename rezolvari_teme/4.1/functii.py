import pandas as pd
import pandas.api.types as tip
from scipy.stats import entropy
import numpy as np


def nan_replace(t):
    assert isinstance(t, pd.DataFrame)
    variabile = list(t.columns)
    for variabila in variabile:
        if any(t[variabila].isna()):
            if tip.is_numeric_dtype(t[variabila]):
                t[variabila].fillna(t[variabila].mean(), inplace=True)
            else:
                modulul = t[variabila].mode()[0]
                t[variabila].fillna(modulul, inplace=True)


def segregare_S(t, v):
    assert isinstance(t, pd.DataFrame)
    x = t[v].values
    sume = np.sum(x, axis=0)
    sume[sume == 0] = 1
    p = x / sume
    p[p == 0] = 1
    e = entropy(p, base=2, axis=0)
    s_e = pd.Series(data=e, index=v)
    return s_e


def segregare_D(t, v):
    assert isinstance(t, pd.DataFrame)
    x = t[v].values
    sume_linii = np.sum(x, axis=1)
    r = np.transpose(sume_linii - x.T)
    t_x = np.sum(x, axis=0)
    t_r = np.sum(r, axis=0)
    t_x[t_x == 0] = 1
    t_r[t_r == 0] = 1
    p_x = x / t_x
    p_r = r / t_r
    dif = np.abs(p_x - p_r)
    sum_dif = 0.5 * np.sum(dif, axis=0)
    return pd.Series(data=sum_dif, index=v)
