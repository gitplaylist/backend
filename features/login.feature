Feature: Login
    Users should be able to login to our service if they have an account on our system.

    Scenario: User logged in with an email and a password
        Given the user entered the email and the password
        When the user clicked the log in button
        Then we should log the user in with a proper session value populated

    Scenario: User logged in with the Github single sign-on button
        Given the user is already signed up previously
        When the user clicked the Github single sign-on button
        Then we should log the user in with a proper session value populated
