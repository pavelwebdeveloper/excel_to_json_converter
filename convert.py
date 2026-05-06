import pandas as pd
import json

# function to convert time from timesatmp to yyyy-mm-dd format
def convertTimeStampToUserFriendlyType(time_stamp):
    return pd.to_datetime(time_stamp, unit='ms').strftime("%Y-%m-%d")
    
# function to add $ and % signs to the corresponding values
def defineValue(data_item, main_key):
    money = ["Total Revenue", "Total Payments", "AR > 90 days", "Total AR", "PT Total Revenue", "RMT Total Revenue", "CHIRO Total Revenue", "Pelvic Health"]
    percentage = ["Revenue Collected (4 wk avg)", "Cancelled Ax Online %", "Cancellation %", "Answer Rate", "Booking Rate", "NAR % Collected at Ax", "Booked:Prescribed %", "% Tx Plan Used", "% of Total Ax (AHS)", "Utilization"]
    if any(word in main_key for word in money):
        return "$ " + str(data_item)
    elif any(word in main_key for word in percentage) and data_item != None:
        return str(int(data_item * 100)) + " %" 
    else:
        return data_item
        

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

# the initial setup of the new json
for data_set in json_data:
    if data_set["Unnamed: 0"] == "\\ ":
        main_key = data_set["Unnamed: 1"]
        new_json_data[main_key] = {}
    elif data_set["Unnamed: 0"] != "\\ ":
        sub_keys.append(data_set["Unnamed: 0"])

times_to_skip = 0

sub_keys[3] = str("...+")

for x in range(0, 141):
    key = f"Unnamed: {x}" if x != 35 else "PHONE PERFORMANCE"
    if times_to_skip == 0:
        for data_set in json_data:
            if x == 0:
                continue
            elif (x != 0 and data_set[key] == main_key):
                continue
            elif (x != 0 and data_set[key] != main_key):
                if x != 35:
                    sub_key = convertTimeStampToUserFriendlyType(sub_keys[index_for_sub_key]) if (type(sub_keys[index_for_sub_key]) == int and sub_keys[index_for_sub_key] > 100000000000) else sub_keys[index_for_sub_key]
                    if (sub_key != "Focus:" and sub_key != "Source:" and sub_key != "Role:" and sub_key != "...+" and sub_key != 6):
                        new_json_data[main_key][sub_key] = defineValue(data_set[f"Unnamed: {x}"], main_key)
                    else:
                        if main_key == "Total Calls (5530)":
                            break
                        new_json_data[main_key][sub_key] = data_set[f"Unnamed: {x}"]
                else:
                    new_json_data[main_key][sub_keys[index_for_sub_key]] = data_set["PHONE PERFORMANCE"]
                index_for_sub_key += 1
                # reseting to create the next json object item
                if index_for_sub_key == len(sub_keys):
                    if x == 33 or x == 34:
                        main_key = json_data[0]["PHONE PERFORMANCE"]
                    else:
                        if json_data[0][f"Unnamed: {x+1}"] != None:
                            main_key = json_data[0][f"Unnamed: {x+1}"] 
                        elif json_data[0][f"Unnamed: {x+1}"] == None:
                            main_key = json_data[0][f"Unnamed: {x+2}"]
                            times_to_skip += 1
                            if json_data[0][f"Unnamed: {x+2}"] == None:
                                main_key = json_data[0][f"Unnamed: {x+3}"]
                                times_to_skip += 1
                    new_json_data[main_key] = {}
                    index_for_sub_key = 0
    else:
        times_to_skip -= 1
        continue
    

with open("output.json", "w") as f:
    json.dump(new_json_data, f, indent=2)
    
    

