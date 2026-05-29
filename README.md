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

## ⚙️ Instalación y Requisitos

Para el correcto funcionamiento del sistema, se deben instalar versiones específicas de las siguientes librerías dentro de tu entorno virtual:

```bash
# Instalación de la versión base de OpenCV
pip install opencv-python==3.4.18.65

# Instalación de los módulos extra de OpenCV (necesario para cv2.face)
pip install opencv-contrib-python==3.4.18.65

# NumPy suele instalarse automáticamente como dependencia, pero puedes forzarlo:
pip install "numpy<2"
```

> [!TIP]
> Para más detalles sobre la creación y configuración del entorno, puedes revisar el guion de la **Práctica 1 "Instalación y Segmentación de imágenes"**, disponible en el portal [Ágora (Universidad de León)](https://agora.unileon.es/).

---

## 🚀 Modo de Uso

### 1. Captura de Caras (`captura-caras.py`)
El script `captura-caras.py`, se encarga de extraer y guardar las imágenes del rostro de un usuario desde la webcam.

**Ejecución básica (interactiva):**
```bash
python captura-caras.py
```
*(Puedes seguir las instrucciones en pantalla para introducir el nombre del usuario y el número de capturas deseadas).*

**Ejecución con parámetros (ideal para automatizar):**
```bash
python captura-caras.py NombreUsuario 300
```

### 2. Entrenamiento de Caras (`entrena.py`)
El script `entrena.py` entrena un modelo de reconocimiento facial con las caras capturadas y genera los archivos del modelo (`.yaml`) y etiquetas (`.txt`) en la carpeta `entrenamientos/`.

**Ejecución básica (entrena a todas las personas capturadas):**
```bash
python entrena.py
```

**Ejecución con parámetros (entrena a usuarios específicos):**
```bash
python entrena.py persona1 persona2 persona3
```

### 3. Reconocimiento Facial en Vivo (`reconoce.py`)
El script `reconoce.py` activa la cámara web y evalúa en tiempo real los rostros detectados frente al modelo entrenado, dibujando recuadros verdes (usuarios registrados) o rojos (desconocidos).

**Ejecución básica (carga automáticamente el último modelo entrenado):**
```bash
python reconoce.py
```

**Ejecución especificando un modelo concreto:**
```bash
python reconoce.py modelo-2026-05-14-11-58.yaml
```
*(Para detener la ejecución, haz clic en la ventana emergente de vídeo y pulsa la tecla `q`).*

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
- [x] 2. Crear sistema de reconocimiento facial
- [x] 3. Identificar a un usuario registrado (recuadro verde + nombre)
- [x] 4. Identificar a un usuario NO registrado (recuadro rojo + aviso)
- [x] 5. Lucha contra Hacking: Detección de ataque con imagen estática (Anti-spoofing). Posible estrategia: detección de movimiento y parpadeo.
- [x] 6. Lucha contra Hacking: Detección de ataque con reproducción de vídeo (Anti-spoofing). Posible estrategia: detección de patrones de iluminación, o detección de reflejos, frecuencias o texturas de pantalla.

---

## 🕵 Detección de Hacking ( Anti-spoofing)
Se han tomado varias medidas para evitar ataques de spoofing:

1. **Detección de movimiento en el fondo**:
   Se ha implementado una lógica para detectar movimiento en las líneas rectas del fondo. Si se detecta movimiento en el fondo, se considera un ataque de spoofing. 
   Si se valora todo el fondo, el movimiento sólo se ve en los bordes ya que los píxeles de una pared bien iluminada son iguales a sus vecinos. Al valorar los bordes, se evita este problema.
   Dado que la determinación de qué es fondo viene determinada por lo que no es cara, es probable que haya elementos de la persona como el pelo o las orejas que entren en el conjunto de lo que es fondo. Valorando sólo las líneas rectas excluimos las partes todos los bordes de la imagen de la persona.
2. **Detección de cercanía**:
   Se ha implementado una lógica para detectar si la cara del usuario está demasiado cerca de la cámara. Si la cara ocupa más del 50% de la imagen, se le pide que se aleje.
   Cualquier técnica anti-spoofing que se implemente se ve amenazada cuando la imagen de la cara está muy cerca y ocupa la imagen captada por la cámara. Pidiendo distancia garantizamos que parte de la imagen nos podrá servir para determinar si se está o no usando una cara real.
3. **Estabilidad**:
   Se ha implementado la lógica ncesaria para valorar los últimos 5 segundos teniendo que ser estable en ese periodo tanto el fondo (o las líneas rectas de este como se ha indicado en el punto 1) como la identificación del usuario.
   En específico se guarda una marca de tiempo del último momento en el que se detectó movimiento en el fondo, y un buffer en el que se almacenan los usuarios identificados cada 10 milisegundos.
## 📜 Licencia

Este proyecto está distribuido bajo la licencia **BSD 3-Clause**. Consulta el archivo [LICENSE](LICENSE) para más detalles.
