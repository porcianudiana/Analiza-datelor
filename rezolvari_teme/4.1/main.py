import pandas as pd
import functii as f

etnii = pd.read_csv("Ethnicity.csv", index_col=0)
f.nan_replace(etnii)
# Citire coduri
localitati = pd.read_excel("CoduriRomania.xlsx", index_col=0)
judete = pd.read_excel("CoduriRomania.xlsx", sheet_name=1, index_col=0)
regiuni = pd.read_excel("CoduriRomania.xlsx",
                        sheet_name="Regiuni", index_col=0)

variabile = list(etnii.columns)[1:]

# Calcul populatie pe etnii la nivel de judet
t1 = etnii.merge(right=localitati, left_index=True, right_index=True)
variabile1 = variabile + ["County"]
g1 = t1[variabile1].groupby(by="County").agg(sum)
# print(g1)
assert isinstance(g1, pd.DataFrame)
g1.to_csv("PopulatieJudete.csv")

# Calcul populatie pe etnii la nivel de regiune
t2 = g1.merge(right=judete, left_index=True, right_index=True)
variabile2 = variabile + ["Regiune"]
g2 = t2[variabile2].groupby(by="Regiune").agg(sum)
g2.to_csv("PopulatieRegiuni.csv")

# Calcul populatie pe etnii la nivel de macroregiune
assert isinstance(g2, pd.DataFrame)
t3 = g2.merge(right=regiuni, left_index=True, right_index=True)
variabile3 = variabile + ["MacroRegiune"]
g3 = t3[variabile3].groupby(by="MacroRegiune").agg(sum)
g3.to_csv("PopulatieMacroregiuni.csv")

# Calcul segregare la nivel de judet dupa indexul Shannon
segregare_Shannon = t1[variabile1].groupby(by="County").agg(
    func = f.segregare_S, v = variabile
)
segregare_Shannon.to_csv("SegregareShannon.csv")

segregare_Disim = t1[variabile1].groupby(by="County").agg(
    func = f.segregare_D, v = variabile
)
segregare_Disim.to_csv("SegregareDisimilaritate.csv")

