import pandas as pd
import numpy as np
import plotly.express as px
import plotly.io as pio
pio.renderers.default="chrome"
from collections import Counter
import json
import kaleido


category =         pd.read_excel("templates/excel_data/master_file_discovery_final.xlsx",sheet_name="category_breakdown")
retailer_info =    pd.read_excel("templates/excel_data/master_file_discovery_final.xlsx",sheet_name="retailer_detail")
retailer_loc =     pd.read_excel("templates/excel_data/master_file_discovery_final.xlsx",sheet_name="retailer_location")
retailer_product = pd.read_excel("templates/excel_data/master_file_discovery_final.xlsx",sheet_name="retailers_product")
comp_df =          pd.read_excel("templates/excel_data/master_file_discovery_final.xlsx",sheet_name="competition")
logo =             pd.read_excel("templates/excel_data/master_file_discovery_final.xlsx",sheet_name="logo")
def category_list():
    cat_list = list(set(category["category"]))
    return cat_list

def sub_cat_list(cat):
    sub_cat=[]
    for x in cat:
        a=list(set(category[category["category"]==x]["sub_category"]))
        for z in a:
            sub_cat.append(z)
    return sub_cat

def product_type_list(sub_cat):
    pro_type=[]
    for x in sub_cat:
        a=list(set(category[category["sub_category"]==x]["product_type"]))
        for z in a:
            pro_type.append(z)
    return pro_type


def result_function(cat, sub_cat, pro_type):
    df_1 = retailer_product[retailer_product["category"].isin(cat)]
    df_2 = df_1[df_1["sub_category"].isin(sub_cat)]
    df_avail = df_2[df_2["product _type"].isin(pro_type)]
    len_pro_type = len(pro_type)

    # list of retailers
    list_of_retailers = (list(set(df_avail["retailer_name"])))
    # len of retailers
    number_of_retailers = len(list_of_retailers)

    # total number of outlet
    number_of_outlet = sum(list(retailer_info[retailer_info["name"].isin(list_of_retailers)]["total_number_of_outlet"]))

    # total number of states
    number_of_states = len(list(set(retailer_loc[retailer_loc["retailer"].isin(list_of_retailers)]["state"])))

    # number of city
    number_of_city = len(list(set(retailer_loc[retailer_loc["retailer"].isin(list_of_retailers)]["city"])))

    # create a dictionary
    result = {"retailer": number_of_retailers,
              "outlet": number_of_outlet,
              "state": number_of_states,
              "city": number_of_city,
              "len": len_pro_type}

    df_6 = retailer_info[retailer_info["name"].isin(list_of_retailers[:])]
    df_7 = df_6[["name", "total_number_of_outlet", "city_present", "state_present", "logo_location"]]
    top_8_retailer_list = list(df_7["name"])

    city = {}
    for i in top_8_retailer_list:
        x = list(set(retailer_loc[retailer_loc["retailer"] == i]["city"]))
        city[i] = x[0:5]

    top_8_df = pd.DataFrame({"name": list(city.keys()), "city": list(city.values())})

    empty_list = []
    for i in top_8_retailer_list:
        x = list(set(retailer_loc[retailer_loc["retailer"] == i]["state"]))
        empty_list.append(x[0:5])
        list_of_retailers = (list(set(df_avail["retailer_name"])))

    list_r1 = []
    list_product_found = []

    for retailer in list_of_retailers:

        selected_retailer_df = retailer_product[retailer_product["retailer_name"] == retailer]
        product_sold = list(selected_retailer_df["product _type"])

        product_found = 0

        for x in pro_type:
            if x in product_sold:
                product_found = product_found + 1
            else:
                pass

        list_r1.append(retailer)

        list_product_found.append(product_found)

    comp_df_1 = comp_df[comp_df["Retailer"].isin(list_of_retailers)]
    comp_df_2 = comp_df_1[comp_df_1["Category"].isin(cat)]
    comp_df_3 = comp_df_2[comp_df_2["Sub Category"].isin(sub_cat)]
    comp_df_4 = comp_df_3[["Retailer", "Match"]]

    comp_df_5 = comp_df_4.groupby("Retailer")
    comp_df_6 = comp_df_5.mean()
    comp_df_6.reset_index(inplace=True)

    comp_df_6.rename(columns={"Retailer": "name", "Match": "Match_percent"}, inplace=True)
    comp_df_6["Match_percent"] = comp_df_6["Match_percent"].astype(int)

    product_found_dict = {"name": list_r1, "product_matched": list_product_found}
    product_found_df = pd.DataFrame(product_found_dict)

    top_8_df["state"] = empty_list

    top_8_df["city"] = top_8_df["city"].apply(lambda x: str(x).strip("[]"))
    top_8_df["state"] = top_8_df["state"].apply(lambda x: str(x).strip("[]"))
    top_8_df["product_input"] = len_pro_type
    top_8_df = top_8_df.merge(product_found_df, on="name", how="left")
    top_8_df = top_8_df.merge(comp_df_6, on="name", how="left")

    top_8_info = top_8_df.merge(df_7, on="name", how="left")
    top_8_info = top_8_info.sort_values(by=["product_matched","Match_percent"],ascending=False)

    top_8_dict = top_8_info.to_dict("index")


    return result, top_8_dict

def bg_func(retailer_name):
    df_1=retailer_info[retailer_info["name"]==retailer_name]
    df_list=list(df_1["bg_location"])
    bg_dict={"bg_image":df_list[0]}
    return bg_dict

def extended_result_function(cat, sub_cat, pro_type,retailer_name ):
    df_1 = retailer_product[retailer_product["category"].isin(cat)]
    df_2 = df_1[df_1["sub_category"].isin(sub_cat)]
    df_avail = df_2[df_2["product _type"].isin(pro_type)]
    len_pro_type = len(pro_type)

    # list of retailers
    list_of_retailers = (list(set(df_avail["retailer_name"])))
    # len of retailers
    number_of_retailers = len(list_of_retailers)

    # total number of outlet
    number_of_outlet = sum(list(retailer_info[retailer_info["name"].isin(list_of_retailers)]["total_number_of_outlet"]))

    # total number of states
    number_of_states = len(list(set(retailer_loc[retailer_loc["retailer"].isin(list_of_retailers)]["state"])))

    # number of city
    number_of_city = len(list(set(retailer_loc[retailer_loc["retailer"].isin(list_of_retailers)]["city"])))

    # create a dictionary
    result = {"retailer": number_of_retailers,
              "outlet": number_of_outlet,
              "state": number_of_states,
              "city": number_of_city,
              "len": len_pro_type}

    df_6 = retailer_info[retailer_info["name"].isin(list_of_retailers[:])]
    df_7 = df_6[["name", "total_number_of_outlet", "city_present", "state_present", "logo_location"]]
    top_8_retailer_list = list(df_7["name"])

    city = {}
    for i in top_8_retailer_list:
        x = list(set(retailer_loc[retailer_loc["retailer"] == i]["city"]))
        city[i] = x[0:5]

    top_8_df = pd.DataFrame({"name": list(city.keys()), "city": list(city.values())})

    empty_list = []
    for i in top_8_retailer_list:
        x = list(set(retailer_loc[retailer_loc["retailer"] == i]["state"]))
        empty_list.append(x[0:5])
        list_of_retailers = (list(set(df_avail["retailer_name"])))

    list_r1 = []
    list_product_found = []

    for retailer in list_of_retailers:

        selected_retailer_df = retailer_product[retailer_product["retailer_name"] == retailer]
        product_sold = list(selected_retailer_df["product _type"])

        product_found = 0

        for x in pro_type:
            if x in product_sold:
                product_found = product_found + 1
            else:
                pass

        list_r1.append(retailer)

        list_product_found.append(product_found)

    comp_df_1 = comp_df[comp_df["Retailer"].isin(list_of_retailers)]
    comp_df_2 = comp_df_1[comp_df_1["Category"].isin(cat)]
    comp_df_3 = comp_df_2[comp_df_2["Sub Category"].isin(sub_cat)]
    comp_df_4 = comp_df_3[["Retailer", "Match"]]

    comp_df_5 = comp_df_4.groupby("Retailer")
    comp_df_6 = comp_df_5.mean()
    comp_df_6.reset_index(inplace=True)

    comp_df_6.rename(columns={"Retailer": "name", "Match": "Match_percent"}, inplace=True)
    comp_df_6["Match_percent"] = comp_df_6["Match_percent"].astype(int)

    product_found_dict = {"name": list_r1, "product_matched": list_product_found}
    product_found_df = pd.DataFrame(product_found_dict)

    top_8_df["state"] = empty_list

    top_8_df["city"] = top_8_df["city"].apply(lambda x: str(x).strip("[]"))
    top_8_df["state"] = top_8_df["state"].apply(lambda x: str(x).strip("[]"))
    top_8_df["product_input"] = len_pro_type
    top_8_df = top_8_df.merge(product_found_df, on="name", how="left")
    top_8_df = top_8_df.merge(comp_df_6, on="name", how="left")

    top_8_info = top_8_df.merge(df_7, on="name", how="left")
    top_8_info = top_8_info[top_8_info["name"]==retailer_name]

    user_input=list(top_8_info["product_input"])
    user_input=user_input[0]

    matching=list(top_8_info["product_matched"])
    matching=matching[0]

    exp_prob = list(top_8_info["Match_percent"])
    exp_prob = exp_prob[0]

    top_8_dict={"product_matched":matching,"product_input":user_input,"exp_prob":exp_prob}


    return result, top_8_dict


def comp_logo(retailer, cat_list, sub_cat_list):
    df_1 = comp_df[comp_df["Retailer"] == retailer]
    df_2 = df_1[df_1["Category"].isin(cat_list)]
    df_3 = df_2[df_2["Sub Category"].isin(sub_cat_list)]

    e1 = list(df_3["E1"])
    e2 = list(df_3["E2"])
    e3 = list(df_3["E3"])
    e4 = list(df_3["E4"])
    e5 = list(df_3["E5"])

    est_list = e1 + e2 + e3 + e4 + e5
    est_list = list(set(est_list))


    est_df = logo[logo["brand_name"].isin(est_list)]
    est_df = est_df.to_dict("index")

    l1 = list(df_3["L1"])
    l2 = list(df_3["L2"])
    l3 = list(df_3["L3"])

    low_list = l1 + l2 + l3
    low_list = list(set(low_list))

    low_df = logo[logo["brand_name"].isin(low_list)]
    low_df = low_df.to_dict("index")

    return est_df, low_df