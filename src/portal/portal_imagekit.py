from imagekitio import ImageKit
import os
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
import time
from icecream import ic



# Configuración inicial de ImageKit portalnet
imagekit = ImageKit(
    private_key='private_ax18l5/nSkA/kQIb9nb/HkHih6k=',
    public_key='public_KKJN0r7QZ3Y3N2UYGIMs/NRzOlo=',
    url_endpoint='https://ik.imagekit.io/bhba8douv'
)


def crear_path(artista):
    #devuelve una lista en la que cada elemento, contiene el nombre del archivo y la extencion por separado [("nombre", ".ext")].
    lista = (os.listdir(f"E:/datos/{artista}/thumbnails_{artista}/"))

    lista_split = []
    for path in lista:
        split = os.path.splitext(path)
        lista_split.append(split)
        
    return lista_split

def subir_img(artista, lista_split):
    for nombre, ext in lista_split:
        file_path = f"E:/datos/{artista}/thumbnails_{artista}/{nombre}{ext}"

        response = imagekit.upload_file(
            file = open(file_path, "rb"),
            file_name = nombre,
            options=UploadFileRequestOptions(
            folder = artista,
            use_unique_file_name = False,
    )
        )
        print(f"{nombre}{ext}, subido")
        time.sleep(500/1000)


#----- programa principal -------
if __name__ == "__main__":
    
    artista = input("nombre artista: ")
    lista_split = crear_path(artista)
    
    subir_img(artista, lista_split)
    print(f"imgs {artista}, subido")