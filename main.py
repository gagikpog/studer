from flask import Flask, render_template
from user import User
from bill import Bill

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
