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
        # 1️⃣ create the auth user
        auth_response = supabase.auth.admin.create_user(
            {
                "email": payload.email,
                "password": payload.password,
                "email_confirm": True,
            }
        )
    except AuthApiError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message or str(e),
        )

    # 2️⃣ insert a blank profile row that just stores the new user’s id
    user_id = auth_response.user.id               # ← auth.users primary-key
    supabase.table("profiles").insert({"id": user_id}).execute()

    # 3️⃣ sign the user in and return the token
    sign_in_response = supabase.auth.sign_in_with_password(
        {"email": payload.email, "password": payload.password}
    )
    token = sign_in_response.session.access_token
    return TokenResponse(access_token=token)

@router.post("/login", response_model=TokenResponse)
async def login(payload: SignInRequest, supabase=Depends(get_supabase)):
    try:
        res = supabase.auth.sign_in_with_password(
            {"email": payload.email, "password": payload.password}
        )
    except AuthApiError as e:
        raise HTTPException(status_code=400, detail=e.message or str(e))

    token = res.session.access_token
    return TokenResponse(access_token=token)