<div align="center">
  <h1>🛡️ Sistema de Reconocimiento y Autenticación Facial</h1>
  <p>
    <strong>Práctica Final - Tecnologías de la Autenticación</strong><br>
    <em>Máster de Investigación en Ciberseguridad | Universidad de León</em>
  </p>
</div>

---

## 📖 Descripción del Sistema

Este proyecto implementa un sistema de reconocimiento facial diseñado para capturar rostros desde un flujo de vídeo en directo y posteriormente autenticar usuarios registrados. Además, el sistema incorpora medidas de seguridad contra ataques de suplantación (spoofing), como la presentación de fotografías impresas o vídeos pregrabados frente a la cámara.

⚠️ **Nota sobre dependencias:** Este proyecto utiliza de manera intencionada versiones antiguas de **OpenCV**, **NumPy** y **modelos pre-entrenados de OpenCV** (como clasificadores en cascada) para mantener la compatibilidad y seguir la línea de trabajo marcada en las sesiones prácticas de la asignatura.

## 🚀 Modo de Uso

### Captura de Caras (`captura-caras.py`)
Actualmente, el script principal disponible es `captura-caras.py`, el cual se encarga de extraer y guardar las imágenes del rostro de un usuario desde la webcam.

**Ejecución básica (interactiva):**
```bash
python captura-caras.py
```
*(Puedes seguir las instrucciones en pantalla para introducir el nombre del usuario y el número de capturas deseadas).*

**Ejecución con parámetros (ideal para automatizar):**
```bash
python captura-caras.py NombreUsuario 300
```

---

## 📝 Enunciado de la Práctica

El desarrollo de este proyecto se divide en las siguientes fases según los requisitos solicitados:

1. **Captura automática:** Entregar un script que permita obtener las imágenes del rostro de un usuario registrado de forma automática a partir de un vídeo en streaming.
2. **Reconocimiento facial:** Presentar un sistema de reconocimiento facial previamente entrenado con los rostros de los miembros del grupo, capaz de distinguir a un usuario registrado de uno que no lo está. 
   - **Usuario registrado:** Mostrará su nombre y un recuadro verde alrededor del rostro al ser identificado.
   - **Usuario no registrado:** Cuando el sistema detecte el rostro de una persona no registrada en la base de datos (por ejemplo, el profesor), indicará que no está registrado y dibujará un recuadro rojo alrededor de su rostro.

### 🛡️ Parte Avanzada (3 puntos): Lucha contra el Hacking (Anti-Spoofing)

El sistema debe ser capaz de luchar contra ciertos intentos de engaño y rechazar la autenticación:

1. **Detección de imagen:** Se presentará una fotografía impresa de un usuario autenticado de forma estática frente a la cámara. El sistema debe detectar que no hay una persona viva, informar de que es una imagen y **no autenticar**.
2. **Detección de vídeo:** Se reproducirá un vídeo de una persona autenticada frente a la cámara mediante una pantalla (móvil, tablet u ordenador). El sistema debe detectar que hay un dispositivo reproduciendo un vídeo y no la persona real, mostrando que el usuario no se encuentra físicamente y **no autenticar**.

---

## ✅ Roadmap (Lista de Tareas)

- [x] 1. Capturar caras de vídeo en streaming (`captura-caras.py`)
- [ ] 2. Crear sistema de reconocimiento facial
- [ ] 3. Identificar a un usuario registrado (recuadro verde + nombre)
- [ ] 4. Identificar a un usuario NO registrado (recuadro rojo + aviso)
- [ ] 5. Lucha contra Hacking: Detección de ataque con imagen estática (Anti-spoofing)
- [ ] 6. Lucha contra Hacking: Detección de ataque con reproducción de vídeo (Anti-spoofing)

---

## 📜 Licencia

Este proyecto está distribuido bajo la licencia **BSD 3-Clause**. Consulta el archivo [LICENSE](LICENSE) para más detalles.
