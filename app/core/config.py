from pydantic import BaseModel, PostgresDsn, computed_field, AnyUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import quote_plus
from datetime import timedelta
from typing import Optional, Any

class RunConfig(BaseModel):
    host: str = "localhost"
    port: int = 9999

class Logger(BaseModel):
    level: str = "INFO"
    name: str = "APP"

class ApiPrefix(BaseModel):
    prefix: str = "/api"

class MinioConfig(BaseModel):
    host: str = "localhost"
    port: int = 9000
    access_key: str = "minioadmin"
    secret_key: str = "minioadmin"
    secure: bool = False
    bucket_name: str = "default"
    health_check_path: str = "/minio/health/live"

    @computed_field
    @property
    def endpoint(self) -> str:
        return f"{self.host}:{self.port}"

class RedisConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: Optional[str] = None
    username: Optional[str] = None

    @computed_field
    @property
    def dsn(self) -> str:
        if self.password:
            return f"redis://{self.username}:{self.password}@{self.host}:{self.port}/{self.db}"
        return f"redis://{self.host}:{self.port}/{self.db}"

class MongoDBConfig(BaseModel):
    host: str = "localhost"
    port: int = 27017
    db_name: str = "app_db"
    username: Optional[str] = None
    password: Optional[str] = None

    @computed_field
    @property
    def dsn(self) -> str:
        if self.username and self.password:
            return f"mongodb://{self.username}:{quote_plus(self.password)}@{self.host}:{self.port}/{self.db_name}?authSource=admin"
        return f"mongodb://{self.host}:{self.port}/{self.db_name}"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="DOCUMENT_SERVICE__",
        extra="ignore"
    )
    
    run: RunConfig = RunConfig()
    logger: Logger = Logger()
    api: ApiPrefix = ApiPrefix()
    minio: MinioConfig = MinioConfig()
    redis: RedisConfig = RedisConfig()
    mongo: MongoDBConfig = MongoDBConfig()

settings = Settings()