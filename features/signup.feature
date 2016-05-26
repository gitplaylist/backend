Feature: Sign Up
    We should have a way to make our users enroll to our system.
    It should be able to sign up with a Github account.
    
    Scenario: User signed up with an email and a password
        Given the user just put the email and the password
        When the user clicked the sign up button
        Then we should create an account for the user with a User model populated properly

    Scenario: User signed up with a Github access token/refresh token
        Given the user just clicked the sign up button with Github account signed in
        When approved on the Github OAuth authorization and called back to our website
        Then we should create an account for the user with a User model populated properly
