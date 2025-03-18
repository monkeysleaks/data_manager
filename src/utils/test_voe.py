import os
import requests
import json
from dotenv import load_dotenv
from src.api import supabase_api as db
load_dotenv()


artistas = db.get_data("official", "artistas")

with open("fallas.md", "w") as file:
    file.write("")
    file.close()

for artista in artistas:
    artista_id = artista["artista_id"]
    data_videos = db.get_data_2_0("official", "videos", artista_id)
    for video in data_videos:
        # print(video["code_voe"])
        try:
            response = requests.get(f"https://voe.sx/{video['code_voe']}")
            if response.status_code != 200:
                with open("fallas.md", "a") as file:
                    file.write(f"artista: {artista}, title: {video['title']} code_voe: {video['code_voe']}\n")
                    file.close()
                print(f"falla en {video['code_voe']}")
            else:
                print(f"video {video['title']}, {video['code_voe']} es válido")
        except Exception as e:
            print(f"ocurrio un error: {e}")

