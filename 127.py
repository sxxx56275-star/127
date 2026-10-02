from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "SMS Dispatch App is running successfully!"

if __name__ == '__main__':
    app.run(debug=True)
