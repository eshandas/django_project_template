class ResponseKeys(object):
    SESSION_ID = 'sessionId'
    USER = 'user'


class SuccessMessages(object):
    PASSWORD_RESET = 'An email has been sent to change the password'


class FailMessages(object):
    USER_INACTIVE = 'This user is not active'
    INVALID_CREDENTIALS = 'Wrong username or password'
    INVALID_EMAIL = 'This email does not exist'
    INVALID_PASSWORD = 'Invalid password'
    USER_ALREADY_EXISTS = 'This user already exists'
    INVALID_SESSION_ID = 'Invalid Session Id'
    TOKEN_MISSING = 'Token missing'
    INVALID_TOKEN = 'Invalid token'
    NOT_ADMIN = 'User is not an admin'
    AUTH_HEADER_INVALID = 'Invalid Authorization'
    INVALID_VALUE = 'Invalid merchant id or app id or secret'


class RequestKeys(object):
    EMAIL = 'email'
    PASSWORD = 'password'
    CONFIRM_PASSWORD = 'confirm_password'
    NEXT = 'next'
    TOKEN = 'token'


class ResponseKeys(object):
    SESSION_ID = 'sessionId'
    USER = 'user'
    LOGGED_OUT = 'loggedOut'
