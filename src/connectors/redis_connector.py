import logging
import redis.asyncio as redis


class RedisConnector:
    _redis: redis.Redis

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
       

    async def connect(self):
        logging.info(f"Connecting to Redis host={self.host}, port={self.port}")
        self.redis = redis.Redis(host=self.host, port=self.port)
        logging.info("Connected to Redis")

    async def set_value(self, key: str, value: str, expire: int | None = None):
        if expire:
            await self.redis.set(key, value, ex=expire)
        else:
            await self.redis.set(key, value)

    async def get_value(self, key: str):
        return await self.redis.get(key)

    async def delete_value(self, key):
        await self.redis.delete(key)

    async def close(self):
        if self.redis:
            await self.redis.close()
