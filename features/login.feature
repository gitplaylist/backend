Feature: Log In
    Users should be able to log in to our service if they have a handle on our system.
    
    Scenario: User logged in with an email and a password
        Given the user just put the email and the password
        When the user clicked the log in button
        Then we should log the user in with a proper session value populated

    Scenario: User logged in with the Github SSO button
        Given the user is already signed up previously
        When the user just clicked the Github SSO button
        Then we should log the user in with a proper session value populated
