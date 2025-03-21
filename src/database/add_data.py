#añadir nuevos datos juntando los datos de voe y filemoon
from src.api import supabase_api as db
from src.api.voe import Voe
from src.api import filemoon
import os
import requests
from icecream import ic
"""
1.- llamar a la api de voe
2.- llamar a la api de filemoon
3.- cruzar los datos
4.- crear el artista en supabase
5.- subir los datos a supabase

"""
#1 .- llamar a la api de voe
def get_data_folder_voe(artista): 
    token_voe = os.environ.get('API_KEY_VOE')
    folders = Voe.get_folders(token_voe)

    for folder in folders:
        if folder["name"] == artista:
            folder_id_voe = folder["fld_id"]
            break

    data_videos_voe =Voe.get_data_folder(token_voe, folder_id_voe)
    return data_videos_voe

def convertir_tiempo(tiempo):
    segundos = tiempo
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    segundos_restantes = segundos % 60
    resultado_hora = (f"{horas:02}:{minutos:02}:{segundos_restantes:02}")
    resultado = (f"{minutos:02}:{segundos_restantes:02}")
    if horas == 0:
        tiempo = resultado  # si hay horas, se actualiza el length
    else:
        tiempo = resultado_hora
    return tiempo
    
def convertir_a_MB(peso):
    # 1 MB = 1,048,576 bytes
    cambio = peso / (1_048_576)
    redondear = round(cambio,2)
    peso = f"{redondear} MB"
    
    return peso

def cruzar_datos(data_videos_voe, data_videos_filemoon):
    data_videos_voe = get_data_folder_voe(artista)
    # ic(data_videos_voe)
    data_videos_filemoon = filemoon.get_data_folder_filemoon(artista)
    # ic(data_videos_filemoon)
    informacion = []
    for dato_voe in data_videos_voe:
        for dato_filemoon in data_videos_filemoon:
            duracion = convertir_tiempo(dato_voe["length"])
            tamanio = convertir_a_MB(dato_voe["size_720p"])
            if dato_voe["title"].rsplit(".")[0] == dato_filemoon["title"]:
                
                info = {
    "title": f"{dato_voe['title']}",
    "code_voe": f"{dato_voe['filecode']}",
    "code_filemoon": f"{dato_filemoon['file_code']}",
    "length": f"{duracion}",
    "file_size": f"{tamanio}",
    "img": f"https://ik.imagekit.io/b2o3nmna5/{artista}/{dato_voe['title'].rsplit('.',1)[0]}",
    "portal": "False",
    "views" : "0", }
                informacion.append(info)
    
    return informacion


def main(artista, fld_voe):
  db.insert_data("official", "artistas", {"name": artista, "fld_voe": fld_voe})
  data_videos_voe = get_data_folder_voe(artista)
  data_videos_filemoon = filemoon.get_data_folder_filemoon(artista)
  datos = cruzar_datos(data_videos_voe, data_videos_filemoon)
  for dato in datos:
      db.insert_data("official", "videos", dato)


if __name__ == "__main__":
    artista = "alitaaa"
    main(artista, 1)
