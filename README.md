# Galería de Imágenes - Flask App

Una aplicación web moderna para subir, almacenar y visualizar imágenes, construida con Flask y SQLite.

## 🌟 Características

- **Subida de imágenes**: Interfaz intuitiva para cargar múltiples formatos de imagen
- **Almacenamiento en base de datos**: Las imágenes se guardan directamente en SQLite como BLOB
- **Galería responsiva**: Visualización elegante de todas las imágenes subidas
- **Gestión de usuarios**: Sistema básico de identificación de usuarios
- **Diseño moderno**: Interfaz de usuario limpia y responsiva

## 🚀 Demo en Vivo

**Frontend**: [https://python-flask-render-frontend.onrender.com](https://python-flask-render-frontend.onrender.com)

**Backend API**: [https://python-flask-render-136u.onrender.com](https://python-flask-render-136u.onrender.com)

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python Flask
- **Base de datos**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **Deployment**: Render.com
- **Almacenamiento**: Base64 encoding para imágenes en SQLite


### Base de Datos
La aplicación utiliza SQLite con la siguiente estructura:

```sql
CREATE TABLE images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    filename TEXT NOT NULL,
    data BLOB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🚀 Deployment en Render

### Configuración Automática
La aplicación está configurada para deploy automático en Render.com:

1. **Build Command**: `pip install -r requirements.txt`
2. **Start Command**: `python app.py`
3. **Environment**: Python 3

### Variables de Entorno en Render
- `PYTHON_VERSION`: 3.11.4
- `PORT`: (automático)

## 📱 Uso de la Aplicación

1. **Subir imágenes**: 
   - Haz clic en "Seleccionar archivos"
   - Elige una o más imágenes
   - Haz clic en "Subir imagen"

2. **Ver galería**: 
   - Las imágenes aparecen automáticamente en la galería
   - Responsive design para móviles y desktop

3. **Gestión**: 
   - Cada imagen se identifica por usuario
   - Timestamp automático de creación

## 📝 Notas Técnicas

- **Formato de imágenes**: JPG, PNG
- **Límite de tamaño**: Configurable (por defecto sin límite específico)
- **Encoding**: Base64 para almacenamiento en SQLite
- **CORS**: Habilitado para desarrollo

## 🐛 Solución de Problemas

### Error 503 en Render
- Verificar logs en Render dashboard
- Confirmar que todas las dependencias están en requirements.txt
- Validar configuración de puerto

### Imágenes no se muestran
- Verificar que el encoding Base64 sea correcto
- Confirmar que el content-type esté bien configurado

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

Iosef Canchán - [iosef.joelcv@gmail.com](iosef.joelcv@gmail.com)

- Enlace del backend: [https://github.com/tu-usuario/galeria-imagenes](https://github.com/fr0st-even/Python-Flask-Render)
- Enlace del frontend: [https://github.com/tu-usuario/galeria-imagenes](https://github.com/fr0st-even/Python-Flask-Render-FrontEnd)

---
## 🎥 Video Tutorial
Enlace video: [https://drive.google.com/file/d/1JYUrqV_GQKI9e9FRExVlzlP9zGKtDJEs/view?usp=drive_link](https://drive.google.com/file/d/1JYUrqV_GQKI9e9FRExVlzlP9zGKtDJEs/view?usp=drive_link)]
