from flask import Flask, request, jsonify
import hashlib
import hmac
import base64

app = Flask(__name__)

# Chave secreta para assinatura digital (deve ser mantida em segredo)
CHAVE_SECRETA = b'MinhaChaveSecreta123'

@app.route('/api/receber_documento', methods=['POST'])
def receber_documento():
    data = request.json
    documento = data.get('documento')
    mac_address = data.get('mac_address')
    usuario = data.get('usuario')
    assinatura = data.get('assinatura')  # Assinatura digital enviada junto com o documento

    # Verificação de autenticidade
    if documento and mac_address and usuario and assinatura:
        # Verifica a autenticidade da assinatura digital
        assinatura_calculada = calcular_assinatura(documento, mac_address, usuario)
        if assinatura_calculada == assinatura:
            # Assinatura válida, processa o documento
            print(f"Documento recebido: {documento}")
            print(f"MAC Address: {mac_address}")
            print(f"Usuário: {usuario}")

            # Simulação de resposta
            return jsonify({'mensagem': 'Documento recebido com sucesso.',
                            'validacao': True}), 200
        else:
            return jsonify({'erro': 'Assinatura inválida.',
                            'validacao': False}), 401
    else:
        return jsonify({'erro': 'Dados incompletos.',
                        'validacao': False}), 400

def calcular_assinatura(documento, mac_address, usuario):
    # Concatena os dados do documento e a chave secreta
    mensagem = documento + mac_address + usuario
    # Calcula o HMAC (Hash-based Message Authentication Code) usando a chave secreta
    assinatura = hmac.new(CHAVE_SECRETA, mensagem.encode('utf-8'), hashlib.sha256).digest()
    # Codifica a assinatura em base64 para transmissão
    assinatura_base64 = base64.b64encode(assinatura).decode('utf-8')
    return assinatura_base64

if __name__ == '__main__':
    app.run(debug=True)
