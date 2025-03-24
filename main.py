from src.upload.uploader_voe import Voe
from src.upload import uploader_filemoon as filemoon
from src.database import update_data
from src.database import add_data 
from src.utils import rebuild
from src.utils import ordenar_carpeta as order
from src.utils import prev_img
from src.upload import upload_imagekit as imagekit
from dotenv import load_dotenv
from icecream import ic
import os
load_dotenv()


def main():

        token_voe = os.environ.get('API_KEY_VOE')
        token_filemoon = os.environ.get('API_KEY_FILEMOON')

        while True:
            try:
                print('''
    1.- Subir voe
    2.- Subir filemoon
    3.- Agregar Datos a la DB
    4.- Actualizar Datos a la DB
    5.- Crear Previews y Subir Previews a Imagekit 
    6.- Rebuild Cloudflare
    7.- Ordenar carpeta
    8.- Salir''')
                
                opcion = int(input("ingrese opcion (1-8): "))
                
                #opcion 1 subir archivos a voe
                if opcion == 1:
                    ic("--- Subir Archivos a Voe")  
                    while True:
                        print('''
            1.- Carpeta Existente
            2.- Nueva Carpeta
            3.- Volver Atrás
                            ''')   
                        subopcion1 = int(input("ingrese opcion (1-3): "))

                        if subopcion1 == 1:
                            artista = input("ingrese artista: ")
                            Voe.main_upload_voe(artista)
                            ic(f"{artista} subido a voe")
                            opcionde_bd = input("actualizar db? 1-si 2-no: ")
                            if opcionde_bd == "1":
                                update_data.main(artista)
                                ic(f"DB actualizada {artista}")
                            elif opcionde_bd == "2":
                                break
                        elif subopcion1 == 2:
                            artista = input("ingrese artista: ")
                            Voe.create_folder(token_voe, artista)
                            ic(f"carpeta {artista} creada")
                            Voe.main_upload_voe(artista)
                            ic(f"{artista} subido a voe")
                        elif subopcion1 == 3:
                            break
            
                #opcion 2 subir archivos a filemoon
                elif opcion == 2:
                    ic("--- Subir Archivos a Filemoon ---")
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
                            filemoon.main_upload_filemoon(artista)

                        elif subopcion2 == 2:
                            artista = input("ingrese artista: ")
                            filemoon.main_upload_filemoon(artista)

                        elif subopcion2 == 3:
                            break
                
                #opcion 3 agregar nuevos datos a la db sin función por ahora
                elif opcion == 3:
                    while True:
                        ic("--- Agregar Datos a la DB ---")
                        print('''
            1.- Agregar Datos a la DB
            2.- Volver Atrás
''')
                        subopcion3 = int(input("ingrese opción (1-2): "))
                        if subopcion3 == 1:
                            artista_agregar = input("ingrese artista: ")
                            folders_voe = Voe.get_folders(token_voe)
                            for folder in folders_voe:
                                if folder["name"] == artista_agregar:
                                    fld_voe = folder["fld_id"]
                                    break
                            add_data.main(artista_agregar, fld_voe)
                            ic(f"Datos agregados de {artista_agregar} a la db")
                        elif subopcion3 == 2:
                            break
                    #agregar un método, para actualizar el archivo js buscador en el frontend, cuando se agregan nuevos 

                #opcion 4 actualizar datos de una determinada artista
                elif opcion == 4:
                    
                    while True:
                        ic("--- Actualizar Datos ---")
                        print('''
            1.- Actualizar Base de Datos
            2.- Volver Atrás
''')
                        subopcion4 = int(input("ingrese opción (1-2): "))
                        if subopcion4 == 1:
                            artista = input("ingrese artista: ")
                            update_data.main(artista)
                            ic(f"--- Datos actualizados para {artista} ---")
                        elif subopcion4 == 2:
                            break

                #opcion 5 crear y subir las previews 
                elif opcion == 5:
                    #crear las previews, hay que mejorar la calidad de la salida
                    while True:
                        ic("--- Crear Previews ---")
                        print('''
            1.- Crear Previews
            2.- upload imagekit
            3.- Volver Atrás
''')
                        subopcion5 = int(input("ingrese opción (1-2): "))
                        if subopcion5 == 1:
                            artista = input("ingrese artista: ")
                            prev_img.main(artista)
                            print("previews creados")
                            print("subir a imagekit? 1-si 2-no")
                            opcion_imgkit = int(input("ingrese opcion (1-2): "))
                            if opcion_imgkit == 1:
                                imagekit.main(artista)
                                print("subido a imagekit")
                            elif opcion_imgkit == 2:
                                pass
                        elif subopcion5 == 2:
                            artista = input("ingrese artista: ")
                            imagekit.main(artista)
                        elif subopcion5 == 3:
                            break
                
                # rebuild de proyecto en cloudflare
                elif opcion == 6:
                    
                    while True:
                        ic("---- hacer la rebuild en clouflare ----")
                        print('''
            1.- Hacer Rebuild
            2.- Volver Atrás
                    ''')
                        subopcion6 = int(input("ingrese opción (1-2): "))
                        if subopcion6 == 1:
                            rebuild.main()
                        elif subopcion6 == 2:
                            break
                
                #ordenar carpeta
                elif opcion == 7:
                    while True:
                        ic("---- ordenar carpeta ----")
                        print('''
            1.- Telegram
            2.- Descargas
            3.- Volver Atrás
''')
                        subopcion7 = int(input("ingrese la carpeta de origen (1-3): "))
                        if subopcion7 == 1:
                            artista = input("ingrese artista: ")
                            order.main(artista, "telegram")
                        elif subopcion7 == 2:
                            artista = input("ingrese artista: ")
                            order.main(artista, "descargas")
                        elif subopcion7 == 3:
                            break
                #salir
                elif opcion == 8:

                    ic("Saludos Que Tengas Buen día")
                    break
            

            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()