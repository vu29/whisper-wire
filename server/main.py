from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from server.core.config import settings
from server.core.database import sessionmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    yield
    if sessionmanager.engine is not None:
        # Close the DB connection
        await sessionmanager.close()


app = FastAPI(lifespan=lifespan, title=settings.app_name)

from server.users.router import router as user_router
from server.auth.router import router as auth_router

routers = (user_router,auth_router,)
for router in routers:
    app.include_router(router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
