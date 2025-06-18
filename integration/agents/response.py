class AskToResponseAI:
    def user_question(self, items, question):
        try:
            #Esse código foi comentado porque não é efetivamente necessário para o funcionamento do sistema.
            """def preparar_dados(items):
                return "\n".join(
                    f"[Colletion {i}]: {' | '.join(f'{k}={v}' for k, v in item.items()) if isinstance(item, dict) else str(item).strip()}"
                    for i, item in enumerate(items[:3], 1)  # Limite de 3 itens
                )

            dados = preparar_dados(items)"""
            

            prompt = f"Com base nos dados abaixo, responda à pergunta: {question}\n\n{items}"

            return prompt
        except Exception as e:
            return f"ERRO: {str(e)}"
