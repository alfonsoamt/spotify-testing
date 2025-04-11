# This test is to search for a playlist and extract the data from web
from selenium import webdriver
# This line is necesary for search the HTML elements
from selenium.webdriver.common.by import By
# Libraries for implicit waits
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import json
import random
import os

# Obtener el directorio base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# load driver
driver = webdriver.Chrome()

# Open Spotify
driver.get("https://open.spotify.com/")
# Wait for  elements to load
driver.maximize_window()
wait = WebDriverWait(driver, 10)

# read the json with the songs and artists
json_path = os.path.join(BASE_DIR, 'files', 'Spotify_playlist_beginner.json')
with open(json_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

artists = set()
for song in data:
    artists.update(song["Artists"])

print(artists)

chosen_artists = random.sample(list(artists), 3)

print("The chosen artist to tesstare: ", chosen_artists)

body = driver.find_element(By.TAG_NAME, "body")
artists_data = []
all_artists_data = [] # Lista para guardar los datos de cada artista

# For each artists open a new tab and go down to click the artists infor and get the world position and, followers and top 5 cities.
for artist in chosen_artists:
    print("The artist to test is: ", artist)
    driver.switch_to.new_window("tab")
    driver.get("https://open.spotify.com/")
    searchBar = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='search-input']")))
    searchBar.send_keys(artist + Keys.RETURN)
    artist_button = wait.until(EC.presence_of_element_located((By.XPATH, ".//a/button/span[text() = 'Artistas']")))
    artist_button.click()
    topArtist = wait.until(EC.presence_of_element_located((By.XPATH, f".//p[@title = '{artist}']")))
    print("The top artist is: ", topArtist.text)
    topArtist.click()
    time.sleep(3)

    for _ in range(50):
        try:
            artist_info_button = driver.find_element(By.XPATH, f".//button[@aria-label='{artist}']")
            print("Button found for artist: ", artist)
            break
        except:
            body.send_keys(Keys.PAGE_DOWN)

    if artist_info_button:
        artist_info_button.click()
        try:
            # 1. Esperar a que el diálogo esté presente
            dialog = wait.until(EC.presence_of_element_located((By.XPATH, f".//dialog[@aria-label='{artist}']")))
            print(f"Diálogo encontrado para {artist}.") # Añadido para depuración

            # 2. Ahora, esperar a que data_container esté presente DENTRO del contexto del diálogo ya visible
            #    Usamos un XPath que empieza desde el diálogo para ser más específicos.
            data_container_xpath = f".//dialog[@aria-label='{artist}']//div[count(./div) >= 7]"
            data_container = wait.until(EC.presence_of_element_located((By.XPATH, data_container_xpath)))
            print(f"Data container encontrado para {artist}.") # Añadido para depuración
            try:
                # Ejemplo: Esperar por el texto del primer div que NO contiene solo números (asumiendo que es la ETIQUETA 'Seguidores')
                # O MEJOR AÚN: Esperar por el elemento que CONTIENE el número de seguidores.
                # Ajusta este XPath según tu estructura HTML real:
                xpath_elemento_con_texto_clave = ".//div[not(translate(., '0123456789.', ''))]" # Ejemplo: el valor de seguidores
                wait.until(lambda d: data_container.find_elements(By.XPATH, xpath_elemento_con_texto_clave)[0].text != "")
                print("Texto del elemento clave detectado (ya no está vacío).")
            except Exception as e:
                # Si después de 10 segundos el texto sigue vacío o el elemento no se encuentra,
                # podría indicar que el artista realmente no tiene esos datos.
                print(f"Advertencia: El texto del elemento clave no apareció o no se encontró: {e}")
                # El script continuará, pero los campos podrían seguir vacíos o N/A.

            # Intentar encontrar el elemento world_number usando find_elements
            world_number_xpath = ".//div[count(following-sibling::div) >= 7 ]/div[starts-with(.,'#')]"
            world_number_elements = data_container.find_elements(By.XPATH, world_number_xpath)

            # Verificar si la lista NO está vacía (es decir, se encontró el elemento)
            if world_number_elements:
                world_number = world_number_elements[0].text.strip("#")
                print(f"Número mundial encontrado: {world_number}")
            else:
                # Si la lista está vacía, el elemento no existe
                world_number = "N/A"
                print("Número mundial no encontrado (N/A).")

            followers = data_container.find_elements(By.XPATH, ".//div[not(translate(., '0123456789.', ''))]")[0]
            print("Followers found for artist: ", followers.text.replace(".", ""))
            mensual = data_container.find_elements(By.XPATH, ".//div[not(translate(., '0123456789.', ''))]")[1]
            print("Mensual found for artist: ", mensual.text.replace(".", ""))
            cities_elements = []
            try:
                # Buscar los 5 divs hermanos siguientes al elemento 'mensual'
                cities_xpath = "../following-sibling::div[position() <= 5]"
                cities_elements = mensual.find_elements(By.XPATH, cities_xpath) # Buscar relativo a mensual_element

                # Ahora iterar para obtener el texto de cada ciudad
                cities_text = [city.text for city in cities_elements]

                # Opcional: Verificar si se encontraron 5 ciudades
                if len(cities_text) == 5:
                    print(f"Ciudades encontradas: {','.join(cities_text)}")
                else:
                    print(f"Se encontraron {len(cities_text)} ciudades (se esperaban 5): {', '.join(cities_text)}")

            except Exception as e:
                print(f"Error al buscar/procesar ciudades después de {mensual}: {e}")
                cities_text = [] # Dejar la lista vacía si hay error
                
            # Crear un diccionario para el artista actual
            current_artist_info = {
                "Artist": artist,
                "Ranking": world_number, # Ya será "N/A" si no se encontró
                "Followers": followers.text.replace(".", ""), # Asegúrate que estas variables tengan los valores correctos
                "MonthlyListeners": mensual.text.replace(".", "")   ,
                "TopCities": cities_text # La lista de ciudades
            }
            # Añadir el diccionario a la lista general
            all_artists_data.append(current_artist_info)

            print(f"Datos recopilados para {artist}")
            print("*"*100)
        except Exception as e:
            print(f"Error esperando el diálogo o data_container para {artist}: {e}")

# Guardar todos los datos recopilados en JSON
output_dir = os.path.join(BASE_DIR, 'files')
os.makedirs(output_dir, exist_ok=True) # Asegura que el directorio exista

json_path = os.path.join(output_dir, "artist_data.json")
with open(json_path, "w", encoding="utf-8") as file:
    json.dump(all_artists_data, file, indent=4, ensure_ascii=False)

print(f"Datos de artistas guardados en {json_path}")

# Cerrar todas las ventanas y terminar el driver
driver.quit()
print("Navegador cerrado. Script finalizado.")




