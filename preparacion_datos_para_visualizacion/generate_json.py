import json
import pandas as pd
import csv
import ast
from numpy import *

initial_year=2014
final_year=2016
for year in range(initial_year,final_year+1):
    input_membership="/home/lain/Redes-Sociales-con-Enfoque-Difuso/membership"+str(year)+".csv"
    input_data="../data/clean/"+str(year)+"_v3_migrantes.csv"
    output_data_to_json="../data/clean/to_json/"+str(year)+"_v3_migrantes_to_process_to_json.csv"
    output_data_final="../data/clean/to_json/"+str(year)+"_v3_migrantes_to_process.csv"
    links_to_json="../data/clean/to_json/"+str(year)+"_links_to_json.json"
    region_names=["Region Central", "Region Chorotega", "Region Pacifico Central", "Region Brunca", "Region Huetar Caribe", "Region Huetar Norte"]
    count_year=0
    last_index=0
    df_data = pd.read_csv(input_data,index_col=False, header=0, usecols=['region_residencia', 'residencia_hace_dos_anos'])
    links = pd.DataFrame(df_data)

    df = pd.crosstab(links['residencia_hace_dos_anos'], links['region_residencia'])
    print df
    link_array = []
    for  column in df:
        for index, row in df.iterrows():
            if row[column] != 0:
                link_array.append({"source": region_names[int(index)-1], "target": region_names[column-1], "length":500, "width": row[column]})
                if index-1 >= last_index:
                    last_index = index-1


    df_memb = pd.read_csv(input_membership,index_col=False, header=0, usecols=["V1","V2","V3"] )
    df_output = pd.concat([df_data, df_memb], axis=1)
    df_output.to_csv(output_data_final)
    columns = []
    rows = []

    to_process = pd.read_csv(output_data_final)
    
    new_df = pd.DataFrame(to_process)

    len_columns = len(new_df.columns)
    for  column in new_df:
        
        rows = []
        uniq_index=0
        for index, row in new_df.iterrows():
            
            if "region" in column:
                new_column2="nodes.Y"+str(year)+"."+str(uniq_index)+".id"
                columns.append(new_column2)
                
            if "hace_dos" in column: 
                new_column="nodes.Y"+str(year)+"."+str(uniq_index)+'.regionDest'
                columns.append(new_column)

            if "V" in column and column:
                cluster_number = int(filter(str.isdigit, str(column)))
                new_column="nodes.Y"+str(year)+"."+str(uniq_index)+".membership."+str(cluster_number)+".percent"
                columns.append(new_column)
            
            
            uniq_index=uniq_index+1

    with open(output_data_to_json, 'wb') as migration_graph:
        wr = csv.writer(migration_graph)
        wr.writerow(columns)


    json_file = None
    i = last_index
    for column in new_df:
        for index, row in new_df.iterrows():
            
            if "region" in column and not row.empty:            
                #rows.append(row[column])
                element_id = "element_"+str(i)
                rows.append(element_id)
                region_name = region_names[(int(row[column]))-1]
                json_file = {"source": region_name, "target": element_id, "length":500, "width": 1}
                link_array.append(json_file)
                i = i + 1


            if "V" in column and not row.empty:
                rows.append(row[column])

            if "hace_dos" in column and  not row.empty:
                rows.append(row[column])


    with open(links_to_json, 'w') as outfile:
        json.dump(link_array, outfile)

    with open(output_data_to_json, 'a') as migration_graph:
        wr = csv.writer(migration_graph, delimiter=',')
        wr.writerow(rows)


    count_year=count_year+1





