import redis
import json
from typing import Optional, List, Any
from datetime import timedelta

redis_client = redis.Redis(
    host='localhost', 
    port=6379, 
    db=0, 
    decode_responses=True,
    password=None
)

def set_cache(key: str, value: Any, expire: int = 300) -> None:
    redis_client.setex(key, expire, json.dumps(value, default=str))

def get_cache(key: str) -> Optional[Any]:
    data = redis_client.get(key)
    return json.loads(data) if data else None

def delete_cache(pattern: str) -> None:
    for key in redis_client.scan_iter(pattern):
        redis_client.delete(key)

    