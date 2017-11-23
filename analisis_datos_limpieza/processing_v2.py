import pandas as pd
import numpy as np
#import savReaderWriter as spss


#class Preprocess():

for year in range(2014,2017):

    df = pd.read_excel('../data/raw/ENAHO'+str(year)+'.xlsx')
    #data4 = df[df["CondMig"]==1]
    migrantes = df[((df["REGION"]!=df["RegResAnt"]) ) & (df["RegResAnt"]<7) & (df['A5']>17)  ]
    
    # Assuming same lines from your example
    

    df_migrantes = pd.DataFrame(migrantes)

    df_migrantes['itpn'] = np.where(pd.isnull(df_migrantes['itpn']) & (df_migrantes['CondAct'] == 2), 0, df_migrantes['itpn'])
    bins = [0, 199999, 700000, 1500000, 3000000]
    #group_names = ['Ingreso_Bajo', 'Ingreso_Medio_Bajo', 'Ingreso_Medio_Alto', 'Ingreso_Alto']
    group_names = [1,0.8, 0.2, 0]
    ingreso_discreto = pd.cut(df_migrantes['itpn'], bins, labels=group_names)
    df_migrantes['ingreso_discreto'] = pd.cut(df_migrantes['itpn'], bins, labels=group_names)

    bins = [18, 25, 30, 40, 50, 60, 70, 80, 90]
    group_names = ['18 - 25', '26 - 30', '31 - 40', '41 - 50', '51 - 60', '61 - 70', '71 - 80', '81 - 90']
    edad_discreta = pd.cut(df_migrantes['A5'], bins, labels=group_names)
    df_migrantes['edad'] = pd.cut(df_migrantes['A5'], bins, labels=group_names)
    #df_migrantes['titulo'] = np.where(df_migrantes['NivInst'] == 0, 'Sin_educacion', np.where(df_migrantes['NivInst'] < 7, 'Secundaria_completada', np.where(df_migrantes['NivInst'] < 9, 'Universidad_completada', 'Desconocido')))
    df_migrantes['titulo'] = np.where(df_migrantes['NivInst'] == 0, 1, np.where(df_migrantes['NivInst'] < 0.9, 3, np.where(df_migrantes['NivInst'] < 7, 0.7, np.where(df_migrantes['NivInst'] < 9, 0, 0))))


    #df_migrantes['condicion_laboral'] = np.where(df_migrantes['CondAct'] == 1, 'Ocupado', np.where(df_migrantes['CondAct'] == 2, 'Desempleado', np.where(df_migrantes['CondAct'] == 3, 'Retirado', 'Desconocido')))
    df_migrantes['condicion_laboral'] = np.where(df_migrantes['CondAct'] == 1, 0, np.where(df_migrantes['CondAct'] == 2, 1, np.where((df_migrantes['CondAct'] == 3) & (df_migrantes['A5']>60), 0.7, 0)))

    df_migrantes['calidad_vivienda'] = np.where(df_migrantes['CalViv'] == 1, 0, np.where(df_migrantes['CalViv'] == 2, 0.9, np.where(df_migrantes['CondAct'] == 3, 0.3, 0)))
  
    df_migrantes['mantiene_familia'] = np.where( (df_migrantes['A23'] == 1) & (df_migrantes['itpn'] < 200000), 1, np.where((df_migrantes['A23'] == 1) & (df_migrantes['itpn'] > 199999) & (df_migrantes['itpn'] < 500000), 0.75, np.where((df_migrantes['A23'] == 0) & (df_migrantes['itpn'] < 250000), 0.6,  np.where((df_migrantes['A23'] == 1) & (df_migrantes['itpn'] > 499999) & (df_migrantes['itpn'] < 800000 ), 0.3, 0))))
    
    data_migrantes = df_migrantes.as_matrix(columns=['REGION','ZONA','edad','RegNac', 'RegResAnt','titulo','condicion_laboral','ingreso_discreto', 'A4', 'A6', 'OcupFuerzaTrab', 'mantiene_familia', 'calidad_vivienda'])
    """
    REGION = Region socioeconomica donde reside
    Zona = 1 = Urbana, 2 = Urbana
    A5 = Edad
    RegNac = Region de Nacimiento(1 = Region Central,2 = Region Chorotega, 3 = Region Pacifico Central,4 = Region Brunca,5 = Region Huetar Caribe,6 = Region Huetar Norte,7 = En otro pais,9 = Ignorado)
    RegResAnt = Region de residencia hace dos anios
    A16B = Titulo (0=No tiene titulo,1=Tecnico, perito no universitario,2=Profesorado, tecnico o diplomado universitario,3=Bachillerato,4=Licenciatura,5=Especializacion,6=Maestria, Doctorado, 9 = Ignorado
    CondAct = Condicion de Actividad (1=ocupado, 2=desempleado, 3=Fuera de la fuerza de trabajo)
    ithn = Ingreso total por hogar neto
    np = Nivel de pobreza (1=Pobreza extrema,2=Pobreza no extrama, 3=No pobre
    """

    new_migrantes = pd.DataFrame(data_migrantes)
    new_migrantes.columns =['region_residencia','zona','edad','region_nacimiento', 'residencia_hace_dos_anos','titulo','condicion_laboral', 'ingreso_por_persona', 'sexo', 'estado_conyugal', 'ocupacion_trabajo', 'mantiene_familia', 'calidad_vivienda']

    new_migrantes['ocupacion_trabajo'].fillna(0, inplace=True)
 #   data2_migrantes = new_migrantes.sample(frac=0.2)

  
    new2_migrantes = pd.DataFrame(new_migrantes)
    data3_migrantes = new2_migrantes.dropna().to_csv("../data/clean/"+str(year)+"_v4_migrantes.csv")
 
