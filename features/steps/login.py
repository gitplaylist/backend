from behave import given, when, then


@given(u'the user entered the email and the password')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given the user just put the email and the password')

@when(u'the user clicked the log in button')
def step_impl(context):
    raise NotImplementedError(u'STEP: When the user clicked the log in button')

@then(u'we should log the user in with a proper session value populated')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then we should log the user in with a proper session value populated')

@given(u'the user is already signed up previously')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given the user is already signed up previously')

@when(u'the user clicked the Github single sign-on button')
def step_impl(context):
    raise NotImplementedError(u'STEP: When the user just clicked the Github SSO button')

@when(u'we should log the user in with a proper session value populated')
def step_impl(context):
    raise NotImplementedError(u'STEP: When the user clicked the sign up button')
