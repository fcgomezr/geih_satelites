

library(plyr)
library(dplyr)
library(foreign)

meses <- c("Enero","Febrero","Marzo","Abril",
           "Mayo","Junio","Julio","Agosto",
           "Septiembre","Octubre","Noviembre","Diciembre")

for (mes in c(1:12)) {

  if (mes < 10) {
    dir <- paste("C:/Users/User/dane.gov.co/DANE_CONVENIO DANE-CRA 2022_0365 - Convenio DANE - CRA/Base de datos/GEIH/GEIH 2009/0",mes,"/",sep="")
  }else {  
    dir <- paste("C:/Users/User/dane.gov.co/DANE_CONVENIO DANE-CRA 2022_0365 - Convenio DANE - CRA/Base de datos/GEIH/GEIH 2009/",mes,"/",sep="")
  } 
  #arc <- paste("Cabecera - Ocupados (",mes,").sav",sep = "")
  arc <- paste("Resto - Ocupados (",mes,").sav",sep = "")
  
  des<- paste(dir,arc,sep = "")
  
  data_ <- as.data.frame(read.spss(des))# assign your data frame here
  data_$mes <- mes
  if (mes == 1 ) {
    
    data <- data_
  }else if  (mes != 1 ){
    data <- rbind.fill(data,data_)
    }
    
}

## 2010 & 2013 & 2014
meses <- c("Enero","Febrero","Marzo","Abril",
           "Mayo","Junio","Julio","Agosto",
           "Septiembre","Octubre","Noviembre","Diciembre")
mes <- 0
for (mesr in meses) {
  
  mes <- mes + 1
  
  dir <- paste("C:/Users/User/dane.gov.co/DANE_CONVENIO DANE-CRA 2022_0365 - Convenio DANE - CRA/Base de datos/GEIH/GEIH 2014/",mesr,"/",sep="")
  #arc <- paste("Cabecera - Ocupados (",mes,").sav",sep = "")
  #arc <- paste("Resto - Ocupados (",mes,").sav",sep = "")
  #arc <- paste("Cabecera - Ocupados.sav",sep = "")
  arc <- paste("Resto - Ocupados.sav",sep = "")
  des<- paste(dir,arc,sep = "")
  
  data_ <- as.data.frame(read.spss(des))# assign your data frame here
  data_$mes <- mes
  if (mes == 1 ) {
    
    data <- data_
  }else if  (mes != 1 ){
    data <- rbind.fill(data,data_)
  }
  
}


### 2011  ###
meses <- c("Enero","Febrero","Marzo","Abril",
           "Mayo","Junio","Julio","Agosto",
           "Septiembre","Octubre","Noviembre","Diciembre")
mes <- 0
for (mesr in meses) {
  
  mes <- mes + 1
  
  dir <- paste("C:/Users/User/dane.gov.co/DANE_CONVENIO DANE-CRA 2022_0365 - Convenio DANE - CRA/Base de datos/GEIH/GEIH 2011/",mesr,".sav/",sep="")
  #arc <- paste("Cabecera - Ocupados.sav",sep = "")
  arc <- paste("Resto - Ocupados.sav",sep = "")
  des<- paste(dir,arc,sep = "")
  
  data_ <- as.data.frame(read.spss(des))# assign your data frame here
  data_$mes <- mes
  if (mes == 1 ) {
    
    data <- data_
  }else if  (mes != 1 ){
    data <- rbind.fill(data,data_)
  }
  
}



for (mes in c(1:12)) {
  
  if (mes < 10) {
    dir <- paste("C:/Users/User/dane.gov.co/DANE_CONVENIO DANE-CRA 2022_0365 - Convenio DANE - CRA/Base de datos/GEIH/GEIH 2012/0",mes,"/",sep="")
  }else {  
    dir <- paste("C:/Users/User/dane.gov.co/DANE_CONVENIO DANE-CRA 2022_0365 - Convenio DANE - CRA/Base de datos/GEIH/GEIH 2012/",mes,"/",sep="")
  } 
  #arc <- paste("Cabecera - Ocupados.sav",sep = "")
  arc <- paste("Resto - Ocupados.sav",sep = "")
  
  des<- paste(dir,arc,sep = "")
  
  data_ <- as.data.frame(read.spss(des))# assign your data frame here
  data_$mes <- mes
  if (mes == 1 ) {
    
    data <- data_
  }else if  (mes != 1 ){
    data <- rbind.fill(data,data_)
  }
  
}






data %>%
  group_by(mes)%>%
  dplyr::summarise(n=n())



con<-file('E:/GEIH/Total/Bases 2009 - 2014/GEIH_2014.csv',encoding="UTF-8")
write.csv(data,file=con,na = "")
