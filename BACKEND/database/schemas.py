from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from enum import Enum

class GeneroClienteEnum(str, Enum):
    MUJER = "mujer"
    HOMBRE = "hombre" 
    NIÑO = "niño"
    NIÑA = "niña"

class RolUsuarioEnum(str, Enum):
    ADMIN = "admin"
    GERENTE = "gerente"
    VENDEDOR = "vendedor"

# Esquemas de Autenticación
class UsuarioBase(BaseModel):
    username: str
    email: str
    nombre_completo: Optional[str] = None
    rol: RolUsuarioEnum = RolUsuarioEnum.VENDEDOR

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioLogin(BaseModel):
    username: str
    password: str

class UsuarioResponse(UsuarioBase):
    id: int
    activo: bool
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UsuarioResponse

class TokenData(BaseModel):
    username: Optional[str] = None

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

