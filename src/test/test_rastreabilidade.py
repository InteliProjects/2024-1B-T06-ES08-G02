import unittest
import requests
import time

class TestRastreabilidade(unittest.TestCase):

    def test_tempo_processamento(self):
        url = "http://localhost:5001/upload"
        dados = {'password': 'senha'}
        for i in range(10):
            with self.subTest(i=i):
                files = {'file': (f'test{i}.txt', 'conteudo do arquivo')}
                inicio = time.time()
                resposta = requests.post(url, data=dados, files=files)
                fim = time.time()
                self.assertEqual(resposta.status_code, 200, "Falha no upload")
                tempo_processamento = (fim - inicio) * 1000
                self.assertTrue(tempo_processamento < 5000, f"Tempo de processamento muito alto: {tempo_processamento} ms")

if __name__ == '__main__':
    unittest.main()
