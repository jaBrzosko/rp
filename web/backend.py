from flask import Flask
from fetch_data import get_temperature
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
  return 'Server Works!'
  
@app.route('/temperature/<year>/<month>')
def say_hello(year, month):
  return get_temperature(year, month, 10)

if __name__ == '__main__':
    app.run(debug=True)
