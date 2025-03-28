import requests
import os
from src.api import supabase_api as db
from icecream import ic
from dotenv import load_dotenv
load_dotenv()


def get_codes(artista):
    artistas = db.get_all_data("official", "artistas") 

    for modelo in artistas:
        if modelo["name"] == artista:
            artista_id = modelo["artista_id"]

    datos = db.get_data_eq("official", "videos", artista_id)
    return datos

def download_file(artista, datos):
    fallas = []
    for dato in datos:
        code_voe = dato["code_voe"]
        nombre_archivo = f"E:/datos/{artista}/thumbnails_{artista}/{dato['title'].rsplit('.',1)[0]}.webp"

        url = f"https://i.voe.sx/cache/{code_voe}_storyboard_L3.jpg"  # Reemplaza con la URL del archivo 

        response = requests.get(url, stream=True)  # stream=True descarga en partes
        if response.status_code == 200:
            with open(nombre_archivo, "wb") as file:
                for chunk in response.iter_content(1024):  # Guarda en bloques de 1KB
                    file.write(chunk)
            print(f"Descarga completada: {nombre_archivo}")
        else:
            
            fallas.append(dato["title"])
            with open("img_fallas.txt", "a") as file:
                file.write(f"{dato['title']}\n")
            print(f"Error al descargar el archivo: {response.status_code}")
    print(fallas)
    return fallas

def crear_carpeta(artista):
    ruta = f"E:/datos/{artista}/thumbnails_{artista}"
    if not os.path.exists(ruta):
        os.mkdir(ruta)
        print("carpeta creada")
    else:
        print("carpeta ya existe")

def main(artista):
    datos = get_codes(artista)
    crear_carpeta(artista)
    download_file(artista, datos)
    

if __name__ == "__main__":
    artista = input("ingrese artista: ")
    main(artista)