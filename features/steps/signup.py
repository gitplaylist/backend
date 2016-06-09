"""Define the behavior of sign up."""
from unittest.mock import MagicMock, Mock, patch

from behave import given, then, when
from models.account import GithubAccessToken, User
from views.oauth import github_oauth_handler
import app


@given(u'the user entered an email and password.')
def step_impl(context):
    context.email = 'sign.up@example.com'
    context.password = 'stewartthis1isnotasecurepassword'

@when(u'the user clicked the sign up button.')
def step_impl(context):
    context.client.post('/sign_up', data={
        "email": context.email,
        "password": context.password,
    })

@then(u'we should create an account for the user with the designated email.')
def step_impl(context):
    with context.app.app_context():
        assert User.query.filter(User.email == context.email).first() is not None

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
