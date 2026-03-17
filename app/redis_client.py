import redis
import orjson
from typing import Optional, Any, List, Dict, Union
from contextlib import contextmanager

class RedisClient:
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0, **kwargs):
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=False, **kwargs)
        self.ping()

    def ping(self) -> bool:
        try:
            return self.client.ping()
        except redis.ConnectionError:
            raise Exception("Redis connection failed")

    def get(self, key: str) -> Optional[bytes]:
        return self.client.get(key)

    def setex(self, key: str, seconds: int, value: Union[bytes, str, Dict, List]):
        if isinstance(value, (dict, list)):
            value = orjson.dumps(value)
        elif isinstance(value, str):
            value = value.encode('utf-8')
        return self.client.setex(key, seconds, value)

    def delete(self, key: str) -> int:
        return self.client.delete(key)

    def exists(self, key: str) -> bool:
        return self.client.exists(key) > 0

    def keys(self, pattern: str = '*') -> List[bytes]:
        return self.client.keys(pattern)

    def flushall(self):
        self.client.flushall()

    def set(self, key: str, value: Union[bytes, str, Dict, List], ex: Optional[int] = None):
        if isinstance(value, (dict, list)):
            value = orjson.dumps(value)
        elif isinstance(value, str):
            value = value.encode('utf-8')
        self.client.set(key, value, ex)

    def get_json(self, key: str) -> Optional[Dict]:
        data = self.get(key)
        return orjson.loads(data) if data else None

    def mget(self, keys: List[str]) -> List[Optional[bytes]]:
        return self.client.mget(keys)

    @contextmanager
    def pipeline(self):
        pipe = self.client.pipeline()
        try:
            yield pipe
            pipe.execute()
        finally:
            pipe.close()

redis_client = RedisClient()

    