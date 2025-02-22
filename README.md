# ML Answers Assist

## Visão Geral

O **ML Answers Assist** é um sistema baseado em Inteligência Artificial e Processamento de Linguagem Natural (NLP) que automatiza respostas para perguntas no **Mercado Livre**. Com o crescente volume de interações nos marketplaces, esta solução busca reduzir o tempo de resposta e melhorar a experiência do consumidor ao fornecer respostas automáticas e precisas.

## Configuração Inicial

### Criando o arquivo de configuração

1. Crie um arquivo `.env` na raiz do projeto e adicione a seguinte base de configuração:

```ini
# Domain
# This would be set to the production domain with an env var on deployment
DOMAIN=localhost

# Configure these with your own Docker registry images
DOCKER_IMAGE_BACKEND=backend
DOCKER_IMAGE_FRONTEND=frontend

# Environment: local, staging, production
ENVIRONMENT=local

PROJECT_NAME="Answers ML Assistent"
STACK_NAME=answers-ml-assistent
VERSION="1.0.0"

# Backend
BACKEND_CORS_ORIGINS="http://localhost,http://localhost:8000,http://localhost:9090,http://localhost:5173,https://localhost,https://localhost:5173"
API_V1_STR="/api/v1"
API_V2_STR="/api/v2"

# External Conections
OPEN_AI_API_KEY=
BASE_ML_API_URL=
CHAT_API_KEY=http://host.docker.internal:8080

# Nome do modelo
# BASE_NAME_CHAT_MODEL="gpt-4o-mini"
BASE_NAME_CHAT_MODEL="Qwen2.5-0.5B-Instruct-Q5_K_M.gguf"
# BASE_NAME_CHAT_MODEL="Llama-3.2-1B-Instruct-Q5_K_M.gguf"
# BASE_NAME_CHAT_MODEL="TinyLlama-1.1B-Chat-v1.0-Q4_K_M.gguf"

# Similaridade para as questões parecidas
SIMILARITY_THRESHOLD=0.5

# Postgres
POSTGRES_SERVER=	# Nome do servidor postgres (não é usado, mas é necessário)
POSTGRES_PORT=		# Porta do servidor postgres
POSTGRES_DB=		# Nome do banco de dados a ser usado
POSTGRES_USER=		# Nome do usuário
POSTGRES_PASSWORD=	# Senha do usuário
```

2. Configure os dados do banco de dados no arquivo `.env`.

3. Defina o mesmo modelo no arquivo `model.Dockerfile` (responsável por baixar e configurar o modelo escolhido).

### Escolhendo um Modelo de IA

Os seguintes modelos estão disponíveis:

-   [GPT-4o Mini (pago)](https://platform.openai.com/api-keys)
-   [Qwen2.5-0.5B-Instruct](https://huggingface.co/second-state/Qwen2.5-0.5B-Instruct-GGUF/resolve/main/Qwen2.5-0.5B-Instruct-Q5_K_M.gguf)
-   [Llama-3.2-1B-Instruct](https://huggingface.co/second-state/Llama-3.2-1B-Instruct-GGUF/resolve/main/Llama-3.2-1B-Instruct-Q4_K_M.gguf)
-   [TinyLlama-1.1B-Chat-v1.0](https://huggingface.co/second-state/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/TinyLlama-1.1B-Chat-v1.0-Q4_K_M.gguf)

Para mais modelos, acesse [Hugging Face](https://huggingface.co/second-state) e siga os passos:

1. Navegue até a seção **Models**
2. Escolha um modelo de chat
3. Acesse a seção **Quantized GGUF Models**

Se desejar usar o ChatGPT, insira sua chave da API no `.env`:

```ini
open_ai_api_key=<sua-chave-aqui>
```

## Execução do Projeto

Na pasta raiz do projeto, execute o seguinte comando para iniciar o ambiente com Docker:

```sh
docker compose -f 'docker-compose.yaml' up -d --build
```

## Uso da API

Com o ambiente rodando, a API estará disponível na porta `8000`.

### Endpoint principal

Para obter respostas automáticas, utilize o endpoint:

**POST** `http://localhost:8000/api/v1/answer`

**Corpo da requisição (`JSON`)**:

```json
{
	"title": "Quantos Megapixels tem a câmera?",
	"description": "Câmera com IA e vídeos em 4K: Tire fotos mesmo em ambientes com pouca luz usando a câmera de 50 MP com IA do novo celular moto g35 5G.\nVocê também pode gravar vídeos supernítidos em 4K e tirar selfies de milhões com a câmera frontal de 16 MP.",
	"endpoint": "items",
	"ml_product_id": "MLB40213468",
	"option_type": "description"
}
```

**Parâmetros obrigatórios:**

| Campo           | Tipo   | Descrição                            |
| --------------- | ------ | ------------------------------------ |
| `title`         | String | Pergunta do usuário                  |
| `description`   | String | Descrição do produto                 |
| `endpoint`      | String | Endpoint da API do Mercado Livre     |
| `ml_product_id` | String | ID do produto no Mercado Livre       |
| `option_type`   | String | Tipo da resposta (ex: `description`) |

## Considerações Finais

O **ML Answers Assist** visa agilizar e otimizar o atendimento no Mercado Livre, melhorando a experiência do cliente e automatizando respostas com IA.
