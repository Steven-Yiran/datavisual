
# set working directory
setwd("~/Desktop/datavisual")

# install libraries
#install.packages("data.table")
library(data.table)
library(tidyverse)
library(dplyr)

# read data, skip first 16 lines
Bat3D <- fread("data/alldata-simple.dat", quote = "", fill = TRUE, skip = 16)
# convert from df to matrix
Bat3D <- data.matrix(Bat3D)
colnames(Bat3D) <- c("X [R]", "Y [R]", "Z [R]", "U_x [km/s]", "U_y [km/s]", "U_z [km/s]", "B_x [nT]", "B_y [nT]", "B_z [nT]", "p [nPa]")
#4029888 set boundary
Bat3D_Data <- Bat3D[0:4029888,]
Bat3D_Pos <- Bat3D[4029889:nrow(Bat3D), 1:8]
colnames(Bat3D_Pos) <- c("P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8")

#export data
#BAT_P <- Bat3D_Data[,c(1,2,3,10)]
#BAT_U <- Bat3D_Data[,c(1,2,3,4,5,6)]
#BAT_B <- Bat3D_Data[,c(1,2,3,7,8,9)]

# to csv
write.csv(Bat3D_Data, "alldata.csv")
write.csv(Bat3D_Pos, "allpos.csv")