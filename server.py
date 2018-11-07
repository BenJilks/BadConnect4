from flask import Flask
from flask import render_template
from flask import send_from_directory
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/place/<x>')
def place(x):
    print(x)
    return str(x)

@app.route('/<path:path>')
def file(path):
    f = open(path, 'rb')
    data = f.read()
    f.close()
    return data

if __name__ == '__main__':
    app.run()
