import json

from flask import Flask, redirect, render_template, request, session, url_for
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
def home():
    if not get_github_oauth_token():
        return redirect(url_for('login') + '?next=' + url_for('home'))
    return render_template('home.html', github_user=session.get('github_user'))


@app.route('/api')
def api():
    if not get_github_oauth_token():
        return render_template('api_noauth.html'), 401

    path = request.args.get('path')
    return json.dumps(github.get(path).data)


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
    session['github_user'] = github.get('/user').data
    return redirect(request.args.get('next'))


@app.route('/log-out/')
def logout():
    session['oauth_token'] = None
    session['github_user'] = None
    return render_template('logged_out.html')


@github.tokengetter
def get_github_oauth_token():
    return session.get('oauth_token')


if __name__ == '__main__':
    app.run()
