
import requests
import json
import os
import time
import csv
from icecream import ic
import winsound





def info_cuenta(api_key):
    url = f"https://filemoonapi.com/api/account/info?key={api_key}"
    response = requests.get(url) 
    if response.status_code == 200:
        data = response.json() # recibe los datos en formato json
        print(data)
    else:
        print(response)

def get_folders(token):
    url = f"https://filemoonapi.com/api/folder/list?key={token}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json() # recibe los datos en formato json
        print(data)

def set_folder(token, filecode, folder_id_destino):
    url = f"https://filemoonapi.com/api/file/clone?key={token}&file_code={filecode}&fld_id={folder_id_destino}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json() # recibe los datos en formato json
        print(data)
    

def info_carpeta(api_key, folder_id):
    url= f"https://filemoonapi.com/api/folder/list?key={api_key}&fld_id={folder_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json() # recibe los datos en formato json
        print(data)
def obtener_servidor(api_key):
    url = f"https://filemoonapi.com/api/upload/server?key={api_key}"
    response = requests.get(url)
    servidor = response.json()
    url_servidor = servidor["result"]
    print(response)
    print(servidor)
    print(url_servidor)
    return url_servidor

def create_folder(token, folder_name):
    url = f"https://filemoonapi.com/api/folder/create?key={token}&parent_id=0&name={folder_name}"
    response = requests.get(url)
    data = response.json()
    fld_id = data["result"]["fld_id"]
    print(fld_id)
    return fld_id

def listar_videos(artista):
    lista_videos = []
    videos = os.listdir(f"E:/datos/{artista}/videos")
    for video in videos:
        lista_videos.append(f"E:/datos/{artista}/videos/{video}")
    return lista_videos

def subir_archivo(ruta, api_key, url_servidor):
    """
    Sube un archivo al servidor dado.

    Parámetros:
    ruta_archivo (str): La ruta al archivo que se desea subir.
    clave_api (str): La clave API requerida por el servidor.
    url (str): La URL del servidor. (Por defecto: "https://be2719.rcr22.ams01.cdn112.com/upload/01")
    
    Retorna:
    dict: Respuesta del servidor si es JSON.
    int: Código de estado si no hay respuesta JSON.
    """
    # Datos que se enviarán (clave API)
    data = {
        'key': api_key
    }

    # Archivo a subir
    try:
        with open(ruta, 'rb') as f:
            files = {
                'file': (ruta, f)
            }
            # Hacer la solicitud POST
            response = requests.post(url_servidor, data=data, files=files)
            # Verificar la respuesta
            if response.status_code == 200:
                print("Subiendo Archivo....")
                try:
                    # Intentar obtener la respuesta en JSON
                    return response.json()
                except:
                    # Si no hay respuesta en JSON, retornar el código de estado
                    return response.status_code
            else:
                return response.status_code

    except FileNotFoundError:
        print("Archivo no encontrado")
    except requests.exceptions.SSLError:
        print("Error de seguridad en la conexión")
    except requests.exceptions.Timeout:
        print("Tiempo de espera agotado")
    except requests.exceptions.HTTPError as e:
        print(f"Error del servidor: {e.response.status_code}")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")

def procesar_csv_filemoon(ruta_csv, artista):
    #abrir el csv
    with open(ruta_csv, mode="r", encoding="utf-8") as file:
        lista_codigos_filemoon = []
        csv_reader = csv.DictReader(file)
         #procesar el csv
        for fila in csv_reader:
            nombre_archivo = fila["file name"]
            url = fila["url"]

            #extraer una porción de la url
            code_filemoon = url.split("/")[-1]  #toma la parte después del /e/

            ruta_csv = f'E:/datos/{artista}/videos/{nombre_archivo}'
            
             #añadir los dicionarios
            lista_codigos_filemoon.append(ruta_csv)
    return lista_codigos_filemoon


# -------- programa principal --------------
def main_upload_filemoon(artista):
    ic("---- subir a filemoon----")
    token_filemoon = os.environ.get('API_KEY_FILEMOON')
    folder_id = ""
    ruta_csv = f"E:/datos/Filemoon.csv"
    # #carga de archivos


    # # ver que archivos faltan para subir, por algún error o algo, este algoritmo convierte las listas en "set"
    # # y los compara como conjuntos, para esto es necesario descargar el csv de filemoon. 
    # # no usar la primera vez!!!

    lista_filemoon = procesar_csv_filemoon(ruta_csv, artista)
    lista_videos = listar_videos(artista)
    set_lista_filemoon = set(lista_filemoon)
    set_lista_videos = set(lista_videos)
    diferencia_videos = set_lista_videos.difference(set_lista_filemoon)
    print(f"total de videos en filemoon: {len(set_lista_filemoon)}") 
    print(f"total de videos en carpeta: {len(lista_videos)}")
    ic(f"faltan: {len(diferencia_videos)} videos")

    # accede al contenido en local para listar los archivos
    lista_rutas = listar_videos(artista)

    #accede al csv generado por filemoon
    lista_rutas = list(diferencia_videos)

    for valor, ruta in enumerate(lista_rutas):
        url_servidor = obtener_servidor(token_filemoon)
        respuesta = subir_archivo(ruta, token_filemoon,url_servidor)
        #mover archivo a carpeta destino
        print(respuesta)
        ic(valor)
        time.sleep(3)

    ruta_sonido = "C:/Users/diego/Desktop/windows-notify.wav"
    winsound.PlaySound(ruta_sonido, winsound.SND_FILENAME) 



            
            









