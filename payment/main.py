import requests, time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from starlette.requests import Request

from models.order import Order
from database.redis import redis

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:3000"],
  allow_methods=["*"],
  allow_headers=["*"],
  )

@app.get("/orders/{pk}")
def get(pk: str):
  return Order.get(pk)

@app.post("/orders")
async def create(request: Request, background_tasks: BackgroundTasks):
  body = await request.json()
  req = requests.get("http://localhost:8000/products/%s" % body["id"])
  product = req.json()

  order = Order(
    product_id=body["id"],
    price=product["price"],
    profit=0.2 * product["price"],
    total_price=1.2 * product["price"],
    quantity=body["quantity"],
    status="Pending"
  )
  order.save()
  
  background_tasks.add_task(order_completed, order)

  return order

def order_completed(order: Order):
  time.sleep(3)
  order.status = "Completed"
  order.save()
  # redis stream - * -> auto-generated id
  redis.xadd("order_completed", order.dict(), "*")