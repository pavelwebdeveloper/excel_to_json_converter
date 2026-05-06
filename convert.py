import pandas as pd
import json

# Loading the excel file
dataframe = pd.read_excel("Scoreboard Test.xlsx")

# Converting to JSON and writing to a file
dataframe.to_json("raw_data.json", orient="records", indent=2)

with open("raw_data.json", "r") as f:
    json_data = json.load(f)

new_json_data = {}

main_key = ""
sub_keys = []
index_for_sub_key = 0

for data_set in json_data:
    if data_set["Unnamed: 0"] == "\\ ":
        main_key = data_set["Unnamed: 1"]
        new_json_data[main_key] = {}
    elif data_set["Unnamed: 0"] != "\\ ":
        sub_keys.append(data_set["Unnamed: 0"])
        
skip_to_next = False

for x in range(0, 141):
    key = f"Unnamed: {x}" if x != 35 else "PHONE PERFORMANCE"
    if not(skip_to_next):
        for data_set in json_data:
            if x == 0:
                continue
            elif (x != 0 and data_set[key] == main_key):
                continue
            elif (x != 0 and data_set[key] != main_key):
                if x != 35:
                    new_json_data[main_key][sub_keys[index_for_sub_key]] = data_set[f"Unnamed: {x}"]
                else:
                    new_json_data[main_key][sub_keys[index_for_sub_key]] = data_set["PHONE PERFORMANCE"]
                index_for_sub_key += 1
                if index_for_sub_key == len(sub_keys):
                    if json_data[0][f"Unnamed: {x+1}"] != None:
                        main_key = json_data[0][f"Unnamed: {x+1}"]
                        new_json_data[main_key] = {}
                        index_for_sub_key = 0 
                    elif json_data[0][f"Unnamed: {x+1}"] == None:
                        if x != 33:
                            main_key = json_data[0][f"Unnamed: {x+2}"]
                            if json_data[0][f"Unnamed: {x+2}"] == None:
                                main_key = json_data[0][f"Unnamed: {x+3}"]
                        else:
                            main_key = json_data[0]["PHONE PERFORMANCE"]
                        new_json_data[main_key] = {}
                        index_for_sub_key = 0
                        skip_to_next = True
    else:
        skip_to_next = False
        continue
    

with open("output.json", "w") as f:
    json.dump(new_json_data, f, indent=2)
