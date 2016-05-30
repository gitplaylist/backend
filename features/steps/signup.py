"""Define the behavior of sign up."""
from behave import given, then, when

from models.account import User


@given(u'the user just put the email and the password.')
def step_impl(context):
    context.email = 'tim+stewart@gmail.com'
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

@given(u'the user just clicked the sign up button with Github account signed in.')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given the user just clicked the sign up button with Github account signed in.')

@when(u'approved on the Github OAuth authorization and called back to our website.')
def step_impl(context):
    raise NotImplementedError(u'STEP: When approved on the Github OAuth authorization and called back to our website.')

@then(u'we should create an account for the user with the designated Github account.')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then we should create an account for the user with the designated Github account.')
