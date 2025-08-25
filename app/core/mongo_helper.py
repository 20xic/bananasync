from motor.motor_asyncio import AsyncIOMotorClient
from core import settings, logger

class MongoDBHelper:
    def __init__(self):
        self.client: AsyncIOMotorClient = None
        self.db = None
        self.connected = False

    async def connect(self):
        try:
            self.client = AsyncIOMotorClient(settings.mongo.dsn)
            await self.client.admin.command('ping')
            self.db = self.client[settings.mongo.db_name]
            self.connected = True
            logger.info("MongoDB connected successfully")
        except Exception as e:
            logger.error(f"MongoDB connection error: {e}")
            raise

    async def disconnect(self):
        if self.client:
            self.client.close()
        self.connected = False
        logger.info("MongoDB disconnected")

    async def get_db(self):
        if not self.connected:
            await self.connect()
        return self.db

mongo_helper = MongoDBHelper()