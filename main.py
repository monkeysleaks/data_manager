from src.upload.uploader_voe import Voe
from dotenv import load_dotenv
from icecream import ic
import os
load_dotenv()


def main():
    try:

        token_voe = os.environ.get('API_KEY_VOE')

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
1.- nuevos archivos
2.- archivos 
 ''')
            elif opcion == 8:
                break
            

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()