import functools
import utils
import requests
import urllib.parse

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/callback', methods=('GET', 'POST'))
def callback():
    pass

@bp.route('/client_id', methods=('GET',))
def client_id():
    d = {}
    d["@context"] = ["https://www.w3.org/ns/solid/oidc-context.jsonld"]
    d["client_id"] = "http://localhost:5000/auth/client_id"
    d["client_name"] = "App"
    d["redirect_uris"] = ["http://localhost:5000/auth/callback"]
    d["post_logout_redirect_uris"] = ['http://localhost:5000/auth/logout']
    d["client_uri"] = ['http://localhost:5000/']
    d["scope"] = "openid webid offline_access"
    d["grant_types"] = [ "refresh_token", "authorization_code"]
    d["response_types"] = "code"
    d["default_max_age"] = 3600
    d["require_auth_time"] = True
    return d

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f'{username} , {password}')
        web_id = "https://id.inrupt.com/zg009test"
        oidc_issuer = utils.get_oidc_issuer(web_id)
        print(oidc_issuer)
        data, auth_endpoint = utils.get_auth_endpoint(oidc_issuer)
        print(data, auth_endpoint)
        token_endpoint = data['token_endpoint']
        print(token_endpoint)
        secret_string = 'abc1234dfe5678'
        session['secret_string'] = secret_string
        # this needs to be stored in the session object
        encoded_string = utils.encode_string(secret_string)
        print(session)
        scope = urllib.parse.quote('openid webid offline_access')
        params = {
            'response_type': 'code',
            'redirect_uri': 'http://localhost:5000/auth/callback',
            'scope': 'openid',
            'client_id': 'http://localhost:5000/auth/client_id',
            'code_challenge_method': 'S256',
            'code_challenge': encoded_string
        }
        resp = requests.get(auth_endpoint, params=params)
        print(resp.request.body)
        print(resp.request.url)
        print(resp.content)
    
    return render_template('auth/login.html')

@bp.route('/logout', methods=('GET',))
def logout():
    session.clear()
    return redirect(url_for('auth.login'))