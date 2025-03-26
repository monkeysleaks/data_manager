""" crear post portal desde la base de datos """
"""
    1.- obtener datos desde supabse
    2.- filtrar los datos
    3.- crear post con salida en consola
    4.- opcional crear salida en markdown
    5.- actualizar base de datos 

"""

import os
from supabase import create_client, Client
from supabase.client import ClientOptions
from icecream import ic
import json
import time

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(
    url, 
    key,
    options=ClientOptions(
        schema="pruebas",
    )
)

# obtener tabla completa de videos
def get_data(artista):
    response = (
        supabase.table(f"{artista}_videos")
        .select("*")
        .execute())

    return(response.data)

#filtrar los datos por duración y si están en portalnet, devuelve una lista con los datos filtrados 
def data_filter(datos):
    datos_filtrados = []
    for dato in datos:
        if dato["length"] >= "00:50":
            if dato["portal"] == False:
                datos_filtrados.append(dato)
                print(f"id: {dato["id"]}, title: {dato["title"]}, length: {dato["length"]}")
    return datos_filtrados

# busca un nombre de video en la lista filtrada y crea un post en consola, ademas devuelve la información del video seleccionado

def create_template(datos_filtrados, artista,title):
    
    elemento = list(filter(lambda item: item["title"] == title, datos_filtrados))
    nombre = (elemento[0]["title"].rsplit(".",1))
    print(f'''
            [URL=https://ik.imagekit.io/bhba8douv/{artista}/{nombre[0]}]
            [IMG]https://ik.imagekit.io/bhba8douv/{artista}/{nombre[0]}[/IMG][/URL]
            filesize: {elemento[0]["file_size"]}
            Resolution: 1280x720
            Duration: {elemento[0]["length"]}
            https://voe.sx/e/{elemento[0]["code_voe"]}
            descarga''')
    return elemento
            
#actualiza db columna portal
def update_db(artista, id):
    response = (
    supabase.table(f"{artista}_videos")
    .update({"portal": True}).eq("id", id)
    .execute())
    ic("Base de Datos Actualizada")
    print(response.data)
    
    

if __name__ == "__main__":
    artista = input("ingrese artista: ")
    datos  = get_data(artista)
    datos_filtrados = data_filter(datos)
    title = input("ingrese el nombre del video: ")
    elemento = create_template(datos_filtrados, artista, title)
    update_db(artista, id= elemento[0]["id"])