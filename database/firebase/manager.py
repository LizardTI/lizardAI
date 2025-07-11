import firebase_admin
import datetime
import uuid
from firebase_admin import credentials, firestore
from flask import Flask, jsonify, request


class FirebaseManager:
    """Classe para gerenciamento de operações no Firebase Firestore."""

    def __init__(self):
        """Inicializa o gerenciador do Firebase."""
        self.firestore_db = None
        self._initialize_firebase()

    def _initialize_firebase(self):
        """
        Estabelece conexão com o Firebase.

        Carrega as credenciais e inicializa o cliente Firestore.
        """
        try:
            cred = credentials.Certificate("database/lizard-ai-firebase-adminsdk.json")
            firebase_admin.initialize_app(cred)
            self.firestore_db = firestore.client()
        except Exception as e:
            print(f"Erro ao inicializar Firebase: {str(e)}")
            self.firestore_db = None

    def insert(self, colecao: str, documento: str = None, dados: dict = None):
        """
        Insere ou atualiza documentos no Firestore.

        Parâmetros:
            colecao (str): Nome da coleção
            documento (str, opcional): ID do documento. Se None, gera UUID automático
            dados (dict, opcional): Dados a serem inseridos

        Retorna:
            dict: {
                "success": bool,
                "document_id": str,
                "error": str (opcional)
            }
        """
        try:
            if not self.firestore_db:
                return {
                    "success": False,
                    "error": "Conexão com Firebase não estabelecida"
                }

            dados = dados or {}

            if documento is None:
                documento = str(uuid.uuid4())
                dados.update({
                    'document_id': documento,
                    'timestamp': datetime.datetime.now().isoformat()
                })

            doc_ref = self.firestore_db.collection(colecao).document(documento)
            doc_ref.set(dados)

            return {
                "success": True,
                "document_id": documento
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def get(self, colecao: str, documento: str):
        """
        Recupera um documento específico do Firestore.

        Parâmetros:
            colecao (str): Nome da coleção
            documento (str): ID do documento

        Retorna:
            dict: {
                "success": bool,
                "data": dict (se sucesso),
                "error": str (se falha)
            }
        """
        try:
            if not self.firestore_db:
                return {
                    "success": False,
                    "error": "Conexão com Firebase não estabelecida"
                }

            doc_ref = self.firestore_db.collection(colecao).document(documento)
            doc = doc_ref.get()

            if doc.exists:
                return {
                    "success": True,
                    "data": doc.to_dict()
                }
            else:
                return {
                    "success": False,
                    "error": f"Documento não encontrado: {documento}"
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def get_all(self, colecao: str):
        """
        Recupera todos os documentos de uma coleção, incluindo IDs.

        Parâmetros:
            colecao (str): Nome da coleção

        Retorna:
            dict: {
                "success": bool,
                "data": list de dicts com os dados + id,
                "error": str (se falha)
            }
        """
        try:
            if not self.firestore_db:
                return {
                    "success": False,
                    "error": "Conexão com Firebase não estabelecida"
                }

            docs = self.firestore_db.collection(colecao).stream()

            data = []
            for doc in docs:
                doc_data = doc.to_dict()
                doc_data['id'] = doc.id
                data.append(doc_data)

            return {
                "success": True,
                "data": data
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
