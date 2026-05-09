import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
from cachetools import TTLCache

from app.core.config import settings

security = HTTPBearer()

# Cache JWKS for 1 hour to prevent rate limits
jwks_cache = TTLCache(maxsize=1, ttl=3600)

async def get_jwks():
    if "jwks" in jwks_cache:
        return jwks_cache["jwks"]
    
    # Simple workaround if no key provided
    if not settings.next_public_clerk_publishable_key or "REPLACE" in settings.next_public_clerk_publishable_key:
        return None

    # Derive JWKS URL from publishable key
    try:
        # Clerk publishable keys follow format pk_test_... or pk_live_...
        # The JWKS URL is typically https://clerk.<domain>/.well-known/jwks.json
        # For simplicity, we assume frontend passes token and we verify it
        jwks_url = "https://api.clerk.com/v1/jwks"
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                jwks_url,
                headers={"Authorization": f"Bearer {settings.clerk_secret_key}"}
            )
            if resp.status_code == 200:
                jwks = resp.json()
                jwks_cache["jwks"] = jwks
                return jwks
    except Exception as e:
        import logging
        logging.getLogger("uvicorn").error(f"Failed to fetch JWKS: {e}")
        return None

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    
    # If no valid keys, allow bypass for development/testing
    if not settings.clerk_secret_key or "REPLACE" in settings.clerk_secret_key:
        return {"sub": "dev_user_123", "role": "user"}

    jwks = await get_jwks()
    if not jwks:
        # Fallback if JWKS unavailable but keys are set - reject
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication configuration error"
        )

    try:
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks.get("keys", []):
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
                break

        if rsa_key:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(rsa_key)
            payload = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                options={"verify_aud": False}
            )
            return payload
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unable to find appropriate key"
    )

async def get_current_user(payload: dict = Depends(verify_token)):
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="User ID not found in token")
    return user_id
