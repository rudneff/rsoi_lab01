from flask import Flask, render_template, request, Response, url_for
import requests

app = Flask(__name__)


@app.route('/')
@app.route('/authorization')
def send_request_without_auth():
    return render_template('index.html')


@app.route('/with_auth')
def send_request_with_auth():
    req = request.data()

    return ""


if __name__ == '__main__':
    app.run()
