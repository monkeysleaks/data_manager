import os
import os.path
import shutil
import random
import string
# from icecream import ic
# ic.disable()

#crear carpeta de destino
def crear_carpeta(carpeta):
    os.mkdir(carpeta)
    pass

def mover_archivos(carpeta_telegram, carpeta):
    archivos = os.listdir(carpeta_telegram)

    for archivo in archivos:
        ruta_origen = os.path.join(carpeta_telegram, archivo)
        ruta_destino = os.path.join(carpeta, archivo)

        
        shutil.move(ruta_origen, ruta_destino)
        print(f"{archivo} movido a {carpeta} ")

# Función para generar un nombre aleatorio de 8 letras
def generar_nombre_aleatorio(longitud=8):
    letras = string.ascii_letters  # Letras mayúsculas y minúsculas
    return ''.join(random.choice(letras) for _ in range(longitud))

def renombrar_archivos(carpeta):
    archivos = os.listdir(carpeta)
    for archivo in archivos:
        if archivo == "fotos" or archivo == "videos":
            pass
        
        else:
            # Obtener la extensión del archivo
            extension = os.path.splitext(archivo)[1]
            # ic(archivo)
            # Generar nombre aleatorio de 8 caracteres
            nuevo_archivo = f"{generar_nombre_aleatorio(8)}{extension}"
            
            # Ruta completa de los archivos
            ruta_actual = os.path.join(carpeta, archivo)
            nueva_ruta = os.path.join(carpeta, nuevo_archivo)
            
            # Renombrar el archivo
            os.rename(ruta_actual, nueva_ruta)

            print(f"{archivo} renombrado a {nuevo_archivo}")
# Ruta de la carpeta donde están los archivos

def ordenar_carpeta(carpeta):
    # Crear las carpetas para fotos y videos
    carpeta_fotos = os.path.join(carpeta, "fotos")
    carpeta_videos = os.path.join(carpeta, "videos")

    # Crear las carpetas si no existen
    os.makedirs(carpeta_fotos, exist_ok=True)
    os.makedirs(carpeta_videos, exist_ok=True)

    # Definir extensiones para fotos y videos
    extensiones_fotos = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
    extensiones_videos = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.m4v']

    # Listar todos los archivos de la carpeta
    archivos = os.listdir(carpeta)

    # Bucle para clasificar y mover los archivos
    for archivo in archivos:
        # Obtener la extensión del archivo
        extension = os.path.splitext(archivo)[1].lower()
        
        # Ruta completa del archivo
        ruta_actual = os.path.join(carpeta, archivo)
        # ic(os.path.join(carpeta_fotos,archivo ))
        # Verificar si es foto o video y mover a la carpeta correspondiente
        if extension in extensiones_fotos:
            shutil.move(ruta_actual, os.path.join(carpeta_fotos, archivo))
            print(f"{archivo} movido a la carpeta de fotos.")
        
        elif extension in extensiones_videos:
            shutil.move(ruta_actual, os.path.join(carpeta_videos, archivo))
            print(f"{archivo} movido a la carpeta de videos.")

def main(artista, carpeta_origen):
    carpeta_destino = f"E:/datos/{artista}"

    if carpeta_origen == "telegram":
        carpeta_telegram = "C:/Users/diego/Downloads/Telegram Desktop"
        renombrar_archivos(carpeta_telegram)
        crear_carpeta(carpeta_destino)
        mover_archivos(carpeta_telegram, carpeta_destino)
        ordenar_carpeta(carpeta_destino)

    elif carpeta_origen == "descargas":
        carpeta_descargas = f"E:/descargas/{artista}"
    
        renombrar_archivos(carpeta_descargas)
        crear_carpeta(carpeta_destino)
        mover_archivos(carpeta_descargas, carpeta_destino)
        ordenar_carpeta(carpeta_destino)

