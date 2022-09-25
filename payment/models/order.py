from redis_om import HashModel
from database.redis import redis

class Order(HashModel):
  product_id: str
  price: float
  profit: float
  total_price: float
  quantity: int
  status: str  # pending, completed, refunded

  class Meta:
    database = redis