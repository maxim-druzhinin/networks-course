from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
import shutil
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()


class Product(BaseModel):
    id: int
    name: str
    description: str
    icon: Optional[str] = None


class ProductCreate(BaseModel):
    name: str
    description: str


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None




products = {}
next_id = 1



@app.get("/product/{product_id}", response_model=Product)
def get_product(product_id: int):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")

    return products[product_id]


@app.post("/product", response_model=Product)
def create_product(product: ProductCreate):
    global next_id

    new_product = Product(
        id=next_id,
        name=product.name,
        description=product.description
    )

    products[next_id] = new_product
    next_id += 1

    return new_product


@app.put("/product/{product_id}", response_model=Product)
def update_product(product_id: int, product: ProductUpdate):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")

    existing = products[product_id]

    if product.name is not None:
        existing.name = product.name

    if product.description is not None:
        existing.description = product.description

    products[product_id] = existing

    return existing


@app.delete("/product/{product_id}", response_model=Product)
def delete_product(product_id: int):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")

    return products.pop(product_id)


@app.get("/products", response_model=List[Product])
def get_products():
    return list(products.values())


@app.get("/product/{product_id}/image")
def get_image(product_id: int):

    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")

    product = products[product_id]

    if not product.icon:
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(product.icon)


@app.post("/product/{product_id}/image", response_model=Product)
def upload_image(product_id: int, icon: UploadFile = File(...)):

    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")

    file_path = f"images/{product_id}_{icon.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(icon.file, buffer)

    products[product_id].icon = file_path

    return products[product_id]
