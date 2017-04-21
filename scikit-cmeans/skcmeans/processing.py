import pandas as pd
import numpy as np
import savReaderWriter as spss


#class Preprocess():

for year in range(2014,2017):

    df = pd.read_excel('../data/raw/ENAHO'+str(year)+'.xlsx')
    data4 = df[df["CondMig"]==1]
    df = pd.DataFrame(data4)

    data = df.as_matrix(columns=['REGION','ZONA','A5','RegNac', 'RegResAnt','A16B','CondAct','ithn','np'])

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

    new = pd.DataFrame(data)
    new.columns =['region_residencia','zona','edad','region_nacimiento', 'residencia_hace_dos_anos','titulo','condicion_actual', 'ingreso_total_hogar_neto','nivel_pobreza']

    data2 = new.sample(frac=0.2)

    new2 = pd.DataFrame(data2)
    data3 = new2.dropna().to_csv("../data/clean/"+str(year)+".csv")

    #print data3
