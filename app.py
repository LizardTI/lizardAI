from flask import Flask, request, jsonify
import datetime
from database.firebase.manager import FirebaseManager
from integration.agents.openai import OpenAIAgents
from integration.agents.response import AskToResponseAI

class LizardAI:
    def __init__(self):
        self.app = Flask(__name__)
        # Inicializa os serviços
        self.firebase_manager = FirebaseManager()
        self.call_agent = OpenAIAgents()
        self.response = AskToResponseAI()

        self._register_routes()

    def _register_routes(self):
        """Registra as rotas da aplicação Flask"""
        self.app.route("/ai-response", methods=["POST"])(self.lizard_ai)

    def lizard_ai(self):
        try:
            question = request.get_json().get('question') if request.is_json else request.form.get('question')

            firebase_data = self.firebase_manager.get("main-collection", "data")

            if "error" in firebase_data:
                return jsonify(firebase_data), 500

            items = firebase_data["data"]
            prompt = self.response.user_question([items], question)
            result = self.call_agent.o3_mini(prompt)

            historico_data = {
                "question": question,
                "response": result,
                "timestamp": datetime.datetime.now().isoformat()
            }
            
            insert_result = self.firebase_manager.insert_historico("historico_ia;", dados=historico_data)
            
            if not insert_result["success"]:
                return jsonify({"response": result, "warning": "Histórico não salvo"}), 200
            
            return jsonify({
                "response": result,
                "historico_id": insert_result["document_id"],
                }), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def run(self, host="0.0.0.0", port=5000, debug=True):
        self.app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    LizardAI().run()
