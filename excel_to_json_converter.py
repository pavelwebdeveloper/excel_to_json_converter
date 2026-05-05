import pandas as pd
import json

# Loading the excel file
dataframe = pd.read_excel("Scoreboard Test.xlsx")

# Converting to JSON and writing to a file
#json_data = dataframe.to_json("result.json", orient="records", indent=2)
dataframe.to_json("result.json", orient="records", indent=2)

with open("result.json", "r") as f:
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

for x in range(0, 142):
    for data_set in json_data:
        if x == 0:
            continue
        elif (x != 0 and data_set[f"Unnamed: {x}"] == main_key):
            continue
        elif (x != 0 and data_set[f"Unnamed: {x}"] != main_key):
            print(new_json_data)
            new_json_data[main_key][sub_keys[index_for_sub_key]] = data_set[f"Unnamed: {x}"]
            index_for_sub_key += 1
            print("index_for_sub_key", index_for_sub_key)
            print("len(sub_keys)", len(sub_keys))
            print("main_key outside if statement", main_key)
            if index_for_sub_key == len(sub_keys):
                if json_data[0][f"Unnamed: {x+1}"] != None:
                    main_key = json_data[0][f"Unnamed: {x+1}"]
                    print("main_key inside if statement", main_key)
                    new_json_data[main_key] = {}
                    index_for_sub_key = 0 
                    with open("new_json_data.json", "w") as f:
                        json.dump(new_json_data, f, indent=2)
                elif json_data[0][f"Unnamed: {x+1}"] == None:
                    main_key = json_data[0][f"Unnamed: {x+2}"]
                    print("main_key inside if statement", main_key)
                    new_json_data[main_key] = {}
                    index_for_sub_key = 0
                    with open("new_json_data.json", "w") as f:
                        json.dump(new_json_data, f, indent=2)
                    continue
    

with open("new_json_data.json", "w") as f:
    json.dump(new_json_data, f, indent=2)


#{
#  "product1": { "name": "Milk", "price": 2.5 },
#  "product2": { "name": "Bread", "price": 1.8 }
#}
