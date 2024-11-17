from flask import Flask, request, jsonify
from rag import RAGService
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  

# Initialize RAG service
base_dir = os.path.dirname(os.path.abspath(__file__))
model_exists = os.path.exists(os.path.join(base_dir, "../saved_models/model"))
vectordb_exists = os.path.exists(os.path.join(base_dir, "../vector_db"))

if not model_exists or not vectordb_exists:
    print("First time initialization...")
    print("This will download and save the models. It might take a few minutes...")
    rag_service = RAGService(init_mode=True)
else:
    print("Loading existing models...")
    rag_service = RAGService(init_mode=False)

@app.route('/api/query', methods=['POST'])
def query_rag():
    try:
        data = request.get_json()
        question = data.get('question')
        
        if not question:
            return jsonify({'error': 'Question is required'}), 400
            
        relevant_docs = rag_service.query_documents(question)
        context = " ".join(relevant_docs)
        response = rag_service.generate_response(question, context)
        
        return jsonify({
            'answer': response,
            'context': relevant_docs
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'models_loaded': bool(rag_service),
        'models_path': os.path.join(base_dir, "saved_models/model")
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)