import requests
import time
import random

def simular_envio_informacoes():
    while True:
        # Simulação de instabilidade no servidor
        status = random.choice([True, False])
        print(f"Instável: {status}")
        data = {'instavel': status}
        requests.post('http://localhost:5000/api/informar_instabilidade', json=data)
        print("Informações de instabilidade enviadas.")
        time.sleep(10)  # Simulação de intervalo entre envios

if __name__ == '__main__':
    simular_envio_informacoes()
