from app.api.routers.dynamics_router import dynamics_router
from app.api.routers.check_and_update_router import check_and_update_router
from app.api.routers.trade_result_router import trade_result_router
from app.api.routers.last_trading_dates_router import last_trading_dates_router

api_routers = [
    dynamics_router,
    check_and_update_router,
    trade_result_router,
    last_trading_dates_router,
]
