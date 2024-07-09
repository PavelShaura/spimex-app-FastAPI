import uvicorn
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import api_routers
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App is starting up...")
    redis = aioredis.from_url(
        settings.REDIS_HOST, encoding="utf8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    FastAPICache.init(InMemoryBackend())
    yield
    print("App is shutting down...")


app = FastAPI(lifespan=lifespan, title="Spimex App")

for router in api_routers:
    app.include_router(router)

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
