Feature: Sign Up
    There should be a way for users create an account with gitplaylist. It should allow for both
    traditional email and password sign up and allow Github single sign on account.

    Scenario: User signed up with an email and a password.
        Given the user entered an email and password.
        When the user clicked the sign up button.
        Then we should create an account for the user with the designated email.

    Scenario: User signed up with an invalid email.
        Given the user entered an invalid email.
        When the user clicked the sign up button.
        Then we should not create an account for the user with the designated email.

    Scenario: User signed up with an invalid password.
        Given the user entered an invalid password.
        When the user clicked the sign up button.
        Then we should not create an account for the user with the designated email.

    Scenario: User signed up with a Github access token/refresh token.
        Given the user clicked the Github sign up button with Github account signed in.
        When approved on the Github OAuth authorization and called back to our website.
        Then we should create an account for the user with the designated Github account.
