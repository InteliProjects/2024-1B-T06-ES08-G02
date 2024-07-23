from flask import Flask, request, jsonify

app = Flask(__name__)

documentos = []
alteracoes = []

@app.route('/api/verificar_alteracoes', methods=['POST'])
def verificar_alteracoes():
    novo_documento = request.json
    documentos.append(novo_documento)
    print(novo_documento)
    # Verifica se houve alguma alteração
    if len(documentos) < 1:
        elemento_alterado = "Novo documento"
        data_alteracao = documentos[-1]['date']
        alteracoes.append({'elemento_alterado': elemento_alterado, 'data_alteracao': data_alteracao})
    elif len(documentos) > 1 and documentos[-1]['document'] != documentos[-2]['document']:
        elemento_alterado = 'documento'
        data_alteracao = documentos[-1]['date']
        alteracoes.append({'elemento_alterado': elemento_alterado, 'data_alteracao': data_alteracao})
    else:
        elemento_alterado = 'nenhum'
        data_alteracao = 'nenhuma'  
        alteracoes.append({'elemento_alterado': elemento_alterado, 'data_alteracao': data_alteracao})
    
    return jsonify({'mensagem': 'Documento recebido com sucesso.', 'elemento_alterado': elemento_alterado, 'data_alteracao': data_alteracao}), 200

if __name__ == '__main__':
    app.run(debug=True)
