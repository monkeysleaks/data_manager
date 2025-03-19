import requests
import json
import os
import time
import winsound
from src.api import supabase_api as db
from ssl import SSLEOFError
from icecream import ic
from dotenv import load_dotenv
load_dotenv()


class Voe:
    # Constructor
    def __init__(self, token):
        self.token = token

    # Métodos
    def get_folders(token): 
        url = f"https://voe.sx/api/folder/list?key={token}&fld_id=0"
        response = requests.get(url)
        data = response.json()
        return data["result"]["folders"]

    def get_balance(token):      
        url = f"https://voe.sx/api/account/info?key={token}"
        response = requests.get(url)
        data = response.json()
        #  print(data)
        return data["result"]["balance"]

    def nombre_video():
        lista_video = os.listdir(ruta)
        return lista_video

    def info_carpeta_voe(api_key_voe, folder_id_voe):
        url = f"https://voe.sx/api/file/list?key={api_key_voe}&page=1&per_page=250&fld_id={folder_id_voe}"
        response = requests.get(url) 
        if response.status_code == 200:
            data = response.json() # recibe los datos en formato json
            # dar formato al json
            formatted_json = json.dumps(data, indent=2, ensure_ascii=False)
            result = data["result"]
            datos = result["data"]
            return datos
        
    def obtener_nombre_voe(datos):
        lista_nombres_voe= []
        for dato in datos:
            nombre = dato["name"]
            lista_nombres_voe.append(nombre)
        return lista_nombres_voe

        
    def comparar_videos(lista_video, lista_nombres_voe):
        set_lista_video = set(lista_video)
        set_lista_nombres_voe = set(lista_nombres_voe)
        comparacion = set_lista_video.difference(set_lista_nombres_voe)
        lista_comparacion = list(comparacion)
        return lista_comparacion

    def crear_ruta(lista_comparacion):
        lista_rutas = []
        for ruta in lista_comparacion:
            ruta = f"E:/datos/{artista}/videos/{ruta}"
            lista_rutas.append(ruta)
        return lista_rutas
        

    def obtener_servidor(api_key):
        url = f"https://voe.sx/api/upload/server?key={api_key}"
        response = requests.get(url)
        servidor = response.json()
        url_servidor = servidor["result"]
        # print(response)
        print("servidor obtenido")
        return url_servidor 

    def move_vid(api_key_voe, file_code, folder_id):
        url = f"https://voe.sx/api/file/set_folder?key={api_key_voe}&file_code={file_code}&fld_id={folder_id}"
        response = requests.get(url)
        print (response.json())
        return response.json()

    def subir_archivo(ruta, api_key, url_servidor):
        videos_subidos = []
        data = {
            'key': api_key
        }
        try:
            with open(ruta, 'rb') as f:
                files = {
                    'file': (ruta, f)
                }
                response = requests.post(url_servidor, data=data, files=files)
                if response.status_code == 200:
                    try:
                        return response.json()
                    except:
                        return response.status_code
                else:
                    return response.status_code
        except Exception as e:
            print(f"Error: {e}")
        return videos_subidos
    
# ---- programa principal -----------------------------------
if __name__ == "__main__":
    
    #listar variables
    ic("----subir a voe----")
    api_key_voe = os.environ.get('API_KEY_VOE')
    artista = input("ingrese artista: ")
    folders = Voe.get_folders(api_key_voe)
    for folder in folders:
        if folder["name"] == artista:
            folder_id_voe = folder["fld_id"]
            break

    ruta = f"E:/datos/{artista}/videos"


    # 1° listar nombres en local
    lista_video = Voe.nombre_video()

    # 2° llamar a la api
    datos = Voe.info_carpeta_voe(api_key_voe, folder_id_voe)

    # 3° filtrar datos de la carpeta en voe
    lista_nombres_voe = Voe.obtener_nombre_voe(datos)
    print("videos subidos: ", len(lista_nombres_voe))
 
    #4° comparar las listas
    lista_comparacion = Voe.comparar_videos(lista_video, lista_nombres_voe)
    print("faltan: ", len(lista_comparacion))

    # 5° crear rutas
    lista_rutas = Voe.crear_ruta(lista_comparacion)

    # 7° subir archivos
    try:
        for numero,  ruta in enumerate(lista_rutas):
            url_servidor = Voe.obtener_servidor(api_key_voe)
            respuesta = Voe.subir_archivo(ruta, api_key_voe, url_servidor)
            ic(respuesta)
            file_code = (respuesta["file"]["file_code"])
            ic(numero, ruta)
            Voe.move_vid(api_key_voe, file_code, folder_id_voe)
            time.sleep(1)
        ruta_sonido = "C:/Users/diego/Desktop/windows-notify.wav"
        winsound.PlaySound(ruta_sonido, winsound.SND_FILENAME) 
    except Exception as e:
        print(f"Error: {e}")
