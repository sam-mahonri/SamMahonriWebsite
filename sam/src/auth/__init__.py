from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity,
    set_access_cookies, unset_jwt_cookies, get_jwt
)
from ... import jwt, limiter
from datetime import timedelta, timezone, datetime
from ..utils.jwt_expiry import *

def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + TIMEDELTA_REFRESH)
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity(), expires_delta=ACCESS_TOKEN_EXPIRY)
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response