from unittest.mock import MagicMock, Mock, patch

from app import db
from behave import given, then, when
from flask_login import current_user
from models.account import GithubAccessToken, User
from views.oauth import github_oauth_handler


@given(u'the user entered the email and the password')
def step_impl(context):
    context.email = 'login@example.com'
    context.password = 'stewartthis1isnotasecurepassword'

    with context.app.app_context():
        user = User(
            email=context.email,
            password=context.email,
        )
        db.session.add(user)
        db.session.commit()

@when(u'the user clicked the log in button')
def step_impl(context):
    context.client.post('/login', data={
        "email": context.email,
        "password": context.password,
    })

@then(u'we should log the user in with a proper session value populated')
def step_impl(context):
    with context.app.app_context():
        user = User.query.filter(User.email == context.email).first()
        assert user.is_authenticated

@given(u'the user is already signed up previously')
def step_impl(context):
    context.email = 'login+1@example.com'
    context.password = 'stewartthis1isnotasecurepassword'
    context.access_token = 'existing-token'
    context.scope = ''
    context.token_type = 'bearer'

    with context.app.app_context():
        context.user = User(
            email=context.email,
            password=context.email,
        )
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
    with patch('app.github.get', github_get),\
        patch('app.github.authorized_response', github_authorized_response),\
        context.app.test_request_context(
            '/callback/github?code=something'
        ):
            res = github_oauth_handler()
            context.current_user_id = current_user.id
    assert res.status_code == 302
    assert res.headers['Location'].endswith("/")

@then(u'we should log the Github user in with a proper session value populated')
def step_impl(context):
    with context.app.app_context():
        assert context.current_user_id == context.expected_user_id
