from flask import Flask
from fetch_data import get_temperature
app = Flask(__name__)

@app.route('/')
def index():
  return 'Server Works!'
  
@app.route('/temperature/<year>/<month>')
def say_hello(year, month):
  return get_temperature(year, month, 10)

if __name__ == '__main__':
    app.run(debug=True)
