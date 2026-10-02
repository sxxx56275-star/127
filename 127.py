
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# የ SMS Ethiopia API ዝርዝሮችዎ
SMS_API_URL = "https://api.smsethiopia.com/v1/send"  # እባክዎን ትክክለኛውን የ API ዩአርኤል ከዶክመንቴሽኑ ያረጋግጡ
API_KEY = "118TPI5N8GKKDRY14ACNCN7KY2A..."  # ሙሉውን የ API ቁልፍዎን እዚህ ያስገቡ

@app.route('/')
def home():
    return "SMS Dispatch App is running successfully!"

@app.route('/send-sms', methods=['POST'])
def send_sms():
    data = request.json
    phone = data.get('phone')
    message = data.get('message')
    
    if not phone or not message:
        return jsonify({"error": "Phone and message are required"}), 400

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
