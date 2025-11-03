from fastapi import Request,Response
from starlette.middleware.base import BaseHTTPMiddleware
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

class TimeLoggerMiddleware(BaseHTTPMiddleware):
    '''
    middleware to measure the time that takes a request to get a response
    '''
    async def dispatch(self,request:Request,call_next):
        time = datetime.now()
        response = await call_next(request)
        logging.info(f'request {request.method} at {request.url} resolved in {datetime.now() - time}')
        return response