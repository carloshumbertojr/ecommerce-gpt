ARG BASE_IMAGE=llamaedge/api-server:latest
FROM $BASE_IMAGE
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# modelos em geral
# https://huggingface.co/second-state
# seção "models"
# selecione um modelo de chat
# vá para a seção "Quantized GGUF Models"
# procure por um modelo com tamanho [medium, balanced quality - recommended] na coluna "Use case"
# Define argumentos de build (usados no build)


ARG CONTEXT_SIZE=32000
ARG MODEL_URL='https://huggingface.co/second-state/Qwen2.5-0.5B-Instruct-GGUF/resolve/main/Qwen2.5-0.5B-Instruct-Q5_K_M.gguf'
ARG PROMPT_FORMAT='chatml'

# ARG CONTEXT_SIZE=128000
# ARG MODEL_URL='https://huggingface.co/second-state/Llama-3.2-1B-Instruct-GGUF/resolve/main/Llama-3.2-1B-Instruct-Q5_K_M.gguf'
# ARG PROMPT_FORMAT='llama-3-chat'

# ARG CONTEXT_SIZE=2048
# ARG MODEL_URL='https://huggingface.co/second-state/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/TinyLlama-1.1B-Chat-v1.0-Q4_K_M.gguf'
# ARG PROMPT_FORMAT='chatml'

# Download the model file.
RUN curl -L -o $(basename $MODEL_URL) $MODEL_URL

# Generate the init script.
RUN cat > /app/init.sh <<EOF
#!/bin/bash
set -e
MODEL_FILE=$(basename $MODEL_URL)

wasmedge \\
	--dir .:. \\
	--nn-preload "default:GGML:AUTO:\$MODEL_FILE" \\
	llama-api-server.wasm \\
	-p "$PROMPT_FORMAT" \\
	-c "$CONTEXT_SIZE" \\
	--model-name "\$MODEL_FILE" \\
	--socket-addr 0.0.0.0:8080 \\
	--log-prompts --log-stat
EOF
RUN chmod +x /app/init.sh

# Execute the API server
ENTRYPOINT ["/bin/bash"]
CMD ["/app/init.sh"]