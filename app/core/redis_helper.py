import redis.asyncio as redis
from core import settings, logger

class RedisHelper:
    def __init__(self):
        self.client: redis.Redis = None
        self.connected = False

    async def connect(self):
        try:
            self.client = redis.from_url(
                settings.redis.dsn,
                encoding="utf-8",
                decode_responses=True
            )
            await self.client.ping()
            self.connected = True
            logger.info("Redis connected successfully")
        except Exception as e:
            logger.error(f"Redis connection error: {e}")
            raise

    async def disconnect(self):
        if self.client:
            await self.client.close()
        self.connected = False
        logger.info("Redis disconnected")

    async def get_client(self) -> redis.Redis:
        if not self.connected:
            await self.connect()
        return self.client

redis_helper = RedisHelper()