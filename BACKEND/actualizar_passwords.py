from utils.auth import get_password_hash
from database.connection import SessionLocal
from database.models import Usuario

print("=" * 60)
print("ACTUALIZANDO CONTRASEÑAS DE USUARIOS")
print("=" * 60)

db = SessionLocal()

# Actualizar contraseñas
usuarios_passwords = [
    ("admin", "admin123"),
    ("gerente", "gerente123"),
    ("vendedor", "vendedor123")
]

for username, password in usuarios_passwords:
    usuario = db.query(Usuario).filter(Usuario.username == username).first()
    if usuario:
        nuevo_hash = get_password_hash(password)
        usuario.hashed_password = nuevo_hash
        print(f"✅ Actualizado: {username} → nueva contraseña: {password}")
    else:
        print(f"⚠️  Usuario no encontrado: {username}")

db.commit()
db.close()

print("\n" + "=" * 60)
print("✅ CONTRASEÑAS ACTUALIZADAS")
print("=" * 60)
print("\nAhora puedes hacer login con:")
print("  👤 admin / admin123")
print("  👤 gerente / gerente123")
print("  👤 vendedor / vendedor123")
print("\n🌐 Ve a: http://localhost:5173")

