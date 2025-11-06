# 🚀 EJECUTAR PROYECTO AHORA - GUÍA RÁPIDA

---

## ⚡ **PASOS RÁPIDOS**

### **PASO 1: Backend (Terminal 1)**

```powershell
cd C:\Users\ANNY\Desktop\ANKASotf\ANKASoft\BACKEND
.\venv\Scripts\Activate.ps1
pip install python-jose[cryptography] email-validator
python migrar_base_datos.py
python cargar_datos.py
python main.py
```

**Espera ver:**
```
✅ 3 usuarios creados
INFO: Uvicorn running on http://0.0.0.0:8000
```

---

### **PASO 2: Frontend (Terminal 2 - Nueva)**

```powershell
cd C:\Users\ANNY\Desktop\ANKASotf\ANKASoft\frontend
npm run dev
```

**Espera ver:**
```
➜ Local: http://localhost:5173/
```

---

### **PASO 3: Probar (Navegador)**

1. Abre: **http://localhost:5173**
2. **El texto ahora es VISIBLE** (azul oscuro, no blanco)
3. Login: `admin` / `admin123`
4. ¡Debería redirigir al dashboard!

---

## ✅ **CAMBIOS APLICADOS**

### **Diseño:**
- ✅ Paleta azul profesional (#1a3d63, #4a7fa7, #b3cfe5)
- ✅ **Texto visible en inputs** (azul oscuro #0a1931)
- ✅ Gradiente azul en fondo
- ✅ Botones azul oscuro profesional
- ✅ Sidebar con color tema

### **Funcionalidad:**
- ✅ API Key incluida en todas las peticiones
- ✅ JWT Token automático
- ✅ Doble autenticación funcionando

---

## 🎨 **PALETA DE COLORES**

```
#1a3d63  Azul Oscuro Profesional  (Botones, sidebar)
#4a7fa7  Azul Medio              (Acentos, hover)
#b3cfe5  Azul Claro              (Bordes, fondos)
#0a1931  Azul Oscuro Base        (Texto principal)
#f6fafd  Blanco Premium          (Fondos, texto claro)
#d64545  Rojo                    (Alertas)
#00b341  Verde                   (Éxito)
```

---

## 📝 **USUARIOS DE PRUEBA**

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| admin | admin123 | ADMIN |
| gerente | gerente123 | GERENTE |
| vendedor | vendedor123 | VENDEDOR |

---

## ✅ **CHECKLIST**

- [ ] Backend corriendo (localhost:8000)
- [ ] Frontend corriendo (localhost:5173)
- [ ] Usuarios creados en BD
- [ ] Texto visible en inputs (azul oscuro)
- [ ] Login funciona
- [ ] Dashboard carga

---

**¡Ejecuta los comandos y prueba el login!** 🚀✨

