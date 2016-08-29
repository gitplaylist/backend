from unittest.mock import MagicMock, Mock, patch

from behave import given, then, when
from flask import session
from flask_login import current_user, logout_user

from app import db
from models.account import GithubAccessToken, SpotifyAccessToken, User
from views.oauth import github_oauth_handler, spotify_oauth_handler


@given(u'the user entered the email and the password')
def step_impl(context):
    context.email = 'login@example.com'
    context.password = 'password and some entropy: 12345'

    with context.app.app_context():
        context.user = User(
            email=context.email,
            password=context.password,
        )
        db.session.add(context.user)
        db.session.commit()

@when(u'the user clicked the log in button')
def step_impl(context):
    with context.app.app_context():
        context.response = context.client.post('/users/authorize', data={
            "email": context.email,
            "password": context.password,
        })

@then(u'we should log the user in with a proper session value populated')
def step_impl(context):
    with context.app.app_context():
        assert context.response.status_code == 200

@given(u'the user entered the email and an incorrect password')
def step_impl(context):
    context.email = 'badlogin@example.com'
    context.password = 'incorrect password'

    with context.app.app_context():
        context.user = User(
            email=context.email,
            password="incorrect password with entropy",
        )
        db.session.add(context.user)
        db.session.commit()

@then(u'we should not log the user in')
def step_impl(context):
    with context.app.app_context():
        assert context.response.status_code == 400

@given(u'the user is already signed up with Github')
def step_impl(context):
    context.email = 'login+1@example.com'
    context.access_token = 'existing-token'
    context.scope = ''
    context.token_type = 'bearer'

    with context.app.app_context():
        context.user = User(email=context.email)
        db.session.add(context.user)
        db.session.commit()
        context.token = GithubAccessToken(
            context.user.id, context.token_type, context.scope, context.access_token
        )
        db.session.add(context.token)
        db.session.commit()

        context.expected_user_id = context.user.id

@when(u'the user clicked the Github single sign-on button')
def step_impl(context):
    github_user_me = MagicMock()
    github_user_me.data = {"email": context.email}
    github_get = Mock(return_value=github_user_me)
    github_authorized_response = Mock(return_value={
        "access_token": context.access_token,
        "scope": context.scope,
        "token_type": context.token_type,
    })
    with\
        patch('app.github.get', github_get),\
        patch('app.github.authorized_response', github_authorized_response),\
        context.app.test_request_context('/callback/github?code=something'):
            # Github OAuth callback
            res = github_oauth_handler()
            context.current_user_id = current_user.id

            # There aren't any errors
            assert session.get('_flashes') in (None, [])
    assert res.status_code == 302
    assert res.headers['Location'].endswith("/")

@then(u'we should log the user in with the proper session value populated')
def step_impl(context):
    with context.app.app_context():
        assert context.current_user_id == context.expected_user_id

@given(u'the user is already signed up with Spotify')
def step_impl(context):
    context.email = 'login+2@example.com'
    context.access_token = 'existing-token'
    context.scope = ''
    context.token_type = 'bearer'
    context.expires_in = 23
    context.refresh_token = 'refresh-token'

    with context.app.app_context():
        context.user = User(email=context.email)
        db.session.add(context.user)
        db.session.commit()
        context.token = SpotifyAccessToken(
            user_id=context.user.id,
            token_type=context.token_type,
            scope=context.scope,
            access_token=context.access_token,
            expires_in=context.expires_in,
            refresh_token=context.refresh_token
        )
        db.session.add(context.token)
        db.session.commit()

        context.expected_user_id = context.user.id

@when(u'the user clicked the Spotify single sign-on button')
def step_impl(context):
    spotify_user_me = MagicMock()
    spotify_user_me.data = {"email": context.email}
    spotify_get = Mock(return_value=spotify_user_me)
    spotify_authorized_response = Mock(return_value={
        "access_token": context.access_token,
        "scope": context.scope,
        "token_type": context.token_type,
        "expires_in": context.expires_in,
        "refresh_token": context.refresh_token,
    })
    with\
        patch('app.spotify.get', spotify_get),\
        patch('app.spotify.authorized_response', spotify_authorized_response),\
        context.app.test_request_context('/callback/spotify?code=something'):
            # Spotify OAuth callback
            res = spotify_oauth_handler()
            context.current_user_id = current_user.id

            # There aren't any errors
            assert session.get('_flashes') in (None, [])
    assert res.status_code == 302
    assert res.headers['Location'].endswith("/")
