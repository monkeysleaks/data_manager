from src.upload.uploader_voe import Voe
from src.upload import uploader_filemoon as filemoon
from src.database import update_data
from src.database import add_data 
from src.utils import rebuild
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
    7.- Salir''')
                
                opcion = int(input("ingrese opcion (1-7): "))
                
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
                            # filemoon.main_upload_filemoon(artista)

                        elif subopcion2 == 2:
                            artista = input("ingrese artista: ")
                            pass

                        elif subopcion2 == 3:
                            break
                
                #opcion 3 agregar nuevos datos a la db sin función por ahora
                elif opcion == 3:
                    #agregar un método, para actualizar el archivo js buscador en el frontend, cuando se agregan nuevos datos
                    artista = input("ingrese artista: ")
                    folders_voe = Voe.get_folders(token_voe)
                    for folder in folders_voe:
                        if folder["name"] == artista:
                            fld_voe = folder["fld_id"]
                            break
                    
                    add_data.main(artista, fld_voe)
                    ic(f"Datos agregados de {artista} a la db")

                #opcion 4 actualizar datos de una determinada artista
                elif opcion == 4:
                    ic("--- Actualizar Datos ---")
                    print('''
            1.- Actualizar Base de Datos
            2.- Volver Atrás
''')
                    while True:
                        subopcion4 = int(input("ingrese opción (1-2): "))
                        if subopcion4 == 1:
                            artista = input("ingrese artista: ")
                            update_data.main(artista)
                        elif subopcion4 == 2:
                            break

                #opcion 5 crear y subir las previews sin funcionar aun
                elif opcion == 5:
                    #crear las previews, hay que mejorar la calidad de la salida
                    pass
                
                # rebuild de proyecto en cloudflare
                elif opcion == 6:
                    ic("---- hacer la rebuild en clouflare ----")
                    print('''
            1.- Hacer Rebuild
            2.- Volver Atrás
                    ''')
                    subopcion6 = int(input("ingrese opción (1-2): "))
                    while True:
                        if subopcion6 == 1:
                            rebuild.main()
                        elif subopcion6 == 2:
                            break
                
                #salir
                elif opcion == 7:

                    ic("Saludos Que Tengas Buen día")
                    break
            

            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()