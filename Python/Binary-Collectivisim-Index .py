from load_data import * 
import numpy as np
import math

# Create Hashmaps for data and identified char for each yr in HRS
keys = [x for x in range(2000,2018,2)]
values =["G","H"] + [chr(y) for y in range(74,83)]
data_all = [data_00, data_02, data_04, data_06, data_08, data_10, data_12, data_14, data_16]
year_match_char = dict(zip(keys, values))
year_match_data = dict(zip(keys, data_all))

# Set ID of each participant as index of df
for x in year_match_data:
    if x == 2000:
        year_match_data[x]["Age"] = 2000 - year_match_data[x]["G1053A"]
    else:
        c = year_match_char[x]
        year_match_data[x]["Age"] = year_match_data[x][c + "A019"] 
    year_match_data[x] = year_match_data[x].set_index("HHIDPN")

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
    
# age can be 50 56 62 68
def get_li_index(yr):
    df = year_match_data[yr]
    c = year_match_char[yr]
    if c == "G":
        #Overall and base variables
        df["Ghelp"] = df["G2999"].apply(lambda x: 1 if x > 0 else 0)
        coll1 = df[[c + "3146",c+"2048",c + "2480",c + "2484", c+"2251", c+"2298", c+"2281", c+"3002", c+"2107", c+"2079", c+"2488",\
                    c+"help"]].copy()
        coll0 = df[[c + "1930", c+"886"]].copy()
        coll2 = coll1.applymap(change_to_01)
        coll0["give housing"] = coll0[c+"1930"] - coll0[c+"886"]
        # Giving
        coll_give = df[[c + "2048",c+"2480", c+"2251", c+"2281", c+"2079", "Ghelp" ]].copy().applymap(change_to_01)
        coll_give["give housing"] = coll0["give housing"].apply(lambda x: 1 if x > 0 else 0)
        # Receiving
        coll_receive = df[[c+"3146",c+"2484", c+"2298", c+"3002", c+"2107", c+"2488"]].copy().applymap(change_to_01)
        
    elif c!= "H" and c != "G":
        coll1 = df[[c+"E060",c+"H088", c+"E105", c+"E111",c+"F104", c+"F152",c+"F139",c+"G097",c+"E087",c+"E075",c+"E117",c+"G198"]].copy()
        coll0 = df[[c + "A098", c+"A099"]].copy()
        coll2 = coll1.applymap(change_to_01)
        coll0["give housing"] = coll0[c+"A098"] - coll0[c+"A099"]
        #Giving
        coll_give = df[[c+"E060", c+"E105", c+"F104", c+"F139", c+"E075",c+"G198" ]].copy().applymap(change_to_01)
        coll_give["give housing"] = coll0["give housing"].apply(lambda x: 1 if x > 0 else 0)
        #Receiving
        coll_receive = df[[c+"H088",c+"E111", c+"F152", c+"G097", c+"E087", c+"E117"]].copy().applymap(change_to_01)
        
    elif c == "H":
        coll1 = df[[c+"E060",c+"H088", c+"E105", c+"E111",c+"F104", c+"F152",c+"F139",c+"G097",c+"E087",c+"E075",c+"E117",c+"G092"]].copy()
        coll0 = df[[c + "A098", c+"A099"]].copy()
        coll2 = coll1.applymap(change_to_01)
        coll0["give housing"] = coll0[c+"A098"] - coll0[c+"A099"]
        #Giving
        coll_give = df[[c+"E060", c+"E105", c+"F104", c+"F139", c+"E075",c+"G092" ]].copy().applymap(change_to_01)
        coll_give["give housing"] = coll0["give housing"].apply(lambda x: 1 if x > 0 else 0)
        #Receiving
        coll_receive = df[[c+"H088",c+"E111", c+"F152", c+"G097", c+"E087", c+"E117"]].copy().applymap(change_to_01)
        
    coll2["give housing"] = coll0["give housing"].apply(lambda x: 1 if x > 0 else 0)
    df["Overall Index"] = coll2.sum(axis = 1)
    df["Give Index"] = coll_give.sum(axis = 1)
    df["Receive Index"] = coll_receive.sum(axis = 1)
    return df[["Overall Index","Give Index", "Receive Index", "Age"]]
    
for x in range(2000, 2018,2):
   get_li_index(x).to_csv(path_or_buf = ("Binary Coll Index Table "+str(x)+".csv"))
    
