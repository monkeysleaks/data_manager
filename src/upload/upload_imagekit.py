from imagekitio import ImageKit
import os
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
import time


# SDK initialization monkeysleaks
imagekit = ImageKit(
    private_key='private_xzSpP2hIJhV1p+a54D7mXuo37a8=',
    public_key='public_hRedibb12KEag2Uv0Noz6X8amYs=',
    url_endpoint='https://ik.imagekit.io/b2o3nmna5'
)

def crear_path(artista):
    #devuelve una lista en la que cada elemento, contiene el nombre del archivo y la extencion por separado [("nombre", ".ext")].
    lista = (os.listdir(f"E:/datos/{artista}/thumbnails_monkeysleaks_{artista}/"))

    lista_split = []
    for path in lista:
        split = os.path.splitext(path)
        lista_split.append(split)
        
    return lista_split

def subir_img(artista, lista_split):
    for nombre, ext in lista_split:
        file_path = f"E:/datos/{artista}/thumbnails_monkeysleaks_{artista}/{nombre}{ext}"

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
def main(artista):
    import winsound
    ruta_sonido = "C:/Users/diego/Desktop/windows-notify.wav"

    lista_split = crear_path(artista)
    
    subir_img(artista, lista_split)
    print(f"imgs {artista}, subido")
    winsound.PlaySound(ruta_sonido, winsound.SND_FILENAME) 