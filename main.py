# -*- coding: utf-8 -*-
__author__ = 'Luis Antón Lopez Sobrado (luilop@uoc.edu)'

from bs4 import BeautifulSoup
from pandas import DataFrame
import requests

#URL base de la que realizaremos la extracción de los datos
URL_BASE = "https://atletismo.gal/competicions/"
# Numero máximo de paginas
MAX_PAGES = 13

# Inicializamos los datos
nombres = []
lugares = []
fechas = []
tipos = []

# Recorremos todas las paginas hasta final de año
for i in range(1, MAX_PAGES):

    # Construyo la URL
    if i >= 1 and i < 10:
        url = URL_BASE + "?cp_date=01%2F0"+str(i)+"%2F2019"
    else:
        url = URL_BASE + "?cp_date=01%2F"+str(i)+"%2F2019"        
    print(url)
    
    # Realizamos la petición a la web
    req = requests.get(url)
    # Comprobamos que la petición nos devuelve un Status Code = 200
    statusCode = req.status_code
    if statusCode == 200:
        
        # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
        html = BeautifulSoup(req.text, "html.parser")     
        
        # recorremos el codigo html en busca de las etiquetas necesarias con los datos de interes
        for c in html.find(class_='archive archive__competition').find_all(class_='row archive__body__row'):
            # recogemos el campo "fecha"
            try:                
                fecha = c.findAll('div')[0].find('span').text
            except:
                fecha = ''
            fechas.append(fecha.strip())
            # recogemos el campo "nombre" (nombre de la carrera)
            try:                
                nombre = c.findAll('div')[3].find('a').text
            except:
                nombre = ''
            nombres.append(nombre.strip())
            # recogemos el campo "lugar" (lugar donde se realizará la carrera)
            try:
                lugar = c.findAll('div')[4].find('span').text
            except:
                lugar = ''
            lugares.append(lugar.strip())
            # recorremos los diferentes tipos de comida
            try:
                tipo = c.findAll('div')[1].find('span').text
            except:
                tipo = ''
            tipos.append(tipo.strip())         
    else:
        print ("La pagina no está disponible")

# Si extraemos los datos de manera correcta generamos el pdf
if((nombres!= []) or (tipos!= []) or (nombres!= []) or (lugares!= [])):
    # Guardamos los datos recogidos en el dataset.csv
    datosCarreras= {'Nombre': nombres,'Tipo': tipos,'Lugar': lugares,'Fecha': fechas}
    df = DataFrame(datosCarreras, columns= ['Nombre', 'Tipo', 'Lugar','Fecha'])
    export_csv = df.to_csv (r'C:\Users\luisob\Documents\UOC\Asignaturas\TipologiaCicloDeVidaDeLosDatos\PRA1\dataset.csv', index = None, header=True) #Don't forget to add '.csv' at the end of the path
    print (df) 
else:
    print ("Fallo al extraer la información de la web")    
    
