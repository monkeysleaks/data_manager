import cv2
import random
import os
import numpy as np
import winsound



def generar_previsualizacion(video_path, salida, output_size=(350, 350)):
    """
    Genera una imagen con un único fotograma del video redimensionado,
    superpuesto sobre un fondo desenfocado del mismo fotograma.
    
    :param video_path: Ruta al archivo de video.
    :param salida: Ruta para guardar la imagen generada. """
    import cv2

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("No se pudo abrir el video.")
        return
    
    # Obtener duración del video en segundos
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    duracion = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / fps
    
    # Seleccionar el tiempo medio del video
    tiempo = duracion / 2
    cap.set(cv2.CAP_PROP_POS_MSEC, tiempo * 1000)  # Ir al tiempo específico
    
    success, frame = cap.read()
    cap.release()
    
    if not success:
        print(f"No se pudo capturar el fotograma. {video_path}")
        return

    # Dimensiones del fotograma original
    frame_height, frame_width = frame.shape[:2]
    aspect_ratio = frame_width / frame_height

    # Redimensionar el fotograma para el fondo desenfocado
    fondo_blur = cv2.resize(frame, output_size)
    fondo_blur = cv2.GaussianBlur(fondo_blur, (35, 35), 0)

    # Calcular las dimensiones del fotograma manteniendo el aspect ratio
    if frame_width > frame_height:
        new_width = output_size[0]
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = output_size[1]
        new_width = int(new_height * aspect_ratio)
    
    # Asegurarse de que el fotograma no exceda las dimensiones del fondo
    new_width = min(new_width, output_size[0])
    new_height = min(new_height, output_size[1])

    # Redimensionar el fotograma
    frame_resized = cv2.resize(frame, (new_width, new_height))

    # Calcular las posiciones para centrar el fotograma
    x_offset = (output_size[0] - new_width) // 2
    y_offset = (output_size[1] - new_height) // 2

    # Superponer el fotograma redimensionado en el centro del fondo desenfocado
    resultado = fondo_blur.copy()
    resultado[y_offset:y_offset+new_height, x_offset:x_offset+new_width] = frame_resized

    # Guardar la imagen en formato WebP
    cv2.imwrite(salida, resultado, [cv2.IMWRITE_WEBP_QUALITY, 90])
    print(f"Imagen generada guardada en {salida}")

def crear_carpeta(ruta,artista):
    carpeta_salida = os.mkdir(f"{ruta}thumbnails_monkeysleaks{artista}")
    return carpeta_salida

def separar_nombre_extencion(ruta):
    lista = os.listdir(ruta)
    lista_sin_ext = []
    for nombre in lista:
        nombre = os.path.splitext(nombre)
        lista_sin_ext.append(nombre)
    return lista_sin_ext

def crear_carpeta_thumb(lista_rutas):
      for artista in lista_rutas:
        comprobacion = os.path.isdir(f"E:/datos/{artista}/thumbnails_monkeysleaks{artista}")
        if comprobacion == True:
            # os.rmdir(f"E:/datos/{artista}/thumbnails_{artista}")
            print(f"la carpeta para {artista} ya existe")
        else: 
            ruta = f"E:/datos/{artista}/"
            crear_carpeta(ruta, artista)
            print(f"ruta para {artista} creada")


def main(artista):
    

    # declaracion de variables
    ruta_video = f"E:/datos/{artista}/videos/"
    ruta_salida = f"E:/datos/{artista}/thumbnails_monkeysleaks_{artista}/"

    #crear el objeto nombre y extencion
    lista_sin_ext = separar_nombre_extencion(ruta_video)

    #validar que la carpeta de salida existe
    if os.path.isdir(ruta_salida) == True:
        try:
            for nombre, extencion in lista_sin_ext:
                generar_previsualizacion(f"{ruta_video}{nombre}{extencion}", f"{ruta_salida}{nombre}.webp")
        except Exception as e:
            print(f"Error: {e}")
            print(f"falla if en:{ruta_video}{nombre}{extencion}")
    else:
        try:
            os.mkdir(f"E:/datos/{artista}/thumbnails_monkeysleaks_{artista}")
            for nombre, extencion in lista_sin_ext:
                generar_previsualizacion(f"{ruta_video}{nombre}{extencion}", f"{ruta_salida}{nombre}.webp")
        except Exception as e:
            print(f"Error: {e}")
            print(f"falla else en:{ruta_video}{nombre}{extencion}")
    
    print(f"prev creadas para {artista}")
    ruta_sonido = "C:/Users/diego/Desktop/windows-notify.wav"
    winsound.PlaySound(ruta_sonido, winsound.SND_FILENAME) 
        
    
    
    