import json
import pandas as pd

for year in range(2015,2017):
    input_data="/home/lain/Redes-Sociales-con-Enfoque-Difuso/other_datasets/libraries_surveys/clean/to_json/"+str(year)+"_v5_libraries_to_json.csv"
    output_data_to_json="/home/lain/Redes-Sociales-con-Enfoque-Difuso/other_datasets/libraries_surveys/clean/to_json/"+str(year)+"_v5_libraries.json"
    nodes = []
    link_array = []

    df = pd.read_csv(input_data,index_col=False, header=0, usecols=['id','Clus 1','Clus 2','Clus 3','Clus 4','Clus 5','Clus 6','age','marital','par','usr', 'state'])
    bins = [18, 25, 30, 45, 60, 90]
    group_names = ['joven', 'joven_adulto', 'adulto', 'mediana_edad','ciudadano_de_oro']
    edad_discreta = pd.cut(df['age'], bins, labels=group_names)
    df['age_group'] = pd.cut(df['age'], bins, labels=group_names)

    usr_dic = {'S': "suburbano", 'R': "rural", 'U': 'urbano'}
    marital_dic = {1:'Casado', 2:'Union libre', 3:'Divorciado', 4:'Separado', 5:'Viudo', 6:'Soltero', 8:'Soltero', 9:'Soltero'}
    parental_dic = {1:'Padre', 2: 'No tiene hijos'}
    states = {1:'Alabama', 2:'Alaska', 4:'Arizona', 5:'Arkansas',6:'California', 8:'Colorado', 9:'Connecticut',10:'Delaware', 11:'DistrictofColumbia',
              12:'Florida', 13:'Georgia', 15:'Hawaii', 16:'Idaho',17:'Illinois', 18:'Indiana', 19:'Iowa', 20:'Kansas', 21:'Kentucky', 22:'Louisiana', 
              23:'Maine', 24:'Maryland', 25:'Massachusetts', 26:'Michigan', 27:'Minnesota', 28:'Mississippi', 29:'Missouri', 30:'Montana', 31:'Nebraska', 
              32:'Nevada', 33:'NewHampshire', 34:'NewJersey', 35:'NewMexico', 36:'NewYork', 37:'NorthCarolina', 38:'NorthDakota', 39:'Ohio',
              40:'Oklahoma', 41:'Oregon', 42:'Pennsylvania', 44:'RhodeIsland', 45:'SouthCarolina', 46:'SouthDakota', 47:'Tennessee', 48:'Texas',
              49:'Utah', 50:'Vermont', 51:'Virginia', 53:'Washington', 54:'WestVirginia', 55:'Wisconsin', 56:'Wyoming'}
    nodes = []
    seen = set(nodes)
    complete_file = []
    link_array = []
    rows = []
    average = None
    clust_list = ['Clus 1','Clus 2','Clus 3','Clus 4','Clus 5','Clus 6']
    i=0
    nodes.append({"id":"United States"})
    average = df.groupby('state', as_index=False)[clust_list].mean()

    for  column in df:
        for index, row in average.iterrows():
            list_percentage = [float(row["Clus 1"]),float(row["Clus 2"]),float(row["Clus 3"]),float(row["Clus 4"]),float(row["Clus 5"]),float(row["Clus 6"])]
            preferred_cluster = max(list_percentage)
            clust_num = [i for i, j in enumerate(list_percentage) if j == preferred_cluster]
            nodes.append({"id": states[int(row['state'])], "preferredCluster": int(clust_num[0]), "type": "parent", 
            "membership":[{"percent": row["Clus 1"]},{"percent": row["Clus 2"]},{"percent": row["Clus 3"]},
            {"percent": row["Clus 4"]},{"percent": row["Clus 5"]},{"percent": row["Clus 6"]}]})
            link_array.append({"source":"United States","target":states[int(row['state'])],"length":500,"width":1})
        
            #percent_dictionary[value][clust] = average


    for  column in df:
        for index, row in df.iterrows():
            if str(row["id"]) not in seen:
                seen.add(str(row["id"]))
                marital_status = marital_dic[int(row['marital'])]
                parent_status = parental_dic[int(row['par'])]
                estado = states[int(row['state'])]
                json_line = {"id": str(row["id"]), "type": "individual", "membership":
                            [{"percent": row["Clus 1"]},{"percent": row["Clus 2"]},{"percent": row["Clus 3"]},
                            {"percent": row["Clus 4"]},{"percent": row["Clus 5"]},{"percent": row["Clus 6"]}],
                                'age':str(row["age_group"]),'marital_status': marital_status,
                                'parent': parent_status,'region': usr_dic[str(row['usr'])],
                                'state': str(estado)}
                list_percentage = [float(row["Clus 1"]),float(row["Clus 2"]),float(row["Clus 3"]),float(row["Clus 4"]),float(row["Clus 5"]),float(row["Clus 6"])]
                preferred_cluster = max(list_percentage)
                clust_num = [i for i, j in enumerate(list_percentage) if j == preferred_cluster]
                parent_cluster = 0
                linkDistance = ""
                for node in nodes:
                    if estado in node["id"]:
                        parent_cluster = int(node["preferredCluster"])

                if int(clust_num[0]) == parent_cluster:
                    linkDistance = "strong"
                else:
                    linkDistance = "low"

                nodes.append(json_line)
                link_array.append({"source": str(estado), "target": str(row["id"]), "length":500, "width": 1, "linkDistance": linkDistance, "preferredCluster": int(clust_num[0])})

                

    complete_file.append({"nodes": nodes})
    complete_file.append({"links": link_array})

    with open(output_data_to_json, 'a') as outfile:
        json.dump(complete_file, outfile)