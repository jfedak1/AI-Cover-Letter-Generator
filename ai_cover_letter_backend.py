# ai_cover_letter_backend

```
ai_cover_letter_backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── security.py
│   │   └── dependencies.py #
│   ├── models/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── user.py #
│   │   ├── profile.py #
│   │   └── cover_letter.py #
│   ├── services/
│   │   ├── __init__.py
│   │   ├── supabase_client.py
│   │   └── openai_service.py #
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── profile.py #
│   │   ├── cover_letters.py #
│   │   └── stats.py #
│   └── utils/
│       ├── __init__.py
│       └── prompts.py
├── .env.example
├── requirements.txt
└── README.md
```

---

## app/__init__.py
```python
from fastapi import FastAPI
from .core.config import settings
from .routers import auth, profile, cover_letters, stats

app = FastAPI(title="AI Cover Letter API", version="1.0.0")

# include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(profile.router, prefix="/profile", tags=["profile"])
app.include_router(cover_letters.router, prefix="/cover_letters", tags=["cover_letters"])
app.include_router(stats.router, prefix="/stats", tags=["stats"])

@app.get("/")
async def root():
    return {"message": "AI Cover Letter Generator API"}
```

## app/main.py
```python
import uvicorn
from . import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

### app/core/config.py
```python
from functools import lru_cache
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    SUPABASE_URL: str = Field(..., env="SUPABASE_URL")
    SUPABASE_KEY: str = Field(..., env="SUPABASE_KEY")
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    JWT_ALG: str = "RS256"
    JWT_ISS: str = "supabase"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
```

### app/core/security.py
```python
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt import PyJWKClient
from .config import settings
from .dependencies import get_supabase

bearer_scheme = HTTPBearer()

async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    supabase = Depends(get_supabase),
):
    try:
        jwk_client = PyJWKClient(f"{settings.SUPABASE_URL}/auth/v1/keys")
        signing_key = jwk_client.get_signing_key_from_jwt(token.credentials)
        payload = jwt.decode(
            token.credentials,
            signing_key.key,
            algorithms=[settings.JWT_ALG],
            audience=None,
            issuer=settings.JWT_ISS,
        )
        user_id: str = payload["sub"]
        # fetch user profile if needed
        return {"id": user_id, "email": payload.get("email")}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
```

### app/core/dependencies.py
```python
from .config import settings
from supabase import create_client, Client
from functools import lru_cache

@lru_cache()
def get_supabase() -> Client:
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
```

---

### app/models/auth.py
```python
from pydantic import BaseModel, EmailStr

class SignUpRequest(BaseModel):
    email: EmailStr
    password: str

class SignInRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
```

### app/models/user.py
```python
from pydantic import BaseModel, EmailStr
from typing import Optional, List

class User(BaseModel):
    id: str
    email: EmailStr

class UserProfileUpdate(BaseModel):
    name: Optional[str]
    skills: Optional[List[str]]
    summary: Optional[str]
```

### app/models/profile.py
```python
from pydantic import BaseModel
from typing import List, Optional

class Profile(BaseModel):
    user_id: str
    name: Optional[str]
    skills: List[str] = []
    summary: Optional[str]
```

### app/models/cover_letter.py
```python
from pydantic import BaseModel, Field
from datetime import datetime

class CoverLetterRequest(BaseModel):
    company_name: str
    job_title: str
    job_description: str

class CoverLetterResponse(BaseModel):
    id: str
    company_name: str
    job_title: str
    content: str
    created_at: datetime
    estimated_time_saved_minutes: int = Field(30, const=True)
```

---

### app/services/supabase_client.py
```python
from .config import settings
from supabase import create_client, Client
from functools import lru_cache

@lru_cache()
def supabase_client() -> Client:
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
```

### app/services/openai_service.py
```python
import openai
from ..core.config import settings
from ..models.cover_letter import CoverLetterRequest
from ..utils.prompts import build_cover_letter_prompt

openai.api_key = settings.OPENAI_API_KEY

async def generate_cover_letter(req: CoverLetterRequest, profile: dict) -> str:
    prompt = build_cover_letter_prompt(profile, req)
    response = await openai.ChatCompletion.acreate(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}],
    )
    return response.choices[0].message.content.strip()
```

---

### app/utils/prompts.py
```python
from ..models.cover_letter import CoverLetterRequest

def build_cover_letter_prompt(profile: dict, req: CoverLetterRequest) -> str:
    skills = ", ".join(profile.get("skills", []))
    return (
        "You are an expert career coach. Using the information provided, write a professional, engaging cover letter.\n\n"
        f"Candidate Name: {profile.get('name','')}\n"
        f"Candidate Skills: {skills}\n"
        f"Candidate Summary: {profile.get('summary','')}\n\n"
        f"Company: {req.company_name}\n"
        f"Job Title: {req.job_title}\n"
        f"Job Description: {req.job_description}\n\n"
        "Respond with only the cover letter body, without salutations or closings."
    )
```

---

### app/routers/auth.py
```python
from fastapi import APIRouter, Depends, HTTPException, status
from ..models.auth import SignUpRequest, SignInRequest, TokenResponse
from ..core.dependencies import get_supabase

router = APIRouter()

@router.post("/signup", response_model=TokenResponse)
async def signup(payload: SignUpRequest, supabase = Depends(get_supabase)):
    result = supabase.auth.sign_up({"email": payload.email, "password": payload.password})
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"]["message"])
    session = result["session"]
    return TokenResponse(access_token=session["access_token"])

@router.post("/login", response_model=TokenResponse)
async def login(payload: SignInRequest, supabase = Depends(get_supabase)):
    result = supabase.auth.sign_in_with_password({"email": payload.email, "password": payload.password})
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"]["message"])
    session = result["session"]
    return TokenResponse(access_token=session["access_token"])
```

### app/routers/profile.py
```python
from fastapi import APIRouter, Depends, HTTPException
from ..core.security import get_current_user
from ..core.dependencies import get_supabase
from ..models.profile import Profile, UserProfileUpdate

router = APIRouter()

@router.get("/me", response_model=Profile)
async def get_profile(current_user=Depends(get_current_user), supabase = Depends(get_supabase)):
    res = supabase.table("profiles").select("*").eq("user_id", current_user["id"]).single().execute()
    if res.error:
        raise HTTPException(status_code=400, detail=res.error.message)
    return res.data

@router.put("/me", response_model=Profile)
async def update_profile(payload: UserProfileUpdate, current_user=Depends(get_current_user), supabase = Depends(get_supabase)):
    update_data = payload.dict(exclude_unset=True)
    res = supabase.table("profiles").update(update_data).eq("user_id", current_user["id"]).execute()
    if res.error:
        raise HTTPException(status_code=400, detail=res.error.message)
    return res.data[0]
```

### app/routers/cover_letters.py
```python
from fastapi import APIRouter, Depends, HTTPException, status
from ..core.security import get_current_user
from ..core.dependencies import get_supabase
from ..models.cover_letter import CoverLetterRequest, CoverLetterResponse
from ..services.openai_service import generate_cover_letter

router = APIRouter()

@router.get("/", response_model=list[CoverLetterResponse])
async def list_cover_letters(current_user=Depends(get_current_user), supabase = Depends(get_supabase)):
    res = supabase.table("cover_letters").select("*").eq("user_id", current_user["id"]).order("created_at", desc=True).execute()
    if res.error:
        raise HTTPException(status_code=400, detail=res.error.message)
    return res.data

@router.post("/", response_model=CoverLetterResponse, status_code=status.HTTP_201_CREATED)
async def create_cover_letter(payload: CoverLetterRequest, current_user=Depends(get_current_user), supabase = Depends(get_supabase)):
    # get profile
    profile_res = supabase.table("profiles").select("*").eq("user_id", current_user["id"]).single().execute()
    if profile_res.error:
        raise HTTPException(status_code=400, detail="Profile not found")
    content = await generate_cover_letter(payload, profile_res.data)
    insert_res = supabase.table("cover_letters").insert({
        "user_id": current_user["id"],
        "company_name": payload.company_name,
        "job_title": payload.job_title,
        "job_description": payload.job_description,
        "content": content,
    }).execute()
    if insert_res.error:
        raise HTTPException(status_code=400, detail=insert_res.error.message)
    created = insert_res.data[0]
    created["estimated_time_saved_minutes"] = 30
    return created

@router.get("/{cover_id}", response_model=CoverLetterResponse)
async def get_cover_letter(cover_id: str, current_user=Depends(get_current_user), supabase = Depends(get_supabase)):
    res = supabase.table("cover_letters").select("*").eq("id", cover_id).eq("user_id", current_user["id"]).single().execute()
    if res.error:
        raise HTTPException(status_code=404, detail="Cover letter not found")
    data = res.data
    data["estimated_time_saved_minutes"] = 30
    return data
```

### app/routers/stats.py
```python
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta
from ..core.security import get_current_user
from ..core.dependencies import get_supabase

router = APIRouter()

@router.get("/", response_model=dict)
async def get_stats(current_user=Depends(get_current_user), supabase = Depends(get_supabase)):
    now = datetime.utcnow()
    since = now - timedelta(days=14)
    total_res = supabase.table("cover_letters").select("id", count="exact").eq("user_id", current_user["id"]).execute()
    recent_res = supabase.table("cover_letters").select("id", count="exact").eq("user_id", current_user["id"]).gte("created_at", since.isoformat()).execute()
    if total_res.error or recent_res.error:
        raise HTTPException(status_code=400, detail="Could not fetch stats")
    total = total_res.count or 0
    recent = recent_res.count or 0
    time_saved = total * 30
    return {"total_generated": total, "generated_last_14_days": recent, "estimated_minutes_saved": time_saved}
```

---

### app/routers/__init__.py
```python
from . import auth, profile, cover_letters, stats  # noqa: F401
```

---

### app/services/__init__.py
```python
# Intentionally left blank for import convenience
```

### app/utils/__init__.py
```python
# Utility package initializer
```

---

## requirements.txt
```
fastapi
uvicorn[standard]
supabase
python-jose[jwt]
openai
python-dotenv
pydantic
```

---

## .env.example
```
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_KEY=service_role_or_anon_key
OPENAI_API_KEY=sk-...
```

---

## README.md
```markdown
# AI Cover Letter Generator Backend

This FastAPI backend provides a REST API for user authentication, profile management, and AI‑powered cover‑letter generation using OpenAI and Supabase.

## Quick Start

1. Copy `.env.example` to `.env` and fill in credentials.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Architecture
- **FastAPI** for HTTP API endpoints
- **Supabase** for database + auth
- **OpenAI** for LLM‑powered text generation
- **JWT** verification via Supabase public JWKs
