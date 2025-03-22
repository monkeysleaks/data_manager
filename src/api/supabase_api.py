import os
from supabase import create_client, Client
from supabase.client import ClientOptions
from icecream import ic
import json
from dotenv import load_dotenv
import time

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(
    url, 
    key,
    options=ClientOptions(
        schema="official",
    )
)
def get_all_data(schema,tabla):
    response = (
        supabase.schema(schema).table(tabla)
        .select("*")
        .execute())
    return response.data

def get_data_eq(schema,tabla, artista_id):
    response = (
        supabase.schema(schema).table(tabla)
        .select("*")
        .eq("artista_id", artista_id)
        .execute())
    return response.data

def insert_data(schema, tabla,datos):
    response = (
    supabase.schema(schema).table(tabla)
    .insert(datos)
    .execute())
    print(response.data)
    return response.data

def update_data(artista, code_voe, title):
    response = (
    supabase.table(f"videos")
    .update({"code_voe": code_voe})
    .eq("title", title)
    .execute()
    )
    print(response.data)
    return response

def upsert_data(artista):
    response = (
    supabase.table(f"{artista}_videos")
    .upsert([{"id": 1, "nombre": "piano"}, {"id": 2, "nombre": "guitar"}])
    .execute())
    print(response.data)


def lista_carpeta():
    ruta = "E:/datos/"
    nombres = os.listdir(ruta)
    lista_nombres = []
    
    for nombre in nombres:

        if nombre != "Filemoon.csv":
            # Crear estructura de datos para cada elemento
            elemento = {"nombre": nombre}
            lista_nombres.append(elemento)
    
    return lista_nombres


def delete_data(tabla, fila, elemento):
    response = (
    supabase.table(tabla)
    .delete()
    .in_(fila, elemento)
    .execute())
    print(response)

def abrir_json(artista):
    path = f"C:/Users/diego/Desktop/Curso_Progamacion/backend_ML/backend/data/{artista}.json"
    informacion = []
    with open (path, "r") as file:
        datos = json.load(file)
        for dato in datos:
            info = {
        "title": f"{dato['title']}",
        "code_voe": f"{dato['code_voe']}",
        "code_filemoon": f"{dato['code_filemoon']}",
        "length": f"{dato['length']}",
        "file_size": f"{dato['file size']}",
        "img": f"{dato['img']}",
        "portal": "false"
        }
            informacion.append(info)
    return informacion


if __name__ == "__main__":
    artistas  = get_data_eq("official", "videos", 9) 
    for video in artistas:
        print(f"{video['title']}", video["code_voe"])




    
