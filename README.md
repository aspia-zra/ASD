# Advanced Software Development University Group Project
## This project uses Tkinter and Python to develop an apartment management web application. 

A four person project.
Credits to: 
- Imaan Mohamed
- Azra Rahman
- Rodha A Ali
- Mercy Lang'At

Check the requirements.txt file to run.

LOGIN CREDS:
(1,'Imaan Mohamed','07999999999','imaan@pams.com','$2b$12$V911MVhGicKRL9PRTDbyyO.pIynN2Tza6JWXQA9thYizVOUaTGfFy','admin',1,NULL),(2,'Rho','07123456789','rho@test.com','$2b$12$clm66bD1lpfOH2f2LntJpeaTTxleBpzDdZ1c9LHGJgc/D3neRX5A2','admin',1,NULL),(3,'Helen Carter','07111111111','helen.admin@paragon.com','pass123','maintenance',1,NULL),(4,'Mark Davies','07222222222','mark@pams.com','$2b$12$fWdlDZZB4TZF0J.8P35.ReHFMXmlCJ1fuQcKHFEmc3X2DPHBatttm','manager',2,NULL),(5,'Samir Khan','07333333333','samir.maint@paragon.com','$2b$12$fWdlDZZB4TZF0J.8P35.ReHFMXmlCJ1fuQcKHFEmc3X2DPHBatttm','finance',1,NULL),(6,'Lucy Brown','07444444444','lucy.frontdesk@paragon.com','$2b$12$fWdlDZZB4TZF0J.8P35.ReHFMXmlCJ1fuQcKHFEmc3X2DPHBatttm','frontdesk',3,NULL),(7,'Tom Wilson','07555555555','tom.maint@paragon.com','$2b$12$fWdlDZZB4TZF0J.8P35.ReHFMXmlCJ1fuQcKHFEmc3X2DPHBatttm','maintenance',4,NULL),(8,'John Smith','07666666666','john.smith@email.com','pass123','tenant',3,NULL),(9,'Emma Jones','07777777777','emma.jones@email.com','pass123','tenant',3,NULL),(10,'Michael Lee','07888888888','michael.lee@email.com','pass123','tenant',3,NULL),(11,'Sara White','07999999999','sara.white@email.com','pass123','tenant',3,NULL),(12,'Daniel Green','071111111111','daniel.green@email.com','pass123','tenant',3,NULL),(13,'David Johnson','07123456789','david.johnson@email.com','$2b$12$clm66bD1lpfOH2f2LntJpeaTTxleBpzDdZ1c9LHGJgc/D3neRX5A2','tenant',3,'2026-03-17 14:22:02'),(15,'test','098765','test@pams.com','$2b$12$gxFSXCblcdzIoqAvTGSWpO6jsXpimDXI9.hERcuLsHLI1QnAovUay','frontdesk',1,'2026-03-18 00:00:00'),(16,'test2','09876543','test.maint@pams.com','$2b$12$bn6yNp6rmqWN48y9.WbaGuCGaJboMjFwPvqA/n1vJ71.mxe9whyRu','maintenance',1,'2026-03-18 00:00:00'),(17,'drashti samgi','0987654321','drashti@pams.com','$2b$12$/FkOweyFwj1wzf8YrYxPz./G3ESBuSAxk/soDuWhz7vOPu4ZpTHPa','frontdesk',1,'2026-03-19 00:00:00'),(18,'tester','098765432','tester@pams.com','$2b$12$A4mipo7CP5aM2m5fYlZBCOWPNJT2ERHX2W6h6Cb8lDSN7WoWkD75m','manager',1,'2026-03-23 00:00:00'),(21,'Alice Cooper','07000000001','alice@email.com','$2b$12$dummyhash1','tenant',2,NULL),(22,'Brian Cox','07000000002','brian@email.com','$2b$12$dummyhash2','tenant',2,NULL),(23,'Charlie Black','07000000003','charlie.maint@paragon.com','$2b$12$dummyhash3','maintenance',2,NULL),(24,'Diana Prince','07000000004','diana.frontdesk@paragon.com','$2b$12$dummyhash4','frontdesk',3,NULL);


# Installation Guide:
## Venv setup:
#### For compatibility, running on python 3.10 is recommended.
### Step 1:
python3.10 -m venv venv310

### Step 2:
source venv310/bin/activate

## Libraries:
### Use pip or pip3 to install:
pip install bcrypt
pip install mysql-connector-python
pip install matplotlib
pip install customtkinter

#### The following libraries are used in our code come pre-installed.
- tkinter
- re
- os
- time
- datetime
- smtplib
- email
- unittest

## To run the application:
#### Alternatively use python3
python main.py
