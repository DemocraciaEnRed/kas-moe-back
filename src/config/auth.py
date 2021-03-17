from os import getenv

from fastapi_users.authentication import CookieAuthentication, JWTAuthentication



class Key:
  EXPIRY: int = 3600
  COOKIE: str = getenv('COOKIE')
  JWT: str = getenv('JWT_SECRET')
  JWT_PATH: str = "/auth/jwt/login"


auth_backends = []


cookie_authentication = CookieAuthentication(
    secret=Key.COOKIE,
    lifetime_seconds=Key.EXPIRY,
    cookie_name="x-moe-code-long",
    cookie_secure=False # Until TLS works properly 
)

auth_backends.append(cookie_authentication)


jwt_authentication = JWTAuthentication(
    secret=Key.JWT,
    lifetime_seconds=Key.EXPIRY,
    tokenUrl=Key.JWT_PATH
)

auth_backends.append(jwt_authentication)