"""Implement OAuth callbacks."""
from __future__ import absolute_import
from flask import Blueprint, request, session, url_for, flash, redirect
from flask_login import login_user, current_user

from app import github, db
from models.account import GithubAccessToken, User

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
def github_oauth_handler(res):
    next_url = request.args.get('next') or url_for('app.index')

    if res is None or not res.get('access_token'):
        flash(u'You denied the request to sign in')
        return redirect(next_url)

    session['github_accesstoken'] = res.get('access_token')
    res = github.get('user').data

    user = User.query.filter(User.email == res.get('email')).first()
    if not user:
        # Create the user object if the user wasn't signed up.
        user = User(res.get('email'))
        db.session.add(user)
        db.session.commit()

        # Save the token for the user.
        github_accesstoken = GithubAccessToken(
            user.id,
            res.get('token_type'),
            res.get('scope'),
            res.get('access_token'),
        )
    else:
        # Get the access token and change it.
        github_accesstoken = user.github_accesstoken
        github_accesstoken.token_type = res.get('token_type')
        github_accesstoken.scope = res.get('scope')
        github_accesstoken.access_token = res.get('access_token')

    db.session.add(github_accesstoken)
    db.session.commit()

    login_user(github_accesstoken.user)

    return redirect(next_url)
