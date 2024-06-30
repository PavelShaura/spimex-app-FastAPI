from fastapi import APIRouter

api_router = APIRouter(prefix="/api/v1", tags=["API"])


@api_router.get("/last_trading_dates")
async def get_last_trading_dates():
    pass


@api_router.get("/dynamics")
async def get_dynamics():
    pass


@api_router.get("/trading_results")
async def get_trading_results():
    pass
