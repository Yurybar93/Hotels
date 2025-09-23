from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.init import redis_connector
from src.api.hotels import router as hotels_router
from src.api.auth import router as auth_router
from src.api.rooms import router as rooms_router
from src.api.bookings import router as bookings_router
from src.api.facilities import router as facilities_router
from src.api.image import router as image_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_connector.connect()
    FastAPICache.init(RedisBackend(redis_connector.redis), prefix="fastapi-cache")

    yield
    await redis_connector.close()


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(bookings_router)
app.include_router(facilities_router)
app.include_router(image_router)

# from fastapi.openapi.docs import get_swagger_ui_html
# from fastapi.middleware.cors import CORSMiddleware
# @app.get("/docs", include_in_schema=False)
# async def custom_swagger_ui_html():
#     return get_swagger_ui_html(
#         openapi_url=app.openapi_url,  # type: ignore
#         title=app.title + " - Swagger UI",  # type: ignore
#         oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,  # type: ignore
#         swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
#         swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
#     )

# app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"])

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", reload=True)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
