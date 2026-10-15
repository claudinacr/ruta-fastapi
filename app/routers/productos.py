from fastapi import APIRouter, HTTPException

from app.schemas.producto import ProductoCreate, ProductoRead, ProductoUpdate

router = APIRouter(prefix="/productos", tags=["productos"])


def buscar_producto(producto_id: int) -> ProductoRead:
    for producto in productos:
        if producto.id == producto_id:
            return producto
    raise HTTPException(status_code=404, detail="Producto no encontrado")


productos: list[ProductoRead] = []
siguiente_id = 1


@router.post("", response_model=ProductoRead, status_code=201)
def create_producto(producto: ProductoCreate):
    global siguiente_id
    nuevo = ProductoRead(id=siguiente_id, **producto.model_dump())
    productos.append(nuevo)
    siguiente_id = siguiente_id + 1
    return nuevo


@router.get("", response_model=list[ProductoRead])
def lista():
    return productos


@router.get("/{producto_id}", response_model=ProductoRead)
def detalle_producto(producto_id: int):
    return buscar_producto(producto_id)


@router.patch("/{producto_id}", response_model=ProductoRead)
def actualizar_producto(producto_id: int, datos: ProductoUpdate):
    prod = buscar_producto(producto_id)
    cambios = datos.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        setattr(prod, campo, valor)
    return prod


@router.delete("/{producto_id}", status_code=204)
def eliminar_producto(producto_id: int):
    producto = buscar_producto(producto_id)
    productos.remove(producto)
