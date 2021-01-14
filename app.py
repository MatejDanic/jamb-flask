from flask import Flask
from models import Form
import sys

app = Flask(__name__)


@app.route('/')
def hello():
    form = Form()
    return str(form)

if __name__ == '__main__':
    app.run(debug=True)