import requests
import json
import os
from icecream import ic
from dotenv import load_dotenv  
load_dotenv()

token_filemoon = os.environ.get('API_KEY_FILEMOON')

def get_info_account(token_filemoon):
    url = f"https://filemoonapi.com/api/account/info?key={token_filemoon}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json() # recibe los datos en formato json
        return data
    else:
        print(response)

def get_folders_filemoon(token_filemoon):
    url = f"https://filemoonapi.com/api/folder/list?key={token_filemoon}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json() # recibe los datos en formato json
        return data["result"]["folders"]
    else:
        print(response)

def get_data_folder_filemoon(artista): 
    token_filemoon = os.environ.get('API_KEY_FILEMOON')
    folders = get_folders_filemoon(token_filemoon)
    for folder in folders:
        if folder["name"] == artista:
            folder_id = folder["fld_id"]
            break
    url  = f"https://filemoonapi.com/api/file/list?key={token_filemoon}&page=1&per_page=1000&fld_id={folder_id}"
    response  = requests.get(url)
    if response.status_code == 200:
        data = response.json() # recibe los datos en formato json
        return data["result"]["files"]
    else:
        print(response)

def move_folder_filemoon(token_filemoon, filecode, folder_id_destino):
    url = f"https://filemoonapi.com/api/file/clone?key={token_filemoon}&file_code={filecode}&fld_id={folder_id_destino}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json() # recibe los datos en formato json
        print(data)
    else:
        print(response)
    
def delete_file_filemoon(token_filemoon, filecode):
    url = f"https://filemoonapi.com/api/file/move?key={token_filemoon}&file_code={filecode}&fld_id="  
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json() # recibe los datos en formato json
        print(data)
    else:
        print(response)

if __name__ == "__main__":
    artista = "sopaipaposting"
    title = "QySaEJSB.m4v"
    filecode = "57lkveuzuy98"
    delete_file_filemoon(token_filemoon, filecode)
    