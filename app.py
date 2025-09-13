import flask
from flask import Flask, template_rendered, request, redirect

app = Flask(__name__)

@app.before_request
def redirect_to_https():
    if request.headers.get('X-Forwarded-Proto', 'http') == 'http':
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)

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
