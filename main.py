from fastapi import FastAPI
from fastapi.responses import JSONResponse
from alembic.config import Config
from alembic import command
import logging
import os
import asyncio

from database import ENGINE,BaseModel
from api.v1.user import user
from api.v1.post import post
from settings import ENVIRONMENT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_migrations():
    '''
    run the migrations
    '''
    path_config = os.path.join(os.getcwd(),ENVIRONMENT.ALEMBIC_CONFIG_FILE_PATH)
    alembic_cfg = Config(path_config)
    command.upgrade(alembic_cfg,'head')

app = FastAPI(
    title='FastAPI Job Application Test',
    description='Challenge',
    version=ENVIRONMENT.API_VERSION
)

@app.on_event('startup')
async def startup():
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None,run_migrations)
    async with ENGINE.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

@app.on_event('shutdown')
async def shutdown():
    await ENGINE.dispose()

app.include_router(user.router,prefix=ENVIRONMENT.GLOBAL_API_PREFIX)
app.include_router(post.router,prefix=ENVIRONMENT.GLOBAL_API_PREFIX)

@app.exception_handler(404)
async def not_found_exception_handler(request,exc):
    return JSONResponse(
        status_code=404,
        content={'message':'Resource not found'}
    )

@app.exception_handler(505)
async def internal_exception_handler(request,exc):
    return JSONResponse(
        status_code=500,
        content={'message':'An unexpected internal error has ocurred'}
    )