from ProjectMejoraDespacho import settings
import datetime
import jwt

def encoded_reset_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.JWT_EXP_DELTA_SECONDS)
    }
    encoded_data = jwt.encode(payload, settings.JWT_SECRET, settings.JWT_ALGORITHM)
    return  encoded_data.decode('utf-8')

def decode_reset_token(reset_token):
    try:
        decoded_data = jwt.decode(reset_token, settings.JWT_SECRET,
                                  algorithms=[settings.JWT_ALGORITHM])
    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        return None  # means expired token

    return decoded_data['user_id']