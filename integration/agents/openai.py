# mainPrompt.py
import os
from colorama import init, Fore
from openai import OpenAI

# Inicializa o colorama para compatibilidade com Windows
init(autoreset=True)

class OpenAIAgents:
    def __init__(self):
        """
        Inicializa o gerenciador da API OpenAI, carregando a chave do ambiente.
        """
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        """
        Inicializa o cliente OpenAI, se a chave estiver disponível.
        """
        if self.api_key:
            print(f"{Fore.GREEN}[INFO] Chave da API OpenAI encontrada e carregada com sucesso.")
            self.client = OpenAI(api_key=self.api_key)
        else:
            print(f"{Fore.RED}[ERRO] Variável de ambiente OPENAI_API_KEY não está definida!")

    def o3_mini(self, prompt: str):
        """
        Envia uma pergunta para a OpenAI e retorna a resposta.

        Args:
            prompt (str): Texto da pergunta

        Returns:
            str | dict: Resposta em texto ou dict com erro
        """
        if not self.client:
            return {
                "success": False,
                "error": "Cliente OpenAI não inicializado. Verifique sua chave de API."
            }

        try:
            completion = self.client.chat.completions.create(
                model="o3-mini",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
            )

            content = completion.choices[0].message.content.strip()
            print(content)
            return content

        except Exception as e:
            print(f"{Fore.RED}[ERRO] Falha ao consultar OpenAI: {e}")
            return {
                "success": False,
                "error": str(e)
            }
