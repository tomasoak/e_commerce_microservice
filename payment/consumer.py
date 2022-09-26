import time
from database.redis import redis
from models.order import Order

key = "refund_order"
group = "payment-group"

try:
  redis.xgroup_create(key, group)
except:
  print("Group already exists!")

while True:
  try:
    results = redis.xreadgroup(group, key, {key: ">"}, None)

    if results != []:
      print(results)
      for result in results:
        obj = result[1][0][1]
        order = Order.get(obj["pk"])
        order.status = "Refunded"
        order.save()

  except Exception as e:
    print(str(e))
  time.sleep(1)