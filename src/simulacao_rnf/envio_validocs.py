import requests
import random
import string
import time
import hashlib
import hmac
import base64

# Chave secreta para assinatura digital (deve ser a mesma utilizada no servidor)
CHAVE_SECRETA = b'MinhaChaveSecreta123'

def gerar_documento():
    # Gera um documento aleatório
    documento = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return documento

def calcular_assinatura(documento, mac_address, usuario):
    # Concatena os dados do documento e a chave secreta
    mensagem = documento + mac_address + usuario
    # Calcula o HMAC (Hash-based Message Authentication Code) usando a chave secreta
    assinatura = hmac.new(CHAVE_SECRETA, mensagem.encode('utf-8'), hashlib.sha256).digest()
    # Codifica a assinatura em base64 para transmissão
    assinatura_base64 = base64.b64encode(assinatura).decode('utf-8')
    return assinatura_base64

def enviar_documento():
    while True:
        # Gera um documento aleatório
        documento = gerar_documento()

        # Simula o endereço MAC do dispositivo
        mac_address = ':'.join(['{:02x}'.format(random.randint(0, 255)) for _ in range(6)])

        # Simula o usuário
        usuario = f'usuario_{random.randint(1, 1000)}'

        # Calcula a assinatura digital do documento
        assinatura = calcular_assinatura(documento, mac_address, usuario)

        # Envia o documento com a assinatura para o módulo simulado
        data = {'documento': documento, 'mac_address': mac_address, 'usuario': usuario, 'assinatura': assinatura}
        response = requests.post('http://localhost:5000/api/receber_documento', json=data)
        print(response.json())

        time.sleep(5)  # Simulação de intervalo entre envios

if __name__ == '__main__':
    enviar_documento()
