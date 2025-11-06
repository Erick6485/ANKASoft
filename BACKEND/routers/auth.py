from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from database.connection import get_db
from database import models, schemas
from utils.auth import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_user_by_username,
    get_user_by_email,
    get_current_active_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])

@router.post("/register", response_model=schemas.UsuarioResponse)
def registrar_usuario(
    usuario: schemas.UsuarioCreate,
    db: Session = Depends(get_db)
):
    """
    Endpoint para registrar un nuevo usuario
    
    Roles disponibles:
    - admin: Acceso total
    - gerente: Gestión de productos y ventas
    - vendedor: Solo lectura
    """
    # Verificar si el username ya existe
    db_user = get_user_by_username(db, usuario.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El username ya está registrado"
        )
    
    # Verificar si el email ya existe
    db_user = get_user_by_email(db, usuario.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    # Crear nuevo usuario
    hashed_password = get_password_hash(usuario.password)
    db_user = models.Usuario(
        username=usuario.username,
        email=usuario.email,
        hashed_password=hashed_password,
        nombre_completo=usuario.nombre_completo,
        rol=usuario.rol
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Endpoint de login - Devuelve un token JWT
    
    Uso:
    - username: Tu nombre de usuario
    - password: Tu contraseña
    
    Respuesta:
    - access_token: Token JWT para usar en peticiones
    - token_type: "bearer"
    - user: Información del usuario
    """
    # Autenticar usuario
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crear token de acceso
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.post("/login-json", response_model=schemas.Token)
def login_json(
    credentials: schemas.UsuarioLogin,
    db: Session = Depends(get_db)
):
    """
    Endpoint de login alternativo con JSON
    
    Request:
    {
        "username": "usuario",
        "password": "contraseña"
    }
    """
    user = authenticate_user(db, credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.get("/me", response_model=schemas.UsuarioResponse)
def obtener_usuario_actual(
    current_user: models.Usuario = Depends(get_current_active_user)
):
    """
    Obtiene información del usuario autenticado actualmente
    
    Requiere token JWT en el header:
    Authorization: Bearer <token>
    """
    return current_user

@router.get("/usuarios", response_model=list[schemas.UsuarioResponse])
def listar_usuarios(
    skip: int = 0,
    limit: int = 100,
    current_user: models.Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Lista todos los usuarios (solo para admins)
    """
    # Verificar que sea admin
    if current_user.rol != models.RolUsuario.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden listar usuarios"
        )
    
    usuarios = db.query(models.Usuario).offset(skip).limit(limit).all()
    return usuarios

