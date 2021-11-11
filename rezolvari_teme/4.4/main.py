import pandas as pd
import functii as f

vot = pd.read_csv("vot_senat.csv", index_col=0)
f.nan_replace(vot)
# print(vot)
variabile = list(vot.columns)
partide = variabile[2:]

# Cerinta 1
t1 = vot.apply(func=f.calcul_procente, axis=1,
               variabile=partide,
               variabila_raport="nr_voturi")
# print(t1)
t1.to_csv("vot_procente.csv")

# Cerinta 2
vot["prezenta_la_vot"] = vot["nr_voturi"] * 100 / vot["nr_alegatori"]
localitati = pd.read_excel("CoduriRomania.xlsx", index_col=0)
t2 = vot.merge(right=localitati, left_index=True, right_index=True)
t2_ = t2.sort_values(by="prezenta_la_vot", ascending=False)
t2_.index.name = "Cod Siruta"
t2_[["City", "prezenta_la_vot"]].to_csv("PrezentaVot.csv")

# Cerinta 3
t3 = t2.groupby(by="County").agg(sum)
t3[partide].to_csv("Judete.csv")

# Cerinta 4
t4 = t2[ ["City"] + partide ].\
    apply(func=f.vot_majoritar,axis=1)
t4.index.name="Cod Siruta"
# print(t4)
t4.to_csv("VotMajoritar.csv")

# Cerinta 5
nume_partid = "UDMR"
t5 = t4[ t4["Partid majoritar"]==nume_partid ]
# print(t5)
t5.to_csv(nume_partid+".csv")

