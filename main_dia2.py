from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Mi API de productos")


class ProductoBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    precio: float = Field(gt=0)
    descripcion: str | None = None


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(BaseModel):
    nombre: str = Field(default=None, min_length=1, max_length=100)
    precio: float = Field(default=None, gt=0)
    descripcion: str | None = None


class ProductoRead(ProductoBase):
    id: int


def buscar_producto(producto_id: int) -> ProductoRead:
    for producto in productos:
        if producto.id == producto_id:
            return producto
    raise HTTPException(status_code=404, detail="Producto no encontrado")


productos: list[ProductoRead] = []
siguiente_id = 1


@app.get("/")
def inicio():
    return {"mensaje": "Hola, FastAPI"}


@app.post("/productos", response_model=ProductoRead, status_code=201)
def create_producto(producto: ProductoCreate):
    global siguiente_id
    nuevo = ProductoRead(id=siguiente_id, **producto.model_dump())
    productos.append(nuevo)
    siguiente_id = siguiente_id + 1
    return nuevo


@app.get("/productos", response_model=list[ProductoRead])
def lista():
    return productos


@app.get("/productos/{producto_id}", response_model=ProductoRead)
def detalle_producto(producto_id: int):
    return buscar_producto(producto_id)


@app.patch("/productos/{producto_id}", response_model=ProductoRead)
def actualizar_producto(producto_id: int, datos: ProductoUpdate):
    prod = buscar_producto(producto_id)
    cambios = datos.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        setattr(prod, campo, valor)
    return prod


@app.delete("/productos/{producto_id}", status_code=204)
def eliminar_producto(producto_id: int):
    producto = buscar_producto(producto_id)
    productos.remove(producto)
