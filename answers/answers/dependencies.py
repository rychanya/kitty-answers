from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi import Depends
from answers.models.settings import Auth0Settings
import jwt

auth0_settings = Auth0Settings()
token_auth_scheme = HTTPBearer()
jwks_client = jwt.PyJWKClient(
    f"https://{auth0_settings.VUE_APP_AUTH0_DOMAIN}/.well-known/jwks.json"
)


def get_payload(token: HTTPAuthorizationCredentials = Depends(token_auth_scheme)):
    signing_key = jwks_client.get_signing_key_from_jwt(token.credentials).key
    payload = jwt.decode(
        token.credentials,
        signing_key,
        algorithms=auth0_settings.AUTH0_ALGORITHMS,
        audience=auth0_settings.VUE_APP_AUTH0_AUDIENCE,
        issuer=auth0_settings.AUTH0_ISSUER,
    )
    return payload
