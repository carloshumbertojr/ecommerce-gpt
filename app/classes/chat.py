from openai import OpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.chat_models.llama_edge import LlamaEdgeChatService

import app.data.prompts as prompts
from app.config.config import settings


class GPTChat:
    """
    A class for interacting with an AI chat model, querying transcripts, finding objections in transcripts
    and generating responses from sales calls.
    """

    def __init__(self):
        """
        Initializes a GPTChat instance.
        """
        url_api = settings.CHAT_API_KEY

        self.messages = []
        # client = OpenAI()
        if settings.BASE_NAME_CHAT_MODEL.__contains__("gpt"):
            self.chat = OpenAI(
                api_key=settings.OPEN_AI_API_KEY,
            )
        else:
            self.chat = LlamaEdgeChatService(
                service_url=url_api,
                model=settings.BASE_NAME_CHAT_MODEL,
                request_timeout=300,
            )
        self.response = ""

        self.messages.append(SystemMessage(content=prompts.NEW_TEST_PROMPT))

        self.ai_message = None

    def message_bot(self, human_message: HumanMessage, description, model):
        """
        Envia uma mensagem para o chatbot e retorna a resposta.

        Parameters:
            human_message (str): A pergunta do usuário.
            description (str): O histórico da conversa ou contexto.
            model (str): O modelo a ser utilizado (ex: "gpt-4o").

        Returns:
            str: A resposta do chatbot.
        """

        messages = [
            {
                "role": "system",
                "content": f"{prompts.NEW_TEST_PROMPT} | Descrição do contexto: {description}",
            },
            {"role": "user", "content": human_message},
        ]

        if "gpt" in settings.BASE_NAME_CHAT_MODEL:
            ai_message = self.chat.chat.completions.create(
                model="gpt-4o",  # Ou settings.BASE_NAME_CHAT_MODEL
                messages=messages,
                max_tokens=200,
            )
            # Pegando a resposta correta
            return ai_message.choices[0].message.content
        else:
            self.chat.model = model
            self.response = self.chat.invoke(
                messages,
                max_tokens=100,
            )

            self.messages.append({"role": "user", "content": human_message})
            ai_message = {"role": "assistant", "content": self.response.content}
            self.messages.append(ai_message)

            return ai_message["content"]
