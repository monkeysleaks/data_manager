import requests
import json
import os
from dotenv import load_dotenv
from icecream import ic

load_dotenv()

class Voe:
    # Constructor
    def __init__(self, token):
        self.token = token


    # Métodos
    def get_folders(token): 
        url = f"https://voe.sx/api/folder/list?key={token}&fld_id=0"
        response = requests.get(url)
        data = response.json()
        return data["result"]["folders"]

    def get_data_folder(api_key_voe, folder_id_voe):
        url = f"https://voe.sx/api/file/list?key={api_key_voe}&page=1&per_page=250&fld_id={folder_id_voe}"
        response = requests.get(url) 
        if response.status_code == 200:
            data = response.json() # recibe los datos en formato json
            # dar formato al json
            formatted_json = json.dumps(data, indent=2, ensure_ascii=False)
            result = data["result"]
            datos = result["data"]
            return datos
    
    def move_folder(token, folder_id_destino):
        url = f"https://voe.sx/api/file/set_folder?key={token}&file_code=&fld_id={folder_id_destino}"
        response = requests.get(url)
        data = response.json()
        return data["result"]["file_code"]

    def get_balance(token):      
        url = f"https://voe.sx/api/account/info?key={token}"
        response = requests.get(url)
        data = response.json()
        #  print(data)
        return data["result"]["balance"]
    
    def create_folder(token, folder_name):
        url = f"https://voe.sx/api/folder/create?key={token}&parent_id=0&name={folder_name}"
        response = requests.get(url)
        data = response.json()
        fld_id = data["result"] 
        print(fld_id)
        return fld_id
       

if __name__ == "__main__":
    token = os.environ.get('API_KEY_VOE')
    Voe.create_folder(token, "test1")

     

