import pandas as pd
import functii as f

etnii = pd.read_csv("Ethnicity.csv", index_col=0)

localitati = pd.read_excel("CoduriRomania.xlsx", index_col=0)
judete = pd.read_excel("CoduriRomania.xlsx", sheet_name=1, index_col=0)
regiuni = pd.read_excel("CoduriRomania.xlsx", sheet_name="Regiuni", index_col=0)

f.nan_replace(etnii)
# print(etnii)

variabile = list(etnii.columns)[1:]

# Calcul populatie pe etnii la nivel de judet
t1 = etnii.merge(right=localitati, left_index=True, right_index=True)
variabile1 = variabile + ["County"]
g1 = t1[variabile1].groupby(by="County").agg(sum)
assert isinstance(g1, pd.DataFrame)
g1.to_csv("PopulatieEtniiJudete.csv")

# Calcul populatie pe etnii la nivel de regiune
t2 = g1.merge(right=judete, left_index=True, right_index=True)
variabile2 = variabile + ["Regiune"]
g2 = t2[variabile2].groupby(by="Regiune").agg(sum)
g2.to_csv("PopulatieEtniiRegiuni.csv")

# Calcul populatie pe etnii la nivel de macroregiune
assert isinstance(g2, pd.DataFrame)
t3 = g2.merge(regiuni, left_index=True, right_index=True)
variabile3 = variabile + ["MacroRegiune"]
g3 = t3[variabile3].groupby(by="MacroRegiune").agg(sum)
g3.to_csv("PopulatieEtniiMacroregiuni.csv")

# Calcul diversitate la nivel de localitate
# print(list(t1))
div1 = t1[variabile+["City_x"]].apply(func=f.diversitate,axis=1)
div1.to_csv("DiversitateLocalitati.csv")

# Calcul diversitate la nivel de judete
div2 = g1[variabile].apply(func=f.diversitate_,axis=1,variabile=variabile)
div2.to_csv("DiversitateJudete.csv")

div3 = g2[variabile].apply(func=f.diversitate_,axis=1,variabile=variabile)
div3.to_csv("DiversitateRegiuni.csv")
