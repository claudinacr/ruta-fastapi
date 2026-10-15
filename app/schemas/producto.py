from fastapi import FastAPI
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
