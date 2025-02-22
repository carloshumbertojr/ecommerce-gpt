import os
import json
import time
import requests

# URL do endpoint para onde as requisições serão enviadas
url = "http://localhost:8000/api/v1/questions"  # Substitua pela URL do seu endpoint

# Cabeçalhos da requisição, se necessário
headers = {
    "Content-Type": "application/json",
    # "Authorization": "Bearer seu_token_aqui",  # Se o endpoint requer autenticação
}


# Caminho absoluto para o arquivo de perguntas
caminho_arquivo = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "dataset_completo.json")
)
# Leitura do arquivo JSON
with open(f"{caminho_arquivo}", "r", encoding="utf-8") as arquivo:
    dados = json.load(arquivo)

# Iteração sobre cada objeto no array original e envio individual
for item in dados:
    # Extração das propriedades desejadas

    ######################################################################################## HERE
    # Chamada da api, no endpoint /api/v1/answer
    # para cada item, para montar o objeto que vai calcular e armazenar as respostas

    # FORMATAR O `dataset.json` com os dados de contexto e respostas humanas,
    ########################################################################################

    description_context: str = f"Titulo do anúncio: {item.get('item_title')} | Descrição do anúncio: {item.get('item_description')} | Ficha técnica: {item.get('item_ficha_tenica')}"

    novo_item = {
        "ml_product_id": item.get("item_id"),
        "question": item.get("text"),
        "description": description_context,
        "human_answer": item.get("resposta_humano"),
    }

    # Envio da requisição POST com o objeto individual
    try:
        response = requests.post(url, headers=headers, json=novo_item)

        # Verificação da resposta
        if response.status_code == 200:
            print(f"Objeto {novo_item['ml_product_id']} enviado com sucesso!")
        else:
            print(
                f"Falha ao enviar o objeto {novo_item['ml_product_id']}. Status: {response.status_code}, Resposta: {response.text}"
            )
    except Exception as e:
        print(f"Erro ao enviar o objeto {novo_item['ml_product_id']}: {e}")

    # Delay entre as requisições
    # Aguarda 10 segundo antes de enviar o próximo
    # 10 para local (Llama, Qwen)
    # 2 para cloud (gpt-4o, Claude)
    time.sleep(10)
