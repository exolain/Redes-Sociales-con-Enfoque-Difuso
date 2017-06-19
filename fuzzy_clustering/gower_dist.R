library(gower)
library(car)
library(proxy)

migrantes <- read.csv("/var/www/PythonFlaskRemoteApp/backends/scikitcmeans/data/clean/2014_v3_migrantes.csv")
no_migrantes <- read.csv("/var/www/PythonFlaskRemoteApp/backends/scikitcmeans/data/clean/2014_v3_no_migrantes.csv")


dat1 <- migrantes
dat2 <- no_migrantes

#x <- as.matrix(
  x <- (proxy::dist(dat1, dat2, method = "gower", by_rows = TRUE, pairwise = FALSE))
x
capture.output(x, file = "/home/lain/Redes-Sociales-con-Enfoque-Difuso/distance.txt")

head(dat1)
head(dat2)
cols <- which(sapply(dat1, is.numeric))
rngs <- rep(1, ncol(dat1))
rngs[cols] <- sapply(dat1[cols], function(x) max(x, na.rm=TRUE) - min(x, na.rm=TRUE)) 

cols <- which(sapply(dat2, is.numeric))
rngs <- rep(1, ncol(dat2))
rngs[cols] <- sapply(dat2[cols], function(x) max(x, na.rm=TRUE) - min(x, na.rm=TRUE)) 


gowerDist <-  as.matrix(gower_dist(dat1[7], dat2[7]))
gowerDist
capture.output(gowerDist, file = "/home/lain/Redes-Sociales-con-Enfoque-Difuso/distance.txt")

library(cluster)
f4 <- fanny(g, 3, memb.exp = 1.7, diss = TRUE)
summary(f4)
#capture.output(s, file = "/home/lain/Redes-Sociales-con-Enfoque-Difuso/results.txt")
#plot(f4)

plot(migrantes$ingreso_total_hogar_neto, no_migrantes$ingreso_total_hogar_neto) #,  cex=0.7, pos=4, col="red")

scatterplotMatrix(migrantes[2:9])
scatterplotMatrix(no_migrantes[2:9])

