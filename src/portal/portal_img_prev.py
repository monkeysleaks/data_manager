import cv2
import random
import os
import numpy as np


def generar_previsualizacion(video_path, salida, output_size=(350, 350)):

    """
    Genera una previsualización con un fondo desenfocado y tres fotogramas seleccionados en orden cronológico.
    
    :param video_path: Ruta al archivo de video.
    :param salida: Ruta para guardar la imagen de previsualización.
    :param output_size: Tamaño de la imagen de salida (ancho, alto).
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("No se pudo abrir el video.")
        return
    
    # Obtener duración del video en segundos
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    duracion = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / fps
    
    # Seleccionar 3 tiempos equidistantes en el video
    tiempos = [duracion * i / 4 for i in range(1, 4)]  # Dividir el video en 4 partes y tomar 3 puntos
    fotogramas = []
    
    for tiempo in tiempos:
        cap.set(cv2.CAP_PROP_POS_MSEC, tiempo * 1000)  # Ir al tiempo específico
        success, frame = cap.read()
        if success:
            fotogramas.append(frame)
    
    cap.release()
    
    if len(fotogramas) < 3:
        print(f"No se pudieron capturar suficientes fotogramas. {video_path}")
        return
    
    # Redimensionar el primer fotograma al tamaño de salida para usarlo como fondo
    fondo_blur = cv2.resize(fotogramas[0], output_size)
    fondo_blur = cv2.GaussianBlur(fondo_blur, (35, 35), 0)

    # Crear el resultado final basado en el fondo desenfocado
    resultado = fondo_blur.copy()

    # Calcular las dimensiones de cada fotograma redimensionado
    frame_height, frame_width = fotogramas[0].shape[:2]
    aspect_ratio = frame_width / frame_height
    max_width = output_size[0] * 0.33  # Cada fotograma ocupa el 30% del ancho
    new_width = int(max_width)
    new_height = 230 # alto del frame puesto a mano

    # Asegurarse de que no excedan el tamaño del fondo
    new_width = min(new_width, output_size[0])
    new_height = min(new_height, output_size[1])

    # Calcular las posiciones para alinear los tres fotogramas centrados
    spacing = 0  # Espaciado entre fotogramas
    total_width = 3 * new_width + 2 * spacing  # Ancho total de los tres fotogramas con espaciado
    x_start = (output_size[0] - total_width) // 2  # Coordenada x inicial para centrar
    y_center = (output_size[1] - new_height) // 2  # Coordenada y para centrar verticalmente

    for i, frame in enumerate(fotogramas):
        frame_resized = cv2.resize(frame, (new_width, new_height))
        x_offset = x_start + i * (new_width + spacing)
        
        # Superponer cada fotograma redimensionado en la posición calculada
        resultado[y_center:y_center+new_height, x_offset:x_offset+new_width] = frame_resized

    # Guardar la imagen en formato WebP
    cv2.imwrite(salida, resultado, [cv2.IMWRITE_WEBP_QUALITY, 90])
    print(f"Imagen de previsualización guardada en {salida}")

def crear_carpeta(ruta,artista):
    carpeta_salida = os.mkdir(f"{ruta}thumbnails_{artista}")
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
        comprobacion = os.path.isdir(f"E:/datos/{artista}/thumbnails_{artista}")
        if comprobacion == True:
            # os.rmdir(f"E:/datos/{artista}/thumbnails_{artista}")
            print(f"la carpeta para {artista} ya existe")
        else: 
            ruta = f"E:/datos/{artista}/"
            crear_carpeta(ruta, artista)
            print(f"ruta para {artista} creada")


if __name__ == "__main__":
    # declaracion de variables
    artista = input("nombre artista: ")
    ruta_video = f"E:/datos/{artista}/videos/"
    ruta_salida = f"E:/datos/{artista}/thumbnails_{artista}/"

    #crear el objeto nombre y extencion
    lista_sin_ext = separar_nombre_extencion(ruta_video)

    #validar que la carpeta de salida existe
    if os.path.isdir(ruta_salida) == True:
        for nombre, extencion in lista_sin_ext:
            generar_previsualizacion(f"{ruta_video}{nombre}{extencion}", f"{ruta_salida}{nombre}.webp")
    else:
        os.mkdir(f"E:/datos/{artista}/thumbnails_{artista}")
        for nombre, extencion in lista_sin_ext:
            generar_previsualizacion(f"{ruta_video}{nombre}{extencion}", f"{ruta_salida}{nombre}.webp")
    
    print(f"prev creadas para {artista}")
        
    
    
    