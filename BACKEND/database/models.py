from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
import enum
from database.connection import Base

class GeneroCliente(enum.Enum):
    MUJER = "mujer"
    HOMBRE = "hombre"
    NIÑO = "niño"
    NIÑA = "niña"

class Producto(Base):
    __tablename__ = "productos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    categoria = Column(String(50), nullable=False)
    genero_cliente = Column(Enum(GeneroCliente), nullable=False)
    talla = Column(String(10), nullable=False)
    precio = Column(Float, nullable=False)
    stock_actual = Column(Integer, default=0)
    stock_minimo = Column(Integer, default=5)

class Sucursal(Base):
    __tablename__ = "sucursales"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    ciudad = Column(String(50), nullable=False)
    direccion = Column(String(200))
    telefono = Column(String(20))
    activa = Column(Boolean, default=True)

class Venta(Base):
    __tablename__ = "ventas"
    
    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"))
    fecha = Column(Date, nullable=False)
    cantidad = Column(Integer, nullable=False)
    sucursal_id = Column(Integer, ForeignKey("sucursales.id"))
    total = Column(Float, nullable=False)
    
    producto = relationship("Producto")
    sucursal = relationship("Sucursal")

