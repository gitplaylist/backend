from behave import given, when, then

from app import db
from models.account import User


@given(u'the user entered the email and the password')
def step_impl(context):
    context.email = 'login@example.com'
    context.password = 'stewartthis1isnotasecurepassword'

    context.client.post('/sign_up', data={
        "email": context.email,
        "password": context.password,
    })


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
    context.email = 'login@example.com'
    context.password = 'stewartthis1isnotasecurepassword'

    user = User(context.email, context.password)
    db.session.add(user)
    db.session.commit()

@when(u'the user clicked the Github single sign-on button')
def step_impl(context):
    raise NotImplementedError(u'STEP: When the user just clicked the Github SSO button')

@when(u'we should log the user in with a proper session value populated')
def step_impl(context):
    raise NotImplementedError(u'STEP: When the user clicked the sign up button')
