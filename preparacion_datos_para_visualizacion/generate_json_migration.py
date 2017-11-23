import json
import pandas as pd
import csv
import ast
from numpy import *

initial_year=2014
final_year=2016
for year in range(initial_year,final_year+1):
    input_membership="/home/lain/Redes-Sociales-con-Enfoque-Difuso/membership"+str(year)+".csv"
    input_data="../data/clean/"+str(year)+"_v4_migrantes.csv"
    output_data_final="../data/clean/to_json2/"+str(year)+"_v4_migrantes_to_process.csv"
    links_to_json="../data/clean/to_json2/"+str(year)+"_links_to_json.json"
    region_names=["Region Central", "Region Chorotega", "Region Pacifico Central", "Region Brunca", "Region Huetar Caribe", "Region Huetar Norte"]
    count_year=0
    last_index=0
    mf_dic = {'1.0': 'Mantiene familia con salario minimo', '0.75': 'Mantiene familia con salario medio bajo', '0.3': 'Mantiene familia con salario medio', '0.0':'No mantiene familia'}
    titulo_dic = {'1.0': 'No tiene educacion', '0.9': 'Educacion primaria', '0.7': 'Educacion Secundaria', '0.0': 'Educacion superior'}
    inp_dic = {'1.0': 'Salario bajo', '0.8': 'Salario medio bajo', '0.2': 'Salario medio', '0.0': 'Salario alto'}
    cl_dic = {'1.0': 'Desempleado', '0.0': 'Ocupado', '0.7': 'Retirado'}
    ocupacion_dic = { '0.0': 'No especificado',
                     '1.0': 'Directores y gerentes', '2.0': 'Profesionales cientificos e intelectuales', 
                     '3.0': 'Tecnicos y profesionales de nivel medio', '4.0': 'Personal de apoyo administrativo', 
                    '5.0': 'Servicios y vendedores de comercios y mercados',
                    '6.0':  'Agricultores, agropecuarios, forestales y pesqueros',
                    '7.0': 'Oficiales, operarios y artesanos',
                    '8.0': 'Operadores de instalaciones y maquinas y ensambladores',
                    '9.0': 'Ocupaciones elementales',
                    '10.0': 'No especificado',
                    '22.0': 'Desempleado sin experiencia'}

    df_data = pd.read_csv(input_data,index_col=False, header=0, usecols=['region_residencia', 'residencia_hace_dos_anos', 
                                                                          'condicion_laboral', 'ingreso_por_persona',
                                                                          'titulo', 'mantiene_familia', 'ocupacion_trabajo'])
    links = pd.DataFrame(df_data)

    #df = pd.crosstab(links['residencia_hace_dos_anos'], links['region_residencia'])
    df = pd.crosstab(links['region_residencia'], links['residencia_hace_dos_anos'])
    link_array = []
    for  column in df:
        for index, row in df.iterrows():
            if row[column] != 0:
                link_array.append({"source": region_names[int(index)-1], "target": region_names[column-1], "length":500, "width": row[column] })
                if index-1 >= last_index:
                    last_index = index-1


    df_memb = pd.read_csv(input_membership,index_col=False, header=0, usecols=["id","Clus 1","Clus 2","Clus 3","Clus 4"] )
    df_output = pd.concat([df_data, df_memb], axis=1)
    df_output.to_csv(output_data_final)
    columns = []
    rows = []

    to_process = pd.read_csv(output_data_final)
    
    df = pd.DataFrame(to_process)

    nodes = []
    seen = set(nodes)
    complete_file = []
    rows = []
    average = None
    clust_list = ['Clus 1','Clus 2','Clus 3','Clus 4']
    i=0
    average = df.groupby('region_residencia', as_index=False)[clust_list].mean()
    print(average)
    print("**")
    for  column in df:
        for index, row in average.iterrows():
            if str(region_names[int(row['region_residencia'])-1]) not in seen:
                seen.add( str(region_names[int(row['region_residencia'])-1]))
                list_percentage = [float(row["Clus 1"]),float(row["Clus 2"]),float(row["Clus 3"]),float(row["Clus 4"])]
                preferred_cluster = max(list_percentage)
                clust_num = [i for i, j in enumerate(list_percentage) if j == preferred_cluster]
                nodes.append({"id": str(region_names[int(row['region_residencia'])-1]), "preferredCluster": int(clust_num[0]), "type": "parent", 
                            "membership":[{"percent": row["Clus 1"]},{"percent": row["Clus 2"]},{"percent": row["Clus 3"]},
                            {"percent": row["Clus 4"]}]})


    for  column in df:
        for index, row in df.iterrows():
            if str(row["id"]) not in seen:
                seen.add(str(row["id"]))
                mantiene_familia = mf_dic[str(row['mantiene_familia'])]
                titulo = titulo_dic[str(row['titulo'])]
                ocupacion = ocupacion_dic[str(row['ocupacion_trabajo'])]
                condicion_laboral = cl_dic[str(row['condicion_laboral'])]
                json_line = {"id": str(row["id"]), "type": "individual", "membership":
                            [{"percent": row["Clus 1"]},{"percent": row["Clus 2"]},{"percent": row["Clus 3"]},
                            {"percent": row["Clus 4"]}],
                                'ingreso_por_persona':row['ingreso_por_persona'],'mantiene_familia': mantiene_familia,
                                'titulo': titulo,'ocupacion': ocupacion,
                                'condicion_laboral': condicion_laboral, 'regionDest': row['residencia_hace_dos_anos']}
                list_percentage = [float(row["Clus 1"]),float(row["Clus 2"]),float(row["Clus 3"]),float(row["Clus 4"])]
                preferred_cluster = max(list_percentage)
                clust_num = [i for i, j in enumerate(list_percentage) if j == preferred_cluster]
                parent_cluster = 0
                linkDistance = ""
                for node in nodes:
                    if str(region_names[int(row['region_residencia'])-1]) in node["id"]:
                        parent_cluster = int(node["preferredCluster"])

                if int(clust_num[0]) == parent_cluster:
                    linkDistance = "strong"
                else:
                    linkDistance = "low"

                nodes.append(json_line)
                link_array.append({"source": str(region_names[int(row['region_residencia'])-1]), 
                                    "target": str(row["id"]), "length":500, "width": 1,
                                     "linkDistance": linkDistance, "preferredCluster": int(clust_num[0])})


    complete_file.append({"nodes": nodes})
    complete_file.append({"links": link_array})

    with open(links_to_json, 'w') as outfile:
        json.dump(complete_file, outfile)


    count_year=count_year+1
