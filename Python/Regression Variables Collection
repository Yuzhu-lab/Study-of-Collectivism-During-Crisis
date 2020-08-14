
# Unstack the variables from imputation file and Coupleness file, create table of Time Series regression variables

import pandas as pd
DF1 = pd.read_csv("IncomeTableHousehold.csv")
DF1 = DF.set_index(DF["HHIDPN"])
DF1 = DF.drop(["HHIDPN"], axis=1)
DF1 = pd.DataFrame(DF.stack())
DF2 = pd.read_csv("coupleness_TS.csv")
DF2 = DF2.set_index(DF2["HHIDPN"])
DF2 = DF2.drop(["HHIDPN"], axis=1)
DF2 = pd.DataFrame(DF2.stack())
DF1 = pd.read_csv("IncomeTableHousehold0814.csv")
DF2 = pd.read_csv("Marriage0814.csv")
Res = pd.merge(DF1, DF2, on=['HHIDPN', 'Year'], how='inner')
Res.to_csv("TS_regression_variables.csv")
