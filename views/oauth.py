"""Implement OAuth callbacks."""
from __future__ import absolute_import
from flask import Blueprint, request, session, url_for, flash, redirect
from flask_login import login_user, current_user

from app import db, github, spotify
from models.account import GithubAccessToken, SpotifyAccessToken, User

bp = Blueprint('oauth', __name__)


@bp.route('/users/github')
def github_auth():
    return github.authorize(
        callback=url_for('oauth.github_oauth_handler', _external=True),
        next=request.args.get('next') or request.referrer
    )

@github.tokengetter
def get_github_token():
    if current_user.is_authenticated:
        access_token = current_user.github_accesstoken.access_token
    else:
        access_token = session.get('github_accesstoken')
    return (access_token, "")

@bp.route('/callback/github')
@github.authorized_handler
def github_oauth_handler(response):
    next_url = request.args.get('next') or url_for('app.index')

    if response is None or not response.get('access_token'):
        flash(u'You denied the request to sign in')
        return redirect(next_url)

    session['github_accesstoken'] = response.get('access_token')
    github_user = github.get('user').data

    user = User.query.filter(User.email == github_user.get('email')).first()
    if not user:
        # Create the user object if the user wasn't signed up.
        user = User(github_user.get('email'))
        db.session.add(user)
        db.session.commit()

        # Save the token for the user.
        github_accesstoken = GithubAccessToken(
            user.id,
            github_user.get('token_type'),
            github_user.get('scope'),
            github_user.get('access_token'),
        )
    else:
        # Get the access token and change it.
        github_accesstoken = user.github_accesstoken
        github_accesstoken.token_type = github_user.get('token_type')
        github_accesstoken.scope = github_user.get('scope')
        github_accesstoken.access_token = github_user.get('access_token')

@bp.route('/users/spotify')
def spotify_auth():
    return spotify.authorize(
        callback=url_for('oauth.spotify_oauth_handler', _external=True),
        next=request.args.get('next') or request.referrer
    )

@spotify.tokengetter
def get_spotify_token():
    if current_user.is_authenticated:
        access_token = current_user.spotify_accesstoken.access_token
    else:
        access_token = session.get('spotify_accesstoken')
    return (access_token, "")

@bp.route('/callback/spotify')
@spotify.authorized_handler
def spotify_oauth_handler(response):
    if not (response and response.get('access_token')):
        return 'Access denied: reason={0} error={1}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )

    session['spotify_accesstoken'] = response.get('access_token')
    spotify_user = spotify.get('/me').data

    user = User.query.filter(User.email == spotify_user.get('email')).first()
    if not user:
        # Create the user object if the user wasn't signed up.
        user = User(spotify_user.get('email'))
        db.session.add(user)
        db.session.commit()

        # Save the token for the user.
        spotify_accesstoken = SpotifyAccessToken (
            user.id,
            spotify_user.get('token_type'),
            spotify_user.get('scope'),
            spotify_user.get('access_token'),
            spotify_user.get('expires_in'),
            spotify_user.get('refresh_token'),
        )
    else:
        # Get the access token and change it.
        spotify_accesstoken = user.spotify_accesstoken
        spotify_accesstoken.token_type = spotify_user.get('token_type')
        spotify_accesstoken.scope = spotify_user.get('scope')
        spotify_accesstoken.access_token = spotify_user.get('access_token')
