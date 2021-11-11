import pandas as pd
import functii as f

innoptari = pd.read_csv("innoptari.csv")
f.nan_replace(innoptari)
# print(innoptari)
localitati = pd.read_excel("CoduriRomania.xlsx", index_col=0)
populatie = pd.read_csv("PopulatieLocalitati.csv", index_col=0)

# Cerinta 1
t1 = innoptari.merge(right=localitati,
                     left_on="Siruta",
                     right_index=True)
t1_ = t1[t1["Ani"] == 2016]
# print(t1_)
t1_[["Siruta", "City", "Valoare"]].to_csv("Innoptari2016.csv", index=False)

# Cerinta 2
t2 = t1[t1["Ani"] == 2015][["County", "Valoare"]].groupby(by="County").agg(sum)
t2.to_csv("InnoptariJudete2015.csv")

# Cerinta 3
t1__ = t1[["Siruta", "County", "Ani", "Valoare"]]. \
    merge(right=populatie, left_on="Siruta", right_index=True)
t3 = t1__.groupby(by=["County", "Ani"]). \
    apply(func=f.medie_ponderata, pondere="Populatie", valoare="Valoare")
t3.to_csv("InnoptariJudeteAni.csv")

# Cerinta 4
t4 = innoptari.pivot(index="Siruta", columns="Ani", values="Valoare")
# print(t4)
t4.fillna(0, inplace=True)
t4.to_csv("InnoptariAni.csv")

# Cerinta 5
t5_ = t4.merge(localitati, left_index=True, right_index=True)
t5 = t5_.groupby(by="County").agg(sum)
t5.to_csv("InnoptariJudete.csv")
