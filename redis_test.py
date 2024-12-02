import redis

try:
    client = redis.Redis(host='127.0.0.1', port=6379)
    client.ping()
    print("Redis is connected!")
except redis.ConnectionError as e:
    print(f"Redis connection failed: {e}")
