import os
from redis_om import get_redis_connection
from dotenv import load_dotenv

load_dotenv()

redis = get_redis_connection(
  host="redis-13731.c293.eu-central-1-1.ec2.cloud.redislabs.com",
  port=13731,
  password=os.getenv("REDIS_PASS"),
  decode_responses=True
)