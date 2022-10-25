from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database import Base, engine
from src.emails.proxy.router import router as proxy_router
from src.emails.forwards.router import router as forward_router
from src.auth.router import router as auth_router

Base.metadata.create_all(engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(proxy_router, prefix="/proxies", tags=["Proxies"])
app.include_router(forward_router, prefix="/forwards", tags=["Forwards"])
