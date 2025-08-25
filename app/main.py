import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from contextlib import asynccontextmanager
from core import settings, logger
from core.minio_helper import minio_helper
from core.redis_helper import redis_helper
from core.mongo_helper import mongo_helper

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application is starting")
    
    minio_helper.connect()
    await redis_helper.connect()
    await mongo_helper.connect()
    
    yield
    
    logger.info("Application is shutting down")
    minio_helper.disconnect()
    await redis_helper.disconnect()
    await mongo_helper.disconnect()

app = FastAPI(lifespan=lifespan, default_response_class=ORJSONResponse)

@app.get("/health")
async def health_check():
    return {
        "status": "OK",
        "redis": redis_helper.connected,
        "mongo": mongo_helper.connected,
        "minio": minio_helper.connected
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app", host=settings.run.host, port=settings.run.port, reload=True
    )