from flask import Flask, jsonify
import time
import requests
import csv
from threading import Thread

app = Flask(__name__)

UPLOAD_SERVICE_URL = "http://localhost:5001"  


def medir_tempo_resposta():
    url = f"{UPLOAD_SERVICE_URL}/"
    inicio = time.time()
    resposta = requests.get(url)
    fim = time.time()
    tempo_resposta = (fim - inicio) * 1000  
    return tempo_resposta

def medir_tempo_processamento():
    url = f"{UPLOAD_SERVICE_URL}/upload"
    tempos_processamento = []

    for i in range(10):
        files = {'file': (f'test{i}.txt', 'conteudo do arquivo')}
        dados = {'password': 'senha'}

        inicio = time.time()
        resposta = requests.post(url, data=dados, files=files)
        fim = time.time()

        if resposta.status_code == 200:
            tempo_processamento = (fim - inicio) * 1000  
            tempos_processamento.append(tempo_processamento)
        else:
            tempos_processamento.append(None)
    
    return tempos_processamento

def verificar_senhas_criptografadas():
    url = f"{UPLOAD_SERVICE_URL}/files"
    resposta = requests.get(url)
    try:
        arquivos = resposta.json().get('files', [])
    except requests.exceptions.JSONDecodeError:
        return [{"name": "Desconhecido", "verificada": False}] * 10

    verificacoes = []

    for arquivo in arquivos:
        nome_arquivo = arquivo['name']
        url_senha = f"{UPLOAD_SERVICE_URL}/uploads/{nome_arquivo}"
        resposta_senha = requests.post(url_senha, data={'password': 'senha'})
        if resposta_senha.status_code == 200 and resposta_senha.content:
            verificacoes.append({"name": nome_arquivo, "verificada": True})
        else:
            verificacoes.append({"name": nome_arquivo, "verificada": False})

    return verificacoes


def coletar_dados_disponibilidade():
    with open('disponibilidade_dados.csv', 'w', newline='') as csvfile:
        fieldnames = ['dia', 'tempo_resposta']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for dia in range(1, 11):
            tempo_resposta = medir_tempo_resposta()
            writer.writerow({'dia': dia, 'tempo_resposta': tempo_resposta})
            time.sleep(1)

def coletar_dados_rastreabilidade():
    with open('rastreabilidade_dados.csv', 'w', newline='') as csvfile:
        fieldnames = ['dia', 'tempo_processamento']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        tempos_processamento = medir_tempo_processamento()
        for i, tempo in enumerate(tempos_processamento):
            writer.writerow({'dia': time.ctime(), 'tempo_processamento': tempo})
        time.sleep(1)

def coletar_dados_seguranca():
    with open('seguranca_dados.csv', 'w', newline='') as csvfile:
        fieldnames = ['dia', 'nome_arquivo', 'senha_criptografada']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        verificacoes = verificar_senhas_criptografadas()
        for verificada in verificacoes:
            writer.writerow({'dia': time.ctime(), 'nome_arquivo': verificada['name'], 'senha_criptografada': verificada['verificada']})
        time.sleep(1)

@app.route('/coletar_dados/<tipo>')
def coletar_dados(tipo):
    if tipo == 'disponibilidade':
        thread = Thread(target=coletar_dados_disponibilidade)
        thread.start()
    elif tipo == 'rastreabilidade':
        thread = Thread(target=coletar_dados_rastreabilidade)
        thread.start()
    elif tipo == 'seguranca':
        thread = Thread(target=coletar_dados_seguranca)
        thread.start()
    return jsonify({"status": "Coleta de dados iniciada para " + tipo})

if __name__ == '__main__':
    app.run(debug=True, port=5003)
