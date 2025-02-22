# Criar container com a llm

[Página Original](https://llamaedge.com/docs/user-guide/llamaedge-docker)

Build your own image
You can build nad publish a Docker image to use any models you like. First, download the model files (must be in GGUF format) you want from Huggingface. Of course, you could also your private finetuned model files here.

curl -LO https://huggingface.co/second-state/Qwen2-0.5B-Instruct-GGUF/resolve/main/Qwen2-0.5B-Instruct-Q5_K_M.gguf

Build a multi-platform image by passing the model files as --build-arg. The PROMPT_TEMPLATE is the specific text format the chat model is trained on to follow conversations. It differs for each model, and you will need to special attention. For all models published by the second-state organization, you can find the prompt-template in the model card.

```shell
docker buildx build . --platform linux/arm64,linux/amd64 \
  --tag secondstate/qwen-2-0.5b:latest -f Dockerfile \
  --build-arg CHAT_MODEL_FILE=Qwen2-0.5B-Instruct-Q5_K_M.gguf \
  --build-arg PROMPT_TEMPLATE=chatml
```

```senha
gpg --generate-key
```

Once it is built, you can publish it to Docker Hub.

docker login
docker push secondstate/qwen-2-0.5b:latest

# Depois temos que adicionar o container ao docker-compose.yaml

-   Executar normalmente como se fosse utilizar
