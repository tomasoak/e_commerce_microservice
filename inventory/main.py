from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models.product import Product

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:3000"],
  allow_methods=["*"],
  allow_headers=["*"],
  )

@app.get("/products")
def list_products():
  return [format(pk) for pk in Product.all_pks()]

def format(pk: str):
  product = Product.get(pk)

  return {
    "id": product.pk,
    "name": product.name,
    "price": product.price,
    "quantity": product.quantity
    }

@app.post("/products")
def create_products(product: Product):
  return product.save()

@app.get("/products/{pk}")
def get_one_product(pk: str):
  return Product.get(pk)

@app.delete("/products/{pk}")
def delete_one_product(pk: str):
  product = Product.get(pk)
  product_name = product.name

  Product.delete(pk)
  return f"{product_name} deleted"