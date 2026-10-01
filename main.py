from fastapi import FastAPI
from models import Product

app=FastAPI()

@app.get('/')
def greet():
    return "Welcome to FASTAPI"

# products_list1=[
#     Product(1, "Apple iPhone", "Iphone 18 pro max", 2599, 5),
#     Product(2, "Apple Macbook", "Macbook Pro m6", 1599, 9),
#     Product(3, "Offer Letter", "FAANG", 100000, 1),
#     Product(4, "Home", "Gated", 50000, 10)
#     ]

products_list1 = [
    Product(id=1, name="Apple iPhone", description="Iphone 16 pro max", price=2599.0, quantity=5),
    Product(id=2, name="Apple Macbook", description="Macbook Pro m6", price=1599.0, quantity=9)
]

@app.get('/products')
def products():
    return products_list1

@app.get('/product/{id}')
def product_by_id(id: int):
    # return products_list1[id-1]
    for product in products_list1:
        if product.id==id: return product
    return "product not found"

@app.post('/product')
def add_product(product: Product):
    products_list1.append(product)
    return product

@app.put('/product/{id}')
def update_product(id: int, product: Product):
    for i in range(len(products_list1)):
        if products_list1[i].id==id:
            products_list1[i] = product
            return {
                "status": "Updated",
                "message": products_list1[i]
            }
    return "Product not found"

@app.delete('/product/{id}')
def delete_product(id: int):
    for index, product in enumerate(products_list1):
        if product.id == id:
            deleted_product = products_list1.pop(index)
            return {"message": "Product deleted successfully", "deleted_product": deleted_product}

    return "Product not found"