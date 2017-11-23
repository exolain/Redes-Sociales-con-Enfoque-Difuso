import json
import pandas as pd
import numpy as np

for year in range(2016,2017):
    input_data="/home/lain/Redes-Sociales-con-Enfoque-Difuso/other_datasets/libraries_surveys/clean/to_json/"+str(year)+"_v5_libraries_to_json.csv"
    output_data_to_json="/home/lain/Redes-Sociales-con-Enfoque-Difuso/other_datasets/libraries_surveys/clean/to_json/"+str(year)+"_v5_libraries.json"
    nodes = []
    link_array = []

    df = pd.read_csv(input_data,index_col=False, header=0, usecols=['id','V1','V2','V3','V4','age_group','marital','par','usr', 'estado'])

    usr_dic = {'S': "suburbano", 'R': "rural", 'U': 'urbano'}
    marital_dic = {1:'Casado', 2:'Union libre', 3:'Divorciado', 4:'Separado', 5:'Viudo', 6:'Soltero', 8:'Soltero', 9:'Soltero'}
    parental_dic = {1:'Padre', 2: 'No tiene hijos'}
   # df["V1"] = np.where(df['V1'] <= 0.10, 0, np.where(df['V1'] >= 0.90, 1, df['V1']))
   # df["V2"] = np.where(df['V2'] <= 0.10, 0, np.where(df['V2'] >= 0.90, 1, df['V2']))
   # df["V3"] = np.where(df['V3'] <= 0.10, 0, np.where(df['V3'] >= 0.90, 1, df['V3']))
   # df["V4"] = np.where(df['V4'] <= 0.10, 0, np.where(df['V4'] >= 0.90, 1, df['V4']))

    nodes = []
    seen = set(nodes)
    complete_file = []
    link_array = []
    rows = []
    for  column in df:
        for index, row in df.iterrows():
            if str(row["id"]) not in seen:
                seen.add(str(row["id"]))
                marital_status = marital_dic[int(row['marital'])]
                parent_status = parental_dic[int(row['par'])]
                json_line = {"id": str(row["id"]), "type": "individual", "membership":[{"percent": row["V1"]},{"percent": row["V2"]},{"percent": row["V3"]},{"percent": row["V4"]}],
                                'age':str(row["age_group"]),'marital_status': marital_status,
                                'parent': parent_status,'region': usr_dic[str(row['usr'])],
                                'state': str(row['estado'])}
                nodes.append(json_line)
                link_array.append({"source": str(row["estado"]), "target": str(row["id"]), "length":500, "width": 1})

                

    complete_file.append({"nodes": nodes})
    complete_file.append({"links": link_array})

    with open(output_data_to_json, 'a') as outfile:
        json.dump(complete_file, outfile)