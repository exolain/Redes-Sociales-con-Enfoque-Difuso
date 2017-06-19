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

    bins = [0, 300000, 700000, 1500000, 3000000]
    group_names = ['Ingreso_Bajo', 'Ingreso_Medio_Bajo', 'Ingreso_Medio_Alto', 'Ingreso_Alto']
    ingreso_discreto = pd.cut(df_migrantes['itpn'], bins, labels=group_names)
    df_migrantes['ingreso_discreto'] = pd.cut(df_migrantes['itpn'], bins, labels=group_names)

    bins = [18, 24, 60, 100]
    group_names = ['joven_adulto', 'adulto', 'ciudadano_de_oro']
    ingreso_discreto = pd.cut(df_migrantes['A5'], bins, labels=group_names)
    df_migrantes['edad'] = pd.cut(df_migrantes['A5'], bins, labels=group_names)

    df_migrantes['titulo'] = np.where(df_migrantes['NivInst'] == 0, 'Sin_educacion', np.where(df_migrantes['NivInst'] < 7, 'Secundaria_completada', np.where(df_migrantes['NivInst'] < 9, 'Universidad_completada', 'Desconocido')))

    df_migrantes['condicion_laboral'] = np.where(df_migrantes['CondAct'] == 1, 'Ocupado', np.where(df_migrantes['CondAct'] == 2, 'Desempleado', np.where(df_migrantes['CondAct'] == 3, 'Retirado', 'Desconocido')))


    data_migrantes = df_migrantes.as_matrix(columns=['REGION','ZONA','edad','RegNac', 'RegResAnt','titulo','condicion_laboral','ingreso_discreto'])
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
    new_migrantes.columns =['region_residencia','zona','edad','region_nacimiento', 'residencia_hace_dos_anos','titulo','condicion_laboral', 'ingreso_por_persona']



    data2_migrantes = new_migrantes.sample(frac=0.2)

  
    new2_migrantes = pd.DataFrame(data2_migrantes)
#    data3_migrantes = new2_migrantes.dropna().to_csv("../data/clean/"+str(year)+"_v3_migrantes.csv")
    data3_migrantes = new2_migrantes.to_csv("../data/clean/"+str(year)+"_v3_migrantes.csv")


    #print data3
