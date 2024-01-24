from fastapi import FastAPI
from fastapi.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

# for logging middleware
import logging
from fastapi import Request
import time

from api.full import router as full_router
from api.health import router as health_router
from api.state import router as state_router
from api.status import router as status_router
from api.job import router as job_router

from core.config import get_settings

settings = get_settings()

if settings.sentry_dsn:
    import sentry_sdk

    sentry_sdk.init(settings.sentry_dsn)

# backgound livespan task
# from services.job import backgound_mock_behavior


middlewares = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
]

app = FastAPI(
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    redoc_url="/api/redoc",
    middleware=middlewares,
    # lifespan=backgound_mock_behavior,
)


# add logger middleware

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next: callable):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    formatted_process_time = "{0:.4f}".format(process_time)
    logger.info(f"{request.method} {request.url} {formatted_process_time}s")
    response.headers["X-Process-Time"] = formatted_process_time
    return response


# include routers
app.include_router(health_router, prefix="")
app.include_router(job_router, prefix="/api")
app.include_router(full_router, prefix="/api")
app.include_router(status_router, prefix="/api")
app.include_router(state_router, prefix="/api")
