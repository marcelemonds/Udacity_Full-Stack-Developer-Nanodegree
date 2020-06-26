from app import oauth
from auth import bp
from flask import request, redirect, url_for, session, jsonify
from six.moves.urllib.parse import urlencode
import os

AUTH0_CALLBACK_URL = os.environ['AUTH0_CALLBACK_URL']
AUTH0_CLIENTID = os.environ['AUTH0_CLIENTID']
AUTH0_CLIENT_SECRET = os.environ['AUTH0_CLIENT_SECRET']
AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
AUTH0_BASE_URL = os.environ['AUTH0_BASE_URL']
AUTH0_AUDIENCE = os.environ['AUTH0_AUDIENCE']

auth0 = oauth.register(
    'auth0',
    client_id=AUTH0_CLIENTID,
    client_secret=AUTH0_CLIENT_SECRET,
    api_base_url=AUTH0_BASE_URL,
    access_token_url=AUTH0_BASE_URL + '/oauth/token',
    authorize_url=AUTH0_BASE_URL + '/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)


# ------------------------
# auth -- login
# ------------------------
@bp.route('/login', methods=['GET'])
def login():
    return auth0.authorize_redirect(
        redirect_uri=AUTH0_CALLBACK_URL,
        audience=AUTH0_AUDIENCE
        )


# ------------------------
# auth -- callback
# ------------------------
@bp.route('/callback')
def callback_handling():
    # get authorization token
    token = auth0.authorize_access_token()
    return jsonify({
        'success': True,
        'token': token['access_token']
    }), 200


# ------------------------
# auth -- logout
# ------------------------
@bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    params = {
        'returnTo': url_for('auth.login', _external=True),
        'client_id': AUTH0_CLIENTID
        }
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))
