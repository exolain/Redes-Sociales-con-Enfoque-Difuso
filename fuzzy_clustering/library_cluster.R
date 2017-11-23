s$set.seed(1680) # for reproducibility

library(dplyr) # for data cleaning
library(cluster) # for gower similarity and pam
library(Rtsne) # for t-SNE plot
library(ggplot2) # for visualization
library(factoextra)
library(fclust)

old.par <- par(mfrow=c(1, 3))

for (year in c(2015, 2016)){

  file <- paste("/home/lain/Redes-Sociales-con-Enfoque-Difuso/other_datasets/libraries_surveys/clean/",year,"_v5_libraries.csv",sep = "")
  survey_data <- read.csv(file)
  

  #plot(silhouette(ratings))
  
  
  glimpse(survey_data)
  
  df <- data.frame(matrix(runif(100), 10))
  #cols <- c(4, 7:9)
  #cols <- c(  3, 4,5,7, 16:18, 34:37,39:41)
  cols <- c(  3:10, 34:37)
  gower_dist <- daisy(survey_data[,cols],
                      metric = "gower", #weights=c(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,3),
                      type = list(logratio = 3))
  
  
  # Check attributes to ensure the correct methods are being used
  # (I = interval, N = nominal)
  # Note that despite logratio being called, 
  # the type remains coded as "I"
  
  #summary(gower_dist)
  
  gower_mat <- as.matrix(gower_dist)
  
  # Output most similar pair
  
  survey_data[
    which(gower_mat == min(gower_mat[gower_mat != min(gower_mat)]),
          arr.ind = TRUE)[1, ], ]
  
  
  survey_data[
    which(gower_mat == max(gower_mat[gower_mat != max(gower_mat)]),
          arr.ind = TRUE)[1, ], ]
  
  
  #f4 <- fanny(gower_dist, 4, memb.exp = 1.6, diss = TRUE)
  
  #FKM.noise(f4,RS=5,delta=3)
  
  f4=FKM(gower_mat[,1:(ncol(gower_mat)-1)],k=6,m=1.5,stand=1)
  
  s <- summary(f4)
  s
  #memb <- s$membership
  memb <- s$U
  #plot(silhouette(s, gower_dist))
  #fviz_silhouette(f4, label = TRUE)
  
  #s.full <- silhouette(s$clustering, gower_dist)
  #s.full
  
  #library(fpc)
  #cluster.stats(gower_dist,s$clustering)
  #library(corrplot)
  #corrplot(f4$membership, is.corr = FALSE)
  
  
  output_file <- paste("/home/lain/Redes-Sociales-con-Enfoque-Difuso/other_datasets/libraries_surveys/clean/comp_membership",year,".csv",sep = "")
  write.csv(memb, output_file)
  
  plot(f4, which = 1)
}

par(old.par)