import pandas as pd
import functii as f
import numpy as np

prezenta = pd.read_csv("prezenta_vot.csv", index_col=0)
f.nan_replace(prezenta)
# print(prezenta)
variabile = list(prezenta)
# print(variabile)
variabile1 = variabile[3:10]
variabile2 = variabile[10:]
# print(variabile1,variabile2,sep="\n")

# Cerinta 1
procent = prezenta["LT"] * 100 / (prezenta["Votanti_LP"] + prezenta["Votanti_LS"])
t1 = prezenta[procent > 50]
t1.to_csv("Prezenta50.csv")

# Cerinta 2
prezenta["procent"] = procent
t2 = prezenta[["Localitate", "Judet", "procent"]].sort_values(by="procent", ascending=False)
t2.to_csv("PrezentaSort.csv")

# Cerinta 2. Versiunea 2
k = np.flipud(np.argsort(procent))
# print(k)
t2_ = prezenta[["Localitate", "Judet", "procent"]].iloc[k, :]
t2_.to_csv("PrezentaSort_.csv")

# Cerinta 3
judete = pd.read_excel("CoduriRomania.xlsx", sheet_name="Judete", index_col=0)
assert isinstance(jut3 = ete, pd.DataFrame)
prezenta_complet = judete.merge(
    right=prezenta,
    left_index=True,
    right_on="Judet"
)
t3 = prezenta_complet[variabile1 + variabile2 + ["Regiune"]].groupby(by="Regiune").agg(sum)
t3.to_csv("Regiuni.csv")

# Cerinta 4
t4 = prezenta[["Localitate"] + variabile2].apply(func=f.vot_categorii, axis=1)
t4.to_csv("Varsta.csv")

# Cerinta 5
categorie_varsta = "Femei_65_"
t5 = t4[t4["Categoria"]==categorie_varsta]
t5.to_csv(categorie_varsta+".csv")
