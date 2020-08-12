from load_data import * 
import numpy as np
import math

# Hashmap for matching
keys = [x for x in range(2000,2018,2)]
values =["G","H"] + [chr(y) for y in range(74,83)]
data_all = [data_00, data_02, data_04, data_06, data_08, data_10, data_12, data_14, data_16]
year_match_char = dict(zip(keys, values))
year_match_data = dict(zip(keys, data_all))

# Set thresholds
def change_to_01(x):
    if x == 1.0:
        return 1
    elif x == 5.0:
        return 0.0
    elif x == 8.0:
        return 0.0
    elif x == 9.0:
        return 0.0
    else:
        return 0.0
    
def set_threshold(df, var = "G2050"):
    result = list(data_00[var].apply(lambda x: x if  x<= 9995 else None).dropna().quantile([0.25,0.5,0.75]))
    if var == "G2481" or var == "G2485"or var == "G2254_1" or var == "G2301_1":
        result = list(data_00[var].apply(lambda x: x if  x<= 999990 else None).dropna().quantile([0.25,0.5, 0.75]))
    return result

#G2050
thresh_grandkid_care = set_threshold(data_00, var = "G2050")
# G2481
thresh_G_F_Friend = set_threshold(data_00, var = "G2481")
# G2485
thresh_R_F_Friend = set_threshold(data_00, var = "G2485")
# G2254_1
thresh_G_F_Parent = set_threshold(data_00, var = "G2254_1")
# G2301_1
thresh_R_F_Parent = set_threshold(data_00, var = "G2301_1")
# G2284_1
thresh_errand = set_threshold(data_00, var = "G2284_1")

def allocation_care(x):
    thresh = thresh_grandkid_care
    if x < thresh[0] or math.isnan(x):
        return 0
    elif x >thresh[0] and x<thresh[1]:
        return 1
    elif x > thresh[1] and x < thresh[2]:
        return 2
    elif x >thresh[2]:
        return 3
def allocation_GMF(x):
    thresh = thresh_G_F_Friend
    if x < thresh[0] or math.isnan(x):
        return 0
    elif x >thresh[0] and x<thresh[1]:
        return 1
    elif x > thresh[1] and x < thresh[2]:
        return 2
    elif x >thresh[2]:
        return 3
def allocation_RMF(x):
    thresh = thresh_R_F_Friend
    if x < thresh[0] or math.isnan(x):
        return 0
    elif x >thresh[0] and x<thresh[1]:
        return 1
    elif x > thresh[1] and x < thresh[2]:
        return 2
    elif x >thresh[2]:
        return 3
def allocation_GMP(x):
    thresh = thresh_G_F_Parent
    if x < thresh[0] or math.isnan(x):
        return 0
    elif x >thresh[0] and x<thresh[1]:
        return 1
    elif x > thresh[1] and x < thresh[2]:
        return 2
    elif x >thresh[2]:
        return 3
def allocation_RMP(x):
    thresh = thresh_R_F_Parent
    if x < thresh[0] or math.isnan(x):
        return 0
    elif x >thresh[0] and x<thresh[1]:
        return 1
    elif x > thresh[1] and x < thresh[2]:
        return 2
    elif x >thresh[2]:
        return 3
def allocation_errand(x):
    thresh = thresh_errand
    if x < thresh[0] or math.isnan(x):
        return 0
    elif x >thresh[0] and x<thresh[1]:
        return 1
    elif x > thresh[1] and x < thresh[2]:
        return 2
    elif x >thresh[2]:
        return 3
# age can be 50 56 62 68
def get_numerical_index (year):
    c = year_match_char[year]
    df = year_match_data[year]
    
    def spend_time(x):
        if not x:
            return 0
        elif x <= 100:
            return 1
        elif x<=200:
            return 2
        elif x >200:
            return 3
        
    if c == "G":
        coll_receive = df[[c+"3002", c+"2107", c+"2488", c+"3146"]].copy().applymap(change_to_01)
        coll_give = df[["G2079"]].copy().applymap(change_to_01)
        
        coll0 = df[[c + "1930", c+"1932"]].copy()
        coll_give["give housing"] = (coll0[c+"1930"] - coll0[c+"1932"]).dropna().apply(lambda x : x if x >= 0 else (3 if x>=3 else 0))/3
        
        #2 Spent time helping friends & relatives
        coll_give["Spend time help friend"] =  df[[c+"2999"]].copy().applymap(spend_time)/3
        
        # Care for Grandkid
        coll_give["care for grandkid"] = df[[c+"2050"]].copy().applymap(allocation_care)/3
        
        # give Financial Help
        coll_give["financial help to friend"] = df[[c+"2481"]].copy().applymap(allocation_GMF)/3
    
        # receive Financial Help
        coll_receive["financial help from friend"] = df[[c+"2485"]].copy().applymap(allocation_RMF)/3
        
        # give financial to parents
        coll_give["financial help to parent"] = df[[c+"2254_1"]].copy().applymap(allocation_GMP)/3

        # give financial from parents
        coll_give["financial help from parent"] = df[[c+"2301_1"]].copy().applymap(allocation_RMP)/3

        # errand
        coll_give["errand"] = df[[c+"2284_1"]].copy().applymap(allocation_errand)/3
        
    if c!= "H" and c!="G":
        coll_receive = df[[c+"G097", c+ "E087", c+"E117", c+"H088"]].copy().applymap(change_to_01)
        coll_give = df[[ c+"E075"]].copy().applymap(change_to_01)
        
        coll0 = df[[c + "A098", c+"A099"]].copy()
        coll_give["give housing"] = (coll0[c+"A098"] - coll0[c+"A099"]).apply(lambda x : x if x >= 0 else None).dropna()
        coll_give["give housing"] = coll_give["give housing"].apply(lambda x : x if x <=3 else 3)/3
        coll_helpfriend = df[[c+"G199", c+"G200"]].copy()
        coll_helpfriend[c+"G199"] = coll_helpfriend[c+"G199"].map(lambda x: x if (x in [1,3,5]) else 0)
        coll_helpfriend[c+"G200"] = coll_helpfriend[c+"G200"].map(lambda x: 2 * x if (x in [1,3,5]) else 0)
        coll_helpfriend["sum_helpfriend"] = coll_helpfriend.sum(axis = 1).dropna()
        coll_give["sum_helpfriend"] = coll_helpfriend["sum_helpfriend"].map(lambda x:0 \
                                                                                   if (x<6 or not x) else(1 \
                                                                                                          if x<8 else (2 if x<10 else 3)))/3
        # Care for Grandkid
        coll_give["care for grandkid"] = df[[c+"E068"]].copy().applymap(allocation_care)/3

        # give Financial Help
        coll_give["financial help to friend"] = df[[c+"E106"]].copy().applymap(allocation_GMF)/3

        # receive Financial Help
        coll_receive["financial help from friend"] = df[[c+"E112"]].copy().applymap(allocation_RMF)/3

        # give financial to parents
        coll_give["financial help to parent"] = df[[c+"F107_1"]].copy().applymap(allocation_GMP)/3

        # give financial from parents
        coll_give["financial help from parent"] = df[[c+"F154_1"]].copy().applymap(allocation_RMP)/3

        # errand
        coll_give["errand"] = df[[c+"F142_1"]].copy().applymap(allocation_errand)/3   
        
    if c == "H":
        coll_receive = df[[c+"G097", c+ "E087", c+"E117", c+"H088"]].copy().applymap(change_to_01)
        coll_give = df[[ c+"E075"]].copy().applymap(change_to_01)
        
        coll0 = df[[c + "A098", c+"A099"]].copy()
        coll_give["give housing"] = (coll0[c+"A098"] - coll0[c+"A099"]).apply(lambda x : x if x >= 0 else None).dropna()
        coll_give["give housing"] = coll_give["give housing"].apply(lambda x : x if x <=3 else 3)/3
        coll_helpfriend = df[[c+"G092"]].copy()
        coll_give["sum_helpfriend"] = coll_helpfriend.applymap(spend_time)/3

        # Care for Grandkid
        coll_give["care for grandkid"] = df[[c+"E068"]].copy().applymap(allocation_care)/3

        # give Financial Help
        coll_give["financial help to friend"] = df[[c+"E106"]].copy().applymap(allocation_GMF)/3

        # receive Financial Help
        coll_receive["financial help from friend"] = df[[c+"E112"]].copy().applymap(allocation_RMF)/3

        # give financial to parents
        coll_give["financial help to parent"] = df[[c+"F107_1"]].copy().applymap(allocation_GMP)/3

        # give financial from parents
        coll_give["financial help from parent"] = df[[c+"F154_1"]].copy().applymap(allocation_RMP)/3

        # errand
        coll_give["errand"] = df[[c+"F142_1"]].copy().applymap(allocation_errand)/3
    
    df["Overall Index"] = coll_give.sum(axis = 1)+coll_receive.sum(axis = 1)
    df["Give Index"] = coll_give.sum(axis = 1)
    df["Receive Index"] = coll_receive.sum(axis = 1)
    
    return df[["HHIDPN","Overall Index","Give Index", "Receive Index"]]
    
for x in range(2000, 2018,2):
    get_numerical_index(x).to_csv(path_or_buf = ("Numeric Coll Index Table "+str(x)+".csv"))
