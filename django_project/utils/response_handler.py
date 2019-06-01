SUCCESS = 'success'
INFO = 'info'
WARNING = 'warning'
DANGER = 'error'


def generic_response(message):
    return {'detail': message}


def alert_response(message_type, message, alert_type=''):
    if isinstance(message, dict):
        # message = str(message)
        message = 'Oops! Some error happened! Please retry.'

    return {
        'alertTitle': alert_type,
        'alertMessageType': message_type,
        'alertMessage': message}


def failed_response(message):
    return {'success': False, 'message': message}


def success_response(message):
    return {'success': True, 'message': message}
