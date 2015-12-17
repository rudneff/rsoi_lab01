import json

from flask import Flask, render_template, request, redirect, Response, url_for
import requests

CLIENT_ID = '55474bf4256c6ff'
CLIENT_SECRET = '8cd4859a6fca4d406d469eb8e5159113500c4ba9'
GRANT_TYPE = 'authorization_code'
ACCESS_TOKEN = ''
REFRESH_TOKEN = ''
app = Flask(__name__)


@app.route('/')
def send_request_without_auth():
    return render_template('index.html', client_id=CLIENT_ID)


@app.route('/authorization')
def auth_request_token():
    access_code = request.args.get('code', '')
    if access_code in '':
        return "Access denied."
    auth_url = 'https://api.imgur.com/oauth2/token'
    params = {
        'code': access_code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': GRANT_TYPE
    }
    response = requests.post(url=auth_url, data=params)
    if response.status_code != 200:
        return "Error."
    global ACCESS_TOKEN
    ACCESS_TOKEN = response.json().get('access_token', '')
    if ACCESS_TOKEN in '':
        return "Error."

    return redirect('http://127.0.0.1:5000/queries')


@app.route('/queries')
def show_queries():
    return render_template('queries.html')


@app.route('/info')
def get_user_info():
    if ACCESS_TOKEN in '':
        return "Authorizaton required!"
    url = 'https://api.imgur.com/3/account/rudneff'
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(ACCESS_TOKEN)}
    response = requests.get(url=url, headers=headers)
    if response.status_code != 200:
        return "Error."
    info = response.text
    info = json.loads(info)
    info = json.dumps(info)
    return info


if __name__ == '__main__':
    app.run()
