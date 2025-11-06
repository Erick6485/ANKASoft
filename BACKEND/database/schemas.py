from pydantic import BaseModel
from datetime import date
from typing import Optional
from enum import Enum

class GeneroClienteEnum(str, Enum):
    MUJER = "mujer"
    HOMBRE = "hombre" 
    NIÑO = "niño"
    NIÑA = "niña"

class ProductoBase(BaseModel):
    nombre: str
    categoria: str
    genero_cliente: GeneroClienteEnum
    talla: str
    precio: float
    stock_actual: int = 0
    stock_minimo: int = 5

class ProductoCreate(ProductoBase):
    pass

class ProductoResponse(ProductoBase):
    id: int
    
    class Config:
        from_attributes = True

class SucursalBase(BaseModel):
    nombre: str
    ciudad: str
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    activa: bool = True

class SucursalCreate(SucursalBase):
    pass

class SucursalResponse(SucursalBase):
    id: int
    
    class Config:
        from_attributes = True

class VentaBase(BaseModel):
    producto_id: int
    fecha: date
    cantidad: int
    sucursal_id: int
    total: float

class VentaCreate(VentaBase):
    pass

class VentaResponse(VentaBase):
    id: int
    producto: Optional[ProductoResponse] = None
    sucursal: Optional[SucursalResponse] = None
    
    class Config:
        from_attributes = True

class KPIFilters(BaseModel):
    mes: Optional[int] = None
    categoria: Optional[str] = None
    genero: Optional[GeneroClienteEnum] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None

