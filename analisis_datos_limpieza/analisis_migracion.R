acs <- read.csv("/var/www/PythonFlaskRemoteApp/backends/scikitcmeans/data/clean/2014_v3_migrantes.csv")


summary(acs)

counts <- table(acs$ingreso_por_persona)
barplot(counts, main="Ingreso por persona Distribucion",  xlab="Ingreso por persona")


counts <- table(acs$residencia_hace_dos_a_nos)
barplot(counts, main="Region de residencia hace dos años Distribution",  xlab="Region de residencia hace dos años")
s <- subset(acs , region_residencia > 0 )
  plot(x = s$edad , y = s$ingreso_discreto, type = 'p')

  
  
  scatterplotMatrix(acs)
  
  
  
  
  
  library(caret)n
  preprocessParams <- preProcess(acs, method=c("scale"))
  # summarize transform parameters
  print(preprocessParams)
  # transform the dataset using the parameters
  transformed <- predict(preprocessParams, acs)
  transformed
  # summarize the transformed dataset
  summary(transformed)
  