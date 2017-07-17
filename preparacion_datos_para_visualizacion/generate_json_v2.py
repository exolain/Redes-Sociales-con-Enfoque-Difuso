import json
import pandas as pd
import csv
import ast
from numpy import *

input_data="/home/lain/movimientos.csv"
output_data_to_json="../data/clean/to_json2/movimientos_to_json.csv"
output_data_final="../data/clean/to_json2/movimientos_to_process.csv"
links_to_json="../data/clean/to_json2/movimientos_links_to_json.json"
region_names=["Region San Jose", "Region Puntarenas", "Region Limon", "Region Alajuela", "Region Heredia", "Region Guanacaste", "Region Cartago"]
count_year=0
last_index=0
link_array = []


df_memb = pd.read_csv(input_data,index_col=False, header=0, usecols=["id","San Jose","Alajuela","Heredia", "Limon", "Puntarenas", "Cartago", "Guanacaste", "Razon"] )
columns = []
rows = []

num_column=0
new_df = pd.DataFrame(df_memb)

len_columns = len(new_df.columns)
for  column in new_df:
    
    rows = []
    uniq_index=0
    for index, row in new_df.iterrows():
        if "id" in column:
            new_column2="nodes."+str(row["id"])+".id"
            columns.append(new_column2)
        elif "Razon" in column:
            new_column="nodes."+str(row["id"])+'.razon'
            columns.append(new_column)
        else:
            #cluster_number = int(filter(str.isdigit, str(column)))
            new_column="nodes."+str(row["id"])+".membership."+str(num_column)+".percent"
            columns.append(new_column)
        uniq_index = uniq_index + 1

    if column != "razon" and column != "id":        
        num_column = num_column + 1
        


with open(output_data_to_json, 'wb') as migration_graph:
    wr = csv.writer(migration_graph)
    wr.writerow(columns)


json_file = None
i = last_index
num_column=0
region_name = ""
element_id = ""
for column in new_df:
    for index, row in new_df.iterrows():
        
        if "id" in column:            
            #rows.append(row[column])
            element_id = "element_"+str(row["id"])
            rows.append(element_id)
    
        elif "razon" in column and  not row.empty:
            rows.append(row[column])
        else: 
            rows.append(row[column])
            region_name = region_names[num_column-1]
        
        if region_name and element_id and row[region_name.split(" ", 1)[1:][0]] != 0:
            json_file = {"source": region_name, "target": "element_"+str(row["id"]), "length":500, "width": 1}
            link_array.append(json_file)
            region_name=""
            #element_id=""
    i = i + 1
    if column != "razon" and column != "id":        
        num_column = num_column + 1


with open(links_to_json, 'w') as outfile:
    json.dump(link_array, outfile)

with open(output_data_to_json, 'a') as migration_graph:
    wr = csv.writer(migration_graph, delimiter=',')
    wr.writerow(rows)






