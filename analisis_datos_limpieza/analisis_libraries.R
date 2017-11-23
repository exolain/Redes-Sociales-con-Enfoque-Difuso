library("factoextra")
library("FactoMineR")
survey_data <- read.csv("/home/lain/Redes-Sociales-con-Enfoque-Difuso/other_datasets/libraries_surveys/clean/2015_v5_libraries.csv")

cols <- c(1:41)
#head(survey_data[cols], n=40)

df <- survey_data[cols]

table(survey_data$sit_and_Study, survey_data$low_budget_e_reader_1_high_2_no_3)
res.pca <- PCA(df,  graph = FALSE)

km.res <- kmeans(survey_data, 4, nstart = 25)

fviz_cluster(km.res, data = survey_data[cols],
             palette = c("#00AFBB","#2E9FDF", "#E7B800", "#FC4E07"),
             ggtheme = theme_minimal(),
             main = "Partitioning Clustering Plot"
)
# Visualize eigenvalues/variances
fviz_screeplot(res.pca, addlabels = TRUE, ylim = c(0, 50))

var <- get_pca_var(res.pca)

# Contribution of variables
head(var$contrib)

# Control variable colors using their contributions
fviz_pca_var(res.pca, col.var="contrib",
             gradient.cols = c("#00AFBB", "#E7B800", "#FC4E07"),
             repel = TRUE # Avoid text overlapping
)