from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

SMS_API_URL = "https://smsethiopia.com/api/sms/send"
API_KEY = 1A64IQPQ4GWUSMIFQ91CL2L4LLV32879SNTC47LD # የእርስዎ ትክክለኛ API Key

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Private SMS Console</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f6f8; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); width: 100%; max-width: 400px; }
        h2 { color: #111; margin-bottom: 5px; }
        p { color: #666; font-size: 14px; margin-bottom: 20px; }
        label { font-weight: bold; font-size: 13px; color: #333; display: block; margin-bottom: 5px; }
        input, textarea { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; margin-bottom: 15px; font-size: 14px; }
        textarea { resize: vertical; height: 100px; }
        button { background-color: #1b4d3e; color: white; border: none; width: 100%; padding: 12px; border-radius: 6px; font-size: 16px; cursor: pointer; font-weight: bold; }
        button:hover { background-color: #14382d; }
        .result { margin-top: 15px; padding: 10px; border-radius: 6px; font-size: 14px; text-align: center; }
        .success { background-color: #e1f5fe; color: #01579b; }
        .error { background-color: #ffebee; color: #c62828; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Compose a message</h2>
        <p>One recipient per send. Your message is sent via gateway.</p>
        
        <form method="POST">
            <label>Recipient phone number</label>
            <input type="text" name="phone" placeholder="+251 91 123 4567" required>
            
            <label>Message</label>
            <textarea name="message" placeholder="Type your message here..." required></textarea>
            
            <button type="submit">Send SMS</button>
        </form>

        {% if response_msg %}
            <div class="result {{ 'success' if success else 'error' }}">
                {{ response_msg }}
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def send_sms():
    response_msg = None
    success = False
    
    if request.method == 'POST':
        phone = request.form.get('phone')
        message = request.form.get('message')
        
        # ከኦፊሴላዊው ዶክመንቴሽን የተወሰደ ትክክለኛ የ Authorization ሄደር
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "KEY": API_KEY,  # ሁለቱንም አማራጮች በመጠቀም ስህተትን እንከላከላለን
            "Content-Type": "application/json"
        }
        payload = {
            "msisdn": phone,
            "text": message
        }
        
        try:
            res = requests.post(SMS_API_URL, json=payload, headers=headers)
            res_data = res.json()
            if res.status_code == 200:
                response_msg = "መልእክቱ በተሳካ ሁኔታ ተልኳል!"
                success = True
            else:
                response_msg = f"ስህተት ተፈጥሯል: {res_data}"
                success = False
        except Exception as e:
            response_msg = f"የግንኙነት ስህተት: {str(e)}"
            success = False
            
    return render_template_string(HTML_PAGE, response_msg=response_msg, success=success)

if __name__ == '__main__':
    app.run(debug=True)
