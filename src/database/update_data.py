#actualizar datos existentes, habitualmente de voe
from src.api import supabase_api as db
import os
from icecream import ic
from src.api.voe import Voe
from dotenv import load_dotenv
load_dotenv()


def actualizar_datos(artista, code_voe, title):
    response = (
    db.update_data(artista, code_voe, title)
    )
    print(response.data)
    return response

def main(artista):
    token_voe = os.environ.get('API_KEY_VOE')
    folders = Voe.get_folders(token_voe)  
    for folder in folders:
        if folder["name"] == artista:
            folder_id_voe = folder["fld_id"]
            print(folder_id_voe)
            break

    data_videos =Voe.get_data_folder(token_voe, folder_id_voe)
    # print(data_videos)
    for video in data_videos:
        code_voe = video["filecode"]
        title = video["title"]
        db.update_data(artista, code_voe, title)

if __name__ == "__main__":
    main("alitaaa")
