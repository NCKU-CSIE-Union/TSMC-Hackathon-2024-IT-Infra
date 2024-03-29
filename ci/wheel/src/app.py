from fastapi import FastAPI
from fastapi.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# for logging middleware
from fastapi import Request
import time

from core.api import webhook_router as hook_router

from core.config import get_settings

settings = get_settings()

if settings.sentry_dsn:
    import sentry_sdk

    sentry_sdk.init(settings.sentry_dsn)


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


@app.middleware("http")
async def add_process_time_header(request: Request, call_next: callable):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    formatted_process_time = "{0:.4f}".format(process_time)
    response.headers["X-Process-Time"] = formatted_process_time
    return response


# include routers
app.include_router(hook_router, prefix="/api/v1")

# test static files
# view at http://localhost:8080/api/v1/test/result/index.html
app.mount("/api/v1/test/result", StaticFiles(directory="htmlcov"), name="static")
