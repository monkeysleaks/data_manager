from src.upload.uploader_voe import Voe
from src.upload import uploader_filemoon as filemoon
from dotenv import load_dotenv
from icecream import ic
import os
load_dotenv()


def main():
    try:

        token_voe = os.environ.get('API_KEY_VOE')
        token_filemoon = os.environ.get('API_KEY_FILEMOON')

        while True:
            print('''1.- Subir voe
2.- Subir filemoon
3.- Agregar Datos a la DB
4.- Actualizar Datos a la DB
5.- Crear Previews
6.- Subir Previews
7.- Rebuild Cloudflare
8.- Salir''')
            
            opcion = int(input("ingrese opcion (1-7): "))
            
            if opcion == 1:

                while True:
                    print('''
        1.- Carpeta Existente
        2.- Nueva Carpeta
        3.- Volver Atrás''')   
                    subopcion1 = int(input("ingrese opcion (1-2): "))

                    if subopcion1 == 1:
                        artista = input("ingrese artista: ")
                        Voe.main_upload_voe(artista)
                    elif subopcion1 == 2:
                        artista = input("ingrese artista: ")
                        Voe.create_folder(token_voe, artista)
                        Voe.main_upload_voe(artista)
                    elif subopcion1 == 3:
                        break
           
            elif opcion == 2:
                while True:
                    print('''
    1.- Nuevos archivos
    2.- resubir Archivos (raro?)
    3.- Volver Atrás
 ''')           
                    subopcion2 = int(input("ingrese opción (1-3): "))
                    if subopcion2 == 1:
                        artista = input("ingrese artista: ")
                        filemoon.create_folder(token_filemoon, artista)
                        # filemoon.main_upload_filemoon(artista)

                    elif subopcion2 == 2:
                        artista = input("ingrese artista: ")
                        pass

                    elif subopcion2 == 3:
                        break

            elif opcion == 3:
                #agregar nuevos datos a la db
                pass

            elif opcion == 8:

                ic("saludos Que Tengas buen día")
                break
            

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()