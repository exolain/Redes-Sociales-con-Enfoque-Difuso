import pandas as pd
import numpy as np
import savReaderWriter as spss


#class Preprocess():

for year in range(2014,2017):

    df = pd.read_excel('../data/raw/ENAHO'+str(year)+'.xlsx')
    data4 = df[df["CondMig"]==1]
    df = pd.DataFrame(data4)

    data = df.as_matrix(columns=['REGION','ZONA','A5','RegNac', 'RegResAnt','A16B','CondAct'])

    """
    REGION = Region socioeconomica donde reside
    Zona = Rural o Urbana
    A5 = Edad
    RegNac = Region de Nacimiento
    RegResAnt = Region de residencia hace dos anios
    A16B = Titulo
    CondAct = Fuera de la fuerza de trabajo, desempleado, ocupado
    """

    new = pd.DataFrame(data)
    new.columns =['region_residencia','zona','edad','region_nacimiento', 'residencia_hace_dos_anos','titulo','condicion_actual']

    data2 = new.sample(frac=0.2)

    new2 = pd.DataFrame(data2)
    data3 = new2.dropna().to_csv("../data/clean/"+str(year)+".csv")

    #print data3
