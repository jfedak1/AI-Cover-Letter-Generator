from fastapi import APIRouter, Depends, HTTPException, status
from ..models.auth import SignUpRequest, SignInRequest, TokenResponse
from ..core.dependencies import get_supabase

router = APIRouter()

@router.post("/create-account", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    payload: SignUpRequest,
    supabase = Depends(get_supabase),
):
    try:
        auth_response = supabase.auth.sign_up({
            "email": payload.email,
            "password": payload.password,
        })
    except AuthApiError as e:
        # Supabase will throw this on any 400-level error (invalid email, already registered, etc)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message or str(e),
        )

    # On success, we get back a session object
    session = auth_response.session
    return TokenResponse(access_token=session.access_token)

@router.post("/login", response_model=TokenResponse)
async def login(payload: SignInRequest, supabase = Depends(get_supabase)):
    result = supabase.auth.sign_in_with_password({"email": payload.email, "password": payload.password})
    if result.error:
        raise HTTPException(status_code=400, detail=result.error.message)
    session = result.session
    return TokenResponse(access_token=session.access_token)