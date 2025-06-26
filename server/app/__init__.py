from fastapi import FastAPI
from .core.config import settings
from .routers import auth#, profile, cover_letters, stats

app = FastAPI(title="AI Cover Letter API", version="1.0.0")

# include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
#app.include_router(profile.router, prefix="/profile", tags=["profile"])
#app.include_router(cover_letters.router, prefix="/cover_letters", tags=["cover_letters"])
#app.include_router(stats.router, prefix="/stats", tags=["stats"])

@app.get("/")
async def root():
    return {"message": "AI Cover Letter Generator API"}