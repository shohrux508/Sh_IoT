from pydantic import BaseModel, ValidationError, Field


class User(BaseModel):
    id: int
    name: str
    is_active: bool = True


try:
    User(id=1, name='shohrux')
except ValidationError as e:
    print(f"e: {e}")


class Product(BaseModel):
    name: str
    price: float = Field(..., gt=-2, description='Цена должна быть больше нуля!', alias='super')


product = Product(name='product1', super=-1)
product2 = Product(name='product2', super=0)
print(product)
print(product2)
