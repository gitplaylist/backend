"""Define the behavior of sign up."""
from unittest.mock import MagicMock, Mock, patch

from behave import given, then, when
from models.account import User
from views.oauth import github_oauth_handler, spotify_oauth_handler


@given(u'the user entered an email and password.')
def step_impl(context):
    context.email = 'sign.up@example.com'
    context.password = 'stewartthis1isnotasecurepassword'

@given(u'the user entered an invalid email.')
def step_impl(context):
    context.email = 'not an email'
    context.password = 'stewartthis1isnotasecurepassword'

@given(u'the user entered an invalid password.')
def step_impl(context):
    context.email = 'bad.sign.up@example.com'
    context.password = 'password'

@when(u'the user clicked the sign up button.')
def step_impl(context):
    context.client.post('/users', data={
        "email": context.email,
        "password": context.password,
    })

@then(u'we should create an account for the user with the designated email.')
def step_impl(context):
    with context.app.app_context():
        assert User.query.filter(User.email == context.email).first() is not None

@then(u'we should not create an account for the user with the designated email.')
def step_impl(context):
    with context.app.app_context():
        assert User.query.filter(User.email == context.email).first() is None

@given(u'the user clicked the Github sign up button with Github account signed in.')
def step_impl(context):
    res = context.client.get('/users/github')
    assert res.status_code == 302
    assert res.headers['Location'].startswith(
        'https://github.com/login/oauth/authorize'
    )

@when(u'approved on the Github OAuth authorization and called back to our website.')
def step_impl(context):
    github_user_me = MagicMock()
    github_user_me.data = {"email": "github@example.com"}
    github_get = Mock(return_value=github_user_me)
    github_authorized_response = Mock(return_value={
        "access_token": "some-token",
        "scope": "",
        "token_type": "bearer",
    })
    with patch('app.github.get', github_get),\
        patch('app.github.authorized_response', github_authorized_response),\
        context.app.test_request_context(
            '/callback/github?code=something'
        ):
            res = github_oauth_handler()
    assert res.status_code == 302
    assert res.headers['Location'].endswith("/")

@then(u'we should create an account for the user with the designated Github account.')
def step_impl(context):
    with context.app.app_context():
        assert User.query.filter(User.email == "github@example.com").first() is not None

@given(u'the user clicked the Spotify sign up button with Spotify account signed in.')
def step_impl(context):
    res = context.client.get('/users/spotify')
    assert res.status_code == 302
    assert res.headers['Location'].startswith(
        'https://accounts.spotify.com/authorize'
    )

@when(u'approved on the Spotify OAuth authorization and called back to our website.')
def step_impl(context):
    spotify_user_me = MagicMock()
    spotify_user_me.data = {"email": "spotify@example.com"}
    spotify_get = Mock(return_value=spotify_user_me)
    spotify_authorized_response = Mock(return_value={
        "access_token": 'existing-token',
        "scope": '',
        "token_type": 'bearer',
        "expires_in": 42,
        "refresh_token": 'refresh-token',
    })
    with patch('app.spotify.get', spotify_get),\
        patch('app.spotify.authorized_response', spotify_authorized_response),\
        context.app.test_request_context(
            '/callback/spotify?code=something'
        ):
            res = spotify_oauth_handler()
    assert res.status_code == 302
    assert res.headers['Location'].endswith("/")

@then(u'we should create an account for the user with the designated Spotify account.')
def step_impl(context):
    with context.app.app_context():
        assert User.query.filter(User.email == "spotify@example.com").first() is not None
