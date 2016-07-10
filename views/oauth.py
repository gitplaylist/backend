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
    response = github.get('user').data

    user = User.query.filter(User.email == response.get('email')).first()
    if not user:
        # Create the user object if the user wasn't signed up.
        user = User(response.get('email'))
        db.session.add(user)
        db.session.commit()

        # Save the token for the user.
        github_accesstoken = GithubAccessToken(
            user.id,
            response.get('token_type'),
            response.get('scope'),
            response.get('access_token'),
        )
    else:
        # Get the access token and change it.
        github_accesstoken = user.github_accesstoken
        github_accesstoken.token_type = response.get('token_type')
        github_accesstoken.scope = response.get('scope')
        github_accesstoken.access_token = response.get('access_token')

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
    next_url = request.args.get('next') or url_for('app.index')

    if response is None or not response.get('access_token'):
        flash(u'You denied the request to sign in')
        return redirect(next_url)

    session['spotify_accesstoken'] = response.get('access_token')
    response = spotify.get('user').data

    user = User.query.filter(User.email == response.get('email')).first()
    if not user:
        # Create the user object if the user wasn't signed up.
        user = User(response.get('email'))
        db.session.add(user)
        db.session.commit()

        # Save the token for the user.
        spotify_accesstoken = SpotifyAccessToken(
            user_id=user.id,
            token_type = response.get('token_type'),
            scope = response.get('scope'),
            access_token = response.get('access_token'),
            expires_in = response.get('expires_in'),
            refresh_token = response.get('refresh_token')
        )
    else:
        # Get the access token and change it.
        spotify_accesstoken = user.spotify_accesstoken
        spotify_accesstoken.token_type = response.get('token_type')
        spotify_accesstoken.scope = response.get('scope')
        spotify_accesstoken.access_token = response.get('access_token')
        spotify_accesstoken.expires_in = response.get('expires_in')
        spotify_accesstoken.refresh_token = response.get('refresh_token')

    db.session.add(spotify_accesstoken)
    db.session.commit()

    login_user(spotify_accesstoken.user)

    return redirect(next_url)
