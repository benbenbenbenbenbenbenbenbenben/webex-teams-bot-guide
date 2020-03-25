from flask import Flask, request
from main import *
 
app = Flask(__name__)

@app.route("/", methods=['POST','GET'])
def index():
   if request.method == 'GET':
      return '<h1>Hello from Webhook Listener App!</h1>'
   if request.method == 'POST':
      return handler(request)

if __name__ == "__main__":
    app.run(debug=True)