from fastapi_users.authentication import JWTAuthentication


class JWT:
  KEY: str = "pwen-me"
  EXPIRY: int = 3600
  PATH: str = "/auth/jwt/login"


jwt_authentication = JWTAuthentication(
    secret=JWT.KEY, lifetime_seconds=JWT.EXPIRY, tokenUrl=JWT.PATH
)
