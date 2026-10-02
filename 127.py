
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# ትክክለኛው የኤፒአይ አድራሻ ከ cURL ትዕዛዙ
SMS_API_URL = "https://smsethiopia.com/api/sms/send"
API_KEY = "118TPI5N8GKKDRY14ACNCN7KY2A..."  # የእርስዎ ትክክለኛ API Key

@app.route('/')
def home():
    return "SMS Dispatch App is running successfully!"

@app.route('/send-sms', methods=['GET', 'POST'])
def send_sms():
    if request.method == 'GET':
        phone = request.args.get('phone')
        message = request.args.get('message')
    else:
        data = request.json or {}
        phone = data.get('phone')
        message = data.get('message')
    
    if not phone or not message:
        return jsonify({"error": "ስልክ ቁጥር እና መልእክት ያስገቡ"}), 400

    headers = {
        "KEY": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "msisdn": phone,
        "text": message
    }
    
    try:
        response = requests.post(SMS_API_URL, json=payload, headers=headers)
        return response.json()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
