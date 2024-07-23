import unittest
import requests
import time

class TestDisponibilidade(unittest.TestCase):

    def test_tempo_resposta(self):
        url = "http://localhost:5001/"
        inicio = time.time()
        resposta = requests.get(url)
        fim = time.time()
        tempo_resposta = (fim - inicio) * 1000
        self.assertTrue(tempo_resposta < 3000, f"Tempo de resposta muito alto: {tempo_resposta} ms")

if __name__ == '__main__':
    unittest.main()
