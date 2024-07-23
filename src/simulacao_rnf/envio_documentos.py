import requests
import json
import time
import random

url = 'http://localhost:5000/api/verificar_alteracoes'

data = {
    "id": 1,
    "name": "Juan",
    "document": "As diretrizes de estilo do Python recomendam o uso de aspas simples para strings de texto simples",
    "date": "2021-01-01"
}

def send_data():
    while True:
        # sets random date to send to the server
        data['date'] = time.strftime('%Y-%m-%d %H:%M:%S')
        # random chance to change the document content
        if random.random() > 0.5:
            data['document'] = "As diretrizes de estilo do Python recomendam o uso de aspas simples para strings de texto simples, embora aspas duplas também sejam aceitáveis."
        else:
            data['document'] = "Javascript é melhor"
        response = requests.post(url, json=data)
        print(response.json())
        time.sleep(5)

if __name__ == '__main__':
    send_data()
