import logging
from enum import Enum

from pydantic import BaseModel


class ProductType2(str, Enum):
    CLOTHING = "clothing"
    ELECTRONICS = "electronics"
    FOOD = "food"


class Product2(BaseModel):
    name: str
    price: float
    in_stock: bool = False
    product_type: ProductType2


product_elect = Product2(name="Mouse", price="355.0", in_stock=True, product_type=ProductType2.ELECTRONICS)
product_food = Product2(name="Banana", price=9.95, product_type=ProductType2.FOOD)

json_data_elect = product_elect.model_dump_json()
json_data_food = product_food.model_dump_json(exclude_unset=True)

print(f"{json_data_elect=}")
print(f"{json_data_food=}")
print("-" * 140)
print(f"{product_elect=}")
print(f"{product_food=}")
print("-" * 140)

not_json_elect = Product2.model_validate_json(json_data_elect)
not_json_food = Product2.model_validate_json(json_data_food)
print(f"{not_json_elect=}")
print(f"{not_json_food=}")
