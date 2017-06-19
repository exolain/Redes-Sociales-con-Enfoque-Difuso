set.seed(1680) # for reproducibility

library(dplyr) # for data cleaning
library(cluster) # for gower similarity and pam
library(Rtsne) # for t-SNE plot
library(ggplot2) # for visualization

old.par <- par(mfrow=c(1, 3))

for (year in c(2014,2015,2016)){
file <- paste("/var/www/PythonFlaskRemoteApp/backends/scikitcmeans/data/clean/",year,"_v3_migrantes.csv",sep = "")
migrantes <- read.csv(file)

glimpse(migrantes)

df <- data.frame(matrix(runif(100), 10))
cols <- c(2, 7:9)
gower_dist <- daisy(migrantes[,cols],
                    metric = "gower",
                    type = list(logratio = 3))

# Check attributes to ensure the correct methods are being used
# (I = interval, N = nominal)
# Note that despite logratio being called, 
# the type remains coded as "I"

summary(gower_dist)

gower_mat <- as.matrix(gower_dist)

# Output most similar pair

migrantes[
  which(gower_mat == min(gower_mat[gower_mat != min(gower_mat)]),
        arr.ind = TRUE)[1, ], ]


migrantes[
  which(gower_mat == max(gower_mat[gower_mat != max(gower_mat)]),
        arr.ind = TRUE)[1, ], ]


f4 <- fanny(gower_dist, 3, memb.exp = 3, diss = TRUE)
s <- summary(f4)
s
memb <- s$membership

output_file <- paste("/home/lain/Redes-Sociales-con-Enfoque-Difuso/membership",year,".csv",sep = "")
write.csv(memb, output_file)

plot(f4, which = 1)
}

par(old.par)