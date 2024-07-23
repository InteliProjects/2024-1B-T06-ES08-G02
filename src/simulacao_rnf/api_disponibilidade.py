from flask import Flask, request, jsonify
import threading
import time

app = Flask(__name__)

# Estado do servidor (0 - estável, 1 - instável)
estado_servidor = 0

# Simulação de bancos de dados replicados
banco_dados_1 = ["Dado 1", "Dado 2", "Dado 3"]
banco_dados_2 = banco_dados_1.copy()

@app.route('/api/informar_instabilidade', methods=['POST'])
def informar_instabilidade():
    global estado_servidor

    data = request.json
    if 'instavel' in data and data['instavel']:
        estado_servidor = 1
        iniciar_servidor_backup()

    return jsonify({'mensagem': 'Informações recebidas com sucesso.'}), 200

def iniciar_servidor_backup():
    # Simula a inicialização de um servidor de backup
    threading.Thread(target=simular_servidor_backup).start()

def simular_servidor_backup():
    global estado_servidor
    print("Iniciando servidor de backup...")
    time.sleep(5)  # Simulação de inicialização
    estado_servidor = 0
    print("Servidor de backup iniciado com sucesso.")

@app.route('/api/obter_dados_banco_1', methods=['GET'])
def obter_dados_banco_1():
    return jsonify({'dados': banco_dados_1}), 200

@app.route('/api/obter_dados_banco_2', methods=['GET'])
def obter_dados_banco_2():
    return jsonify({'dados': banco_dados_2}), 200

if __name__ == '__main__':
    app.run(debug=True)
