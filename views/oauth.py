"""Implement OAuth callbacks."""
import requests

from flask import Blueprint, current_app, request, session, url_for, flash, redirect
from flask_login import login_user, current_user, logout_user
from flask.views import MethodView
from models.account import GithubAccessToken, User
from app import github, db

bp = Blueprint('oauth', __name__)

@bp.route('/users/signup/github')
def github_signup():
    return github.authorize(
        callback=url_for('oauth.github_oauth_handler', _external=True),
        next=request.args.get('next') or request.referrer
    )


@github.tokengetter
def get_github_token(token=None):
    if current_user.is_authenticated:
        return current_user.github_accesstoken.access_token
    else:
        return session.get('github_accesstoken')


@bp.route('/callback/github')
@github.authorized_handler
def github_oauth_handler(res):
    next_url = request.args.get('next') or url_for('public.index')

    if res is None:
        flash(u'You denied the request to sign in')
        return redirect(next_url)

    github_accesstoken = GithubAccessToken.query.filter(
        GithubAccessToken.access_token == res.get('access_token'),
    ).first()

    if not github_accesstoken:
        # Not signed up yet
        session['github_accesstoken'] = res.get('access_token')
        res = github.get('user').data

        # Create the user object.
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
        db.session.add(github_accesstoken)
        db.session.commit()

    login_user(github_accesstoken.user)

    return redirect(next_url)
