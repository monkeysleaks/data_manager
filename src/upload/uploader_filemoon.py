
import requests
import json
import os
import time
import csv
from icecream import ic
import winsound
from src.api import filemoon





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
        lista_videos.append(f"E:/datos/{artista}/videos/{video.rsplit('.',1)[0]}")
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

def titles_filemoon(artista):
    #abrir el csv
    lista_titles_filemoon = []
    data = filemoon.get_data_folder_filemoon(artista)
    for video in data:
        title = video["link"].rsplit("/",1)[1]
        lista_titles_filemoon.append(title)

    return lista_titles_filemoon


# -------- programa principal --------------
def main_upload_filemoon(artista):
    ic("---- subir a filemoon----")
    token_filemoon = os.environ.get('API_KEY_FILEMOON')
    folders = filemoon.get_folders_filemoon(token_filemoon)
    for folder in folders:
        if folder["name"] == artista:
            folder_id = folder["fld_id"]
            break
  
    lista_nombres_local = []
    lista_filemoon = titles_filemoon(artista)
   
    lista_videos = os.listdir(f"E:/datos/{artista}/videos")
    for i in lista_videos:
        lista_nombres_local.append(i)
    
    set_lista_filemoon = set(lista_filemoon)
    set_lista_videos_local = set(lista_nombres_local)
    diferencia_videos = set_lista_videos_local.difference(set_lista_filemoon)
    print(f"total de videos en filemoon: {len(set_lista_filemoon)}") 
    print(f"total de videos en carpeta: {len(lista_nombres_local)}")
    ic(f"faltan: {len(diferencia_videos)} videos")

    #crear los path usando el nombre del video, incluida la extension
    lista_rutas = list(diferencia_videos)
    lista_path = []
    for ruta in lista_rutas:
        lista_path.append(f"E:/datos/{artista}/videos/{ruta}")
    # print(lista_path)

    #subir y mover los archvivos
    for valor, ruta in enumerate(lista_path):
        url_servidor = obtener_servidor(token_filemoon)
        respuesta = subir_archivo(ruta, token_filemoon,url_servidor)
        files = respuesta["files"]
        for file in files:
            filecode = file["filecode"]
            print(filecode)
            break
        filemoon.move_folder_filemoon(token_filemoon, filecode, folder_id)
        print(respuesta)
        ic(valor)
        time.sleep(3)

    ruta_sonido = "C:/Users/diego/Desktop/windows-notify.wav"
    winsound.PlaySound(ruta_sonido, winsound.SND_FILENAME) 

if __name__ == "__main__":
    artista = "sopaipaposting"
    main_upload_filemoon(artista)

            
            









