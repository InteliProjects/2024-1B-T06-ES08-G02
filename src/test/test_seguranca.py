import unittest
import requests

class TestSeguranca(unittest.TestCase):

    def test_senhas_criptografadas(self):
        url_files = "http://localhost:5001/files"
        resposta = requests.get(url_files)
        arquivos = resposta.json().get('files', [])
        
        for arquivo in arquivos:
            with self.subTest(file=arquivo['name']):
                url_senha = f"http://localhost:5001/uploads/{arquivo['name']}"
                resposta_senha = requests.post(url_senha, data={'password': 'senha'})
                self.assertEqual(resposta_senha.status_code, 200, "Falha na verificação da senha")
                self.assertTrue(resposta_senha.content, "Senha não criptografada")

if __name__ == '__main__':
    unittest.main()
