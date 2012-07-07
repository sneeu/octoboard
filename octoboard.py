import pprint

from flask import Flask, redirect, url_for, session, request
from flaskext.oauth import OAuth

import secrets


DEBUG = True


app = Flask(__name__)
app.debug = DEBUG
app.secret_key = secrets.SECRET_KEY
oauth = OAuth()


github = oauth.remote_app('github',
    base_url='https://api.github.com',
    request_token_url=None,
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    consumer_key='e149164fb1f47b192df6',
    consumer_secret=secrets.GITHUB_CLIENT_SECRET,
)


@app.route('/')
def index():
    if not get_github_oauth_token():
        return redirect(url_for('login') + '?next=' + url_for('index'))
    me = github.get('/user')
    return pprint.pformat(me.data)


@app.route('/log-in/')
def login():
    return github.authorize(callback=url_for('github_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))


@app.route('/log-in/complete/')
@github.authorized_handler
def github_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    return redirect(request.args.get('next'))


@github.tokengetter
def get_github_oauth_token():
    return session.get('oauth_token')


if __name__ == '__main__':
    app.run()
