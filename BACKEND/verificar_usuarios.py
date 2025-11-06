from utils.auth import get_password_hash, verify_password
from database.connection import SessionLocal
from database.models import Usuario

db = SessionLocal()

print("=" * 60)
print("VERIFICACIÓN DE USUARIOS")
print("=" * 60)

usuarios = db.query(Usuario).all()

for usuario in usuarios:
    print(f"\n👤 Usuario: {usuario.username}")
    print(f"   Email: {usuario.email}")
    print(f"   Rol: {usuario.rol.value}")
    print(f"   Hash en DB: {usuario.hashed_password[:50]}...")
    
    # Verificar contraseña
    password_test = f"{usuario.username}123"
    hash_test = get_password_hash(password_test)
    
    print(f"   Password esperada: {password_test}")
    print(f"   Hash esperado: {hash_test[:50]}...")
    print(f"   ¿Coinciden? {verify_password(password_test, usuario.hashed_password)}")

db.close()

print("\n" + "=" * 60)
print("CONCLUSIÓN")
print("=" * 60)
print("\nCredenciales de login:")
print("  - admin / admin123")
print("  - gerente / gerente123")
print("  - vendedor / vendedor123")

