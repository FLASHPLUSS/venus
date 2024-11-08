from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# URL do arquivo JSON no Dropbox
dropbox_url = 'https://www.dropbox.com/scl/fi/bkdqz292n71jsr0e2588q/Venus.json?rlkey=eu6wno4weq9glll69la70sml2&st=jg6zln0t&dl=1'

def carregar_dados_json():
    try:
        # Fazer o download do arquivo JSON
        response = requests.get(dropbox_url)
        if response.status_code == 200:
            # Carregar o conteúdo JSON
            dados = json.loads(response.content)
            return dados
        else:
            return []
    except Exception as e:
        print(f"Erro ao carregar JSON: {e}")
        return []

@app.route('/api/venus', methods=['GET'])
def filmes_series():
    # Carregar dados do JSON do Dropbox
    data = carregar_dados_json()

    # Retornar todos os dados sem paginação
    return jsonify({
        'total': len(data),
        'data': data
    })

@app.route('/api/pesquisa', methods=['GET'])
def pesquisa():
    termo = request.args.get('termo', '').lower()
    data = carregar_dados_json()
    
    # Filtrar dados que contêm o termo de pesquisa no título
    resultados = [item for item in data if termo in item.get('titulo', '').lower()]

    # Retornar todos os resultados de uma vez (sem paginação)
    return jsonify({
        'termo': termo,
        'total': len(resultados),
        'data': resultados
    })

@app.route('/api/categoria', methods=['GET'])
def categoria():
    categoria = request.args.get('categoria', '').lower()
    data = carregar_dados_json()
    
    # Filtrar dados que correspondem à categoria especificada
    resultados = [item for item in data if categoria in item.get('categoria', '').lower()]

    # Retornar dados sem paginação
    return jsonify({
        'categoria': categoria,
        'total': len(resultados),
        'data': resultados
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
