from flask import Flask, request, jsonify
import base64
import io
from pdfminer.high_level import extract_text
import docx

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "API online!"

@app.route("/extract", methods=["POST"])
def extract():
    try:
        data = request.get_json()
        file_data = data.get("file_data")
        file_name = data.get("file_name")
        if not file_data or not file_name:
            return jsonify({"error": "Missing data"}), 400
        file_bytes = base64.b64decode(file_data)
        content = io.BytesIO(file_bytes)
        if file_name.lower().endswith('.pdf'):
            text = extract_text(content)
        elif file_name.lower().endswith(('.doc', '.docx')):
            doc = docx.Document(content)
            text = "\n".join([p.text for p in doc.paragraphs])
        else:
            return jsonify({"error": "Unsupported file type"}), 400
        return jsonify({"parsed_text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
