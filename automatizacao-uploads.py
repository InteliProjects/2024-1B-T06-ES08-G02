import os
import requests
import random
import time


API_UPLOAD_URL = 'http://127.0.0.1:5001/upload'  
FOLDER_PATH = 'src/ecm_backend/uploads'  
NUM_UPLOADS = 50  
FILES_PER_UPLOAD = 10  


if not os.path.exists(FOLDER_PATH):
    raise ValueError(f'A pasta {FOLDER_PATH} não existe.')


all_files = [os.path.join(FOLDER_PATH, f) for f in os.listdir(FOLDER_PATH) if os.path.isfile(os.path.join(FOLDER_PATH, f))]

if len(all_files) < FILES_PER_UPLOAD:
    raise ValueError(f'Não há arquivos suficientes na pasta {FOLDER_PATH}. Mínimo necessário: {FILES_PER_UPLOAD}.')


def upload_files(files):
    for file_path in files:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            dados = {'password': 'senha'}
            response = requests.post(API_UPLOAD_URL, files=files, data=dados)
            if response.status_code == 200:
                print(f'Sucesso: {file_path} -> {response.json()}')
            else:
                print(f'Erro: {file_path} -> {response.status_code}')


for i in range(NUM_UPLOADS):
    files_to_upload = random.sample(all_files, FILES_PER_UPLOAD)
    print(f'Upload {i+1}/{NUM_UPLOADS}: {files_to_upload}')
    upload_files(files_to_upload)
    time.sleep(random.uniform(0.5, 2.0))  
