import flask
from flask import Flask, template_rendered

app = Flask(__name__)

@app.route('/')
def home():
    return flask.render_template('index.html')

@app.route('/first')
def first():
    return flask.render_template('first.html')

@app.route('/second')
def second():
    return flask.render_template('second.html')

@app.route('/third')
def third():
    return flask.render_template('third.html')

if __name__ == '__main__':
    app.run(debug=True)
