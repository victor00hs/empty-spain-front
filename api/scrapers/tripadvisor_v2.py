from os import replace
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import json
#from selenium.webdriver.common.keys import Keys

url = []

def contenido_TripAdvisor(user_input):
    # Headless is faster than a window browser and consumes less resources since there is no need for a GUI
    #Headless para evitar que se lance la ventana de chrome, ahorrando recursos ya que no se necesitan para la Interfaz Gráfica de Usuario
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') 
    PATH = "C:/WebDriver/bin/chromedriver.exe"
    driver = webdriver.Chrome(PATH, options=options)
    driver.get('https://www.tripadvisor.es/Hotels')     #Lanzar la URL
    driver.find_element_by_xpath('//*[@id="_evidon-accept-button"]').click()    #Aceptar Cookies

    window_before = driver.window_handles[0]
    buscador = driver.find_element_by_xpath('//input').send_keys(user_input)  #Buscar en la barra de busqueda
    time.sleep(1)

    driver.find_element_by_xpath('//*[@id="typeahead_results"]/a[1]').click()
    '''    
    #driver.find_element_by_xpath('//input').send_keys(Keys.ENTER)
    #cont = driver.find_element_by_xpath('//*[@id="BODY_BLOCK_JQUERY_REFLOW"]/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[1]/div/div[3]/div/div[1]/div/div[2]/div/div/div/div/div').click()
    #time.sleep(2)

    #window_after = driver.window_handles[1]
    #driver.switch_to.window(window_after)'''
    time.sleep(3)
    url.append(driver.current_url)      # Url 

    return driver.page_source



def info_TripAdvisor(location):
    decoded_location = location.decode('utf-8')
    output = {}
    output[decoded_location] = []

    #Variables aux
    array_cosas = []
    array_alojate = []
    array_comer = []
    r = contenido_TripAdvisor(decoded_location)
    soup = BeautifulSoup(r, 'lxml')

    contenedor = soup.find_all(class_="_1HQROFP")   # Clase general con toda la informacion
    for filas in contenedor:
        haz_cosas = filas.find_all(class_="_2dicJkxa _1EJ8NpwH _21Eo9VeW _2shTTUfB")[1] # Clase de cosas que hacer
        for cositas in haz_cosas:
            cont_cosas = cositas.find_all(class_="_1RFDj48Z") # Nombres por separado
            
            for contenido_cosas in cont_cosas:
                #Titulo
                try:
                    titulo_cosas = contenido_cosas.find(class_="VQlgmkyI WullykOU _3WoyIIcL").text
                except Exception as e:
                    titulo_cosas = ""
                #Imagen
                try:
                    imagen_cosas = contenido_cosas.find("img").attrs['src']
                except Exception as e:
                    imagen_cosas = ""
                #Valoracion
                try:
                    valoracion_cosas = contenido_cosas.find(class_="zTTYS8QR _1myiToNC _1z-B2F-n").attrs['aria-label'].replace("burbujas", "puntos")
                except Exception as e:
                    valoracion_cosas = ""
    
                cosas_dict = {
                    'Titulo': titulo_cosas,
                    'Imagen': imagen_cosas,
                    'Valoracion': valoracion_cosas
                }
                array_cosas.append(cosas_dict)

        alojate = filas.find_all(class_="_2dicJkxa _1EJ8NpwH _21Eo9VeW _2shTTUfB")[2]   # Clase de alojamiento
        for alojate_clase in alojate:
            cont_alojate = alojate_clase.find_all(class_="_1RFDj48Z") # Nombres por separado

            for contenido_alojate in cont_alojate:
                #Titulo
                try:
                    titulo_alojate = contenido_alojate.find(class_="VQlgmkyI WullykOU _3WoyIIcL").text
                except Exception as e:
                    titulo_alojate = ""
                #Imagen
                try:
                    imagen_alojate = contenido_alojate.find("img").attrs['src']
                except Exception as e:
                    imagen_alojate = ""
                #Valoracion
                try:
                    valoracion_alojate = contenido_alojate.find(class_="zTTYS8QR _1myiToNC _1z-B2F-n").attrs['aria-label'].replace("burbujas", "puntos")
                except Exception as e:
                    valoracion_alojate = ""
                
                alojate_dict = {
                    'Titulo': titulo_alojate,
                    'Imagen': imagen_alojate,
                    'Valoracion': valoracion_alojate
                }
                array_alojate.append(alojate_dict)

        comer = filas.find_all(class_="_2dicJkxa _1EJ8NpwH _21Eo9VeW _2shTTUfB")[3]     # Clase de restaurantes
        
        for comer_clase in comer:
            cont_comer = comer_clase.find_all(class_="_1RFDj48Z") # Nombres por separado
            
            for contenido_comer in cont_comer:
                #Titulo
                try:
                    titulo_comer = contenido_comer.find(class_="VQlgmkyI WullykOU _3WoyIIcL").text
                except Exception as e:
                    titulo_comer = ""
                #Imagen
                try:
                    imagen_comer = contenido_comer.find("img").attrs['src']
                except Exception as e:
                    None
                #Valoracion
                try:
                    valoracion_comer = contenido_comer.find(class_="zTTYS8QR _1myiToNC _1z-B2F-n").attrs['aria-label'].replace("burbujas", "puntos")
                except Exception as e:
                    valoracion_comer = ""
                #Descripcion
                try:
                    descripcion_comer = contenido_comer.find(class_="DrjyGw-P _26S7gyB4 _3gC8zGeY _3SccQt-T").text
                except Exception as e:
                    descripcion_comer = ""

                comer_dict = {
                    'Titulo': titulo_comer,
                    'Imagen': imagen_comer,
                    'Valoracion': valoracion_comer,
                    'Descripcion': descripcion_comer
                }
                array_comer.append(comer_dict)
        
        output[decoded_location].append({
            'Url': url[-1],
            'Cosas que hacer': array_cosas,
            'Alojate en': array_alojate,
            'Comer en': array_comer
        })
    return json.dumps(output, indent=3)


#print(info_TripAdvisor(b'Samaniego'))
#print(info_TripAdvisor(b'madrigalejo del monte'))