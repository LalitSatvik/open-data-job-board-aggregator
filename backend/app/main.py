from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.config import settings
from app.routers import applications as applications_router
from app.routers import auth as auth_router
from app.routers import ingest as ingest_router
from app.routers import jobs as jobs_router

app = FastAPI(title="Open Data Job Board Aggregator")

app.include_router(ingest_router.router)
app.include_router(auth_router.router)
app.include_router(jobs_router.router)
app.include_router(applications_router.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=settings.jwt_secret)


@app.get("/health")
def health():
    return {"status": "ok"}
