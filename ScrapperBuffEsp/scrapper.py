import os
import random
import re
from datetime import datetime
from time import sleep
from common import *

from selenium.webdriver import ActionChains

import settings

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import codecs
import time
from noti_msg import enviar_mensaje

# Encontrado será true cuando sea encontrado
encontrado = False

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" \
             " Chrome/78.0.3904.97 Safari/537.36"

previus_page_count = 0


browser = configure_driver_with_profile(settings, user_agent)

# Ir a la URL en cuestión url inicio de settings
browser.get(settings.url_inicio)
print ("Entra")
browser.implicitly_wait(1)
browser.switch_to.default_content()
time.sleep(1)

# Lista de skins que quieres buscar
skins_a_buscar = [
    {"nombre": "★ Sport Gloves | Vice (Field-Tested)", "contador": 0},               #7949.49 - 7017.66                             409.97RMB
    {"nombre": "Sport Gloves | Vice (Well-Worn)", "contador": 0},                     #6400 - 5082.45                               917.26RMB        
    {"nombre": "AK-47 | Vulcan (Factory New)", "contador": 0},                       #5075 - 4159.95                                593.1RMB
    {"nombre": "AK-47 | Vulcan (Field-Tested)", "contador": 0},                        #1559 - 1266                                   194.51RMB
    {"nombre": "★ Karambit | Doppler (Factory New)", "contador": 0},     #p1        #9649.5 - 8479.07                              538.34RMB
    {"nombre": "★ Karambit | Doppler (Factory New)", "contador": 0},     #p2         #13377 - 11575.52                             931.49RMB
    {"nombre": "★ Karambit | Doppler (Factory New)", "contador": 0},     #p3        #9425 - 8464.60                             336.62RMB
    {"nombre": "★ Karambit | Doppler (Factory New)", "contador": 0},     #p4          #9950 - 8681.64                            409.97RMB
    {"nombre": "★ Flip Knife | Doppler (Factory New)", "contador": 0},   #p1        #3469.5 - 3081.98                              159.09RMB
    {"nombre": "★ Flip Knife | Doppler (Factory New)", "contador": 0},   #p2        #4154 - 3617.35                             265.69RMB
    {"nombre": "★ Flip Knife | Doppler (Factory New)", "contador": 0},   #p3          #3445 - 2963.12                               258.46RMB
    {"nombre": "Desert Eagle | Blaze (Factory New)", "contador": 0},                   #4056 - 3617.35                           171.1RMB
    {"nombre": "Desert Eagle | Blaze (Minimal Wear)", "contador": 0},                   #4050 - 3589.71                          193.91RMB
    {"nombre": "★ M9 Bayonet | Doppler (Factory New)", "contador": 0},     #p1          #8450 - 7234.70                              668.45RMB
    {"nombre": "★ M9 Bayonet | Doppler (Factory New)", "contador": 0},     #p2           #11095 - 9766.84                            600.77RMB
    {"nombre": "AWP | Lightning Strike (Factory New)", "contador": 0},                  #3872.5 - 3327.96                       293.49RMB
    {"nombre": "M4A1-S | Icarus Fell (Factory New)", "contador": 0},                    #3246.66 - 2893.88                        138.67RMB
    {"nombre": "★ Sport Gloves | Slingshot (Field-Tested)", "contador": 0},            #5290 - 4496.37                             452.43RMB
    {"nombre": "★ Karambit | Gamma Doppler (Factory New)", "contador": 0},     #p1     #14799.5 - 13022.46                           806.97RMB
    {"nombre": "AK-47 | Vulcan (Field-Tested)", "contador": 0},                 #1559 - 1266                                   194RMB
    {"nombre": "AK-47 | Vulcan (Field-Tested)", "contador": 0},                 #1559 - 1266                                   194RMB


    # Añade más skins si es necesario
]

while not encontrado:
    for skin_info in skins_a_buscar:
        skin = skin_info["nombre"]
        contador = skin_info["contador"]
        print(f"Buscando la skin: {skin} - Intento {contador + 1}")
        
        browser.find_element(By.NAME,"search").send_keys(skin)
        browser.implicitly_wait(4)
        browser.switch_to.default_content()
        time.sleep(4)

        browser.find_element(By.ID,"autocomplete-result-0").click()
        browser.implicitly_wait(3)
        browser.switch_to.default_content()
        time.sleep(3)

        # Lista para almacenar los precios de las cinco skins desde la segunda hasta la sexta
        precios = []

        # Iterar sobre los cinco tr (del tercero al séptimo)
        for i in range(3, 8):
            # Encontrar el quinto td dentro del tr actual que no tenga la clase "des_row"
            td_element = browser.find_element(By.XPATH, f'//table[@id="market-selling-list"]//tbody//tr[not(contains(@class, "des_row"))][{i}]/td[5]')
            # Dentro de este td, encontrar el primer div
            div_element = td_element.find_element(By.XPATH, './div[1]')
            # Obtener el texto principal del elemento strong dentro del div
            numero_texto = div_element.find_element(By.XPATH, './strong').text
            # Eliminar el símbolo de la moneda y cualquier carácter que no sea un número o un punto
            numero_texto_limpio = numero_texto.replace('¥ ', '').replace(',', '').strip()
            # Convertir el texto limpio a un número decimal y agregarlo a la lista de precios
            precio = float(numero_texto_limpio)
            precios.append(precio)

        # Calcular la media de los precios
        media_precios = sum(precios) / len(precios)
        print(f"Media de precio de la skin {skin}: ", media_precios)

        # Calcular el 85% del precio medio
        skin_barata = 0.85 * media_precios

        # Ahora sacamos el precio más barato, el primero por defecto
        td_element = browser.find_element(By.XPATH, f'//table[@id="market-selling-list"]//tbody//tr[{2}]/td[5]')
        div_element = td_element.find_element(By.XPATH, './div[1]')
        numero_texto = div_element.find_element(By.XPATH, './strong').text
        numero_texto_limpio = numero_texto.replace('¥ ', '').replace(',', '').strip()
        precio_mas_barato = float(numero_texto_limpio)
        print(f"Precio más barato de la skin {skin}:" ,precio_mas_barato)

        #Si se encuentra me notifica y tiene que quedarse en la página
        if precio_mas_barato <= skin_barata:
            encontrado = True
            print(f"Se ha encontrado la skin {skin} por debajo del 85% \n")
            enviar_mensaje(skin, media_precios, skin_barata)  # Llamar a la función para enviar el mensaje
            fecha_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            browser.save_screenshot(settings.files_path + "\\encontrado-{}.png".format(fecha_actual))
            while True:
                pass  # Este bucle mantendrá el programa en ejecución
            
        else:
            print(f"No se ha encontrado la skin {skin} por debajo del 85% \n")
            skin_info["contador"] += 1  # Incrementa el contador
            # Vuelve a la página principal para volver a buscar
            browser.find_element(By.XPATH, "//strong[text()='Tienda']").click()
            browser.implicitly_wait(2)
            browser.switch_to.default_content()
            time.sleep(2)