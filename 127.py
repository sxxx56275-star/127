from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

SMS_API_URL = "https://api.smsethiopia.com/v1/send"
API_KEY = "118TPI5N8GKKDRY14ACNCN7KY2A..."  # እባክዎን ትክክለኛውን የ API ቁልፍዎን እዚህ መሆኑን ያረጋግጡ

@app.route('/')
def home():
    return "SMS Dispatch App is running successfully!"

# አሁን በ GET እና በ POST ሁለቱንም መቀበል እንዲችል ተደርጓል
@app.route('/send-sms', methods=['GET', 'POST'])
def send_sms():
    # መረጃውን ከ URL (GET) ወይም ከ JSON (POST) መቀበል እንዲችል
    if request.method == 'GET':
        phone = request.args.get('phone')
        message = request.args.get('message')
    else:
        data = request.json or {}
        phone = data.get('phone')
        message = data.get('message')
    
    if not phone or not message:
        return jsonify({"error": "אנא አቅርብ phone እና message (ስልክ ቁጥር እና መልእክት ያስፈልጋሉ)"}), 400

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "to": phone,
        "message": message
    }
    
    try:
        response = requests.post(SMS_API_URL, json=payload, headers=headers)
        return response.json()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
