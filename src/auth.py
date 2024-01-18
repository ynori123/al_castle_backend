import redis
from src.config import setting
from datetime import datetime, timedelta
import uuid
from hashlib import sha256


r = redis.Redis(
    host=setting.REDIS_HOST,
    port=setting.REDIS_PORT,
    password=setting.REDIS_PASSWORD,
    ssl=True
)


def set_token():
    token = (str(uuid.uuid4())).encode()
    now = datetime.now()
    now = f"{now.year}-{now.month}-{now.day} {now.hour}:{now.minute}:{now.second}"
    hashed_token = sha256(token).hexdigest()
    r.set(hashed_token, now)
    return token

def auth_token(token: str):
    token = sha256(token.encode()).hexdigest()
    if r.exists(token):
        current_datetime = datetime.now()
        parsed_datetime = datetime.strptime(r.get(token).decode(), '%Y-%m-%d %H:%M:%S')
        if current_datetime - parsed_datetime <= timedelta(minutes=30):
            r.delete(token)
            return True
        else:
            r.delete(token)
            return False
    else:
        return False
