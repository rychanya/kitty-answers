import jwt
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import Depends, Header, HTTPException, Path, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

from answers.db.user import get_or_create
from answers.models.settings import Auth0Settings

auth0_settings = Auth0Settings()
token_auth_scheme = HTTPBearer()
jwks_client = jwt.PyJWKClient(
    f"https://{auth0_settings.VUE_APP_AUTH0_DOMAIN}/.well-known/jwks.json"
)


def oid_from_path(str_id: str = Path(...)) -> ObjectId:
    try:
        return ObjectId(str_id)
    except (InvalidId, TypeError):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="not valid id"
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


def get_user(payload: dict = Depends(get_payload)):
    sub = payload["sub"]
    return get_or_create(sub)


def max_content_length(content_length: int = Header(None)):
    if content_length > 200 * 1024:
        raise HTTPException(status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
