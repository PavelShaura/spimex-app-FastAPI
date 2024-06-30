import uvicorn
from fastapi import FastAPI
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.routes.check_and_update_route import check_and_update_router

app = FastAPI(title="Spimex App")


app.include_router(check_and_update_router)


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url(
        settings.REDIS_HOST, encoding="utf8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


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
