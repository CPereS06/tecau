import cv2
import os
import sys
import numpy as np
from datetime import datetime

# Leer argumento personas a entrenar, por defecto los que haya en personas
# Tener en cuenta que una persona puede haber realizado varias sesiones de captura
# siempre se usará la última captura realizada.

personas_dir = 'personas'
personas_a_entrenar = sys.argv[1:]

if not os.path.exists(personas_dir):
    print(f"Error: No existe el directorio '{personas_dir}'. Asegúrate de haber capturado caras primero.")
    sys.exit(1)

directorios = os.listdir(personas_dir)

# Agrupar las sesiones por persona
sesiones_por_persona = {}
for d in directorios:
    if os.path.isdir(os.path.join(personas_dir, d)):
        # El formato es nombre-YYYY-MM-DD-HH-MM
        # Hacemos split desde la derecha (5 guiones de la fecha)
        partes = d.rsplit('-', 5)
        if len(partes) == 6:
            nombre = partes[0]
            fecha_str = '-'.join(partes[1:])
            try:
                fecha = datetime.strptime(fecha_str, "%Y-%m-%d-%H-%M")
                if nombre not in sesiones_por_persona:
                    sesiones_por_persona[nombre] = []
                sesiones_por_persona[nombre].append((fecha, d))
            except ValueError:
                pass

if not sesiones_por_persona:
    print("No se encontraron sesiones de captura válidas en la carpeta 'personas'.")
    sys.exit(1)

# Filtrar por argumentos si se proporcionaron
if personas_a_entrenar:
    personas_finales = [p for p in sesiones_por_persona.keys() if p in personas_a_entrenar]
else:
    personas_finales = list(sesiones_por_persona.keys())

if not personas_finales:
    print("No se encontraron datos para las personas especificadas.")
    sys.exit(1)

# Seleccionar la última sesión para cada persona
carpetas_a_procesar = []
label_map = {}
current_label = 0

for persona in personas_finales:
    # Ordenar por fecha descendente y coger la primera (más reciente)
    sesiones_ordenadas = sorted(sesiones_por_persona[persona], key=lambda x: x[0], reverse=True)
    ultima_sesion = sesiones_ordenadas[0][1]
    carpetas_a_procesar.append((persona, ultima_sesion, current_label))
    label_map[current_label] = persona
    current_label += 1

print("Sesiones seleccionadas para entrenamiento:")
for persona, carpeta, lbl in carpetas_a_procesar:
    print(f" - {persona}: {carpeta} (Label: {lbl})")

# Hacer etiquetado de las caras
labels = []
facesData = []

for persona, carpeta, label in carpetas_a_procesar:
    personPath = os.path.join(personas_dir, carpeta)
    print(f"Leyendo imágenes de {personPath} ...")
    
    for fileName in os.listdir(personPath):
        if fileName.endswith(('.jpg', '.jpeg', '.png')):
            # Se añade la etiqueta correspondiente
            labels.append(label)
            # Se lee la imagen en escala de grises
            facesData.append(cv2.imread(os.path.join(personPath, fileName), 0))

if not facesData:
    print("No se encontraron imágenes válidas para entrenar.")
    sys.exit(1)

print(f"Se van a entrenar {len(facesData)} imágenes en total.")
print("Entrenando el modelo...")

# Entrenar 
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.train(facesData, np.array(labels))

# Crear directorio de entrenamientos si no existe
entrenamientos_dir = 'entrenamientos'
if not os.path.exists(entrenamientos_dir):
    os.makedirs(entrenamientos_dir)

# Guardar entrenamiento en yaml con el nombre modelo-año-mes-dia-hora-minuto.yaml
fecha_hora_actual = datetime.now().strftime('%Y-%m-%d-%H-%M')
modelo_filename = os.path.join(entrenamientos_dir, f"modelo-{fecha_hora_actual}.yaml")
face_recognizer.save(modelo_filename)

print(f"¡Modelo guardado exitosamente como {modelo_filename}!")

# Guardar un archivo de correspondencia entre ID (label) y Nombre para el script de reconocimiento
labels_filename = os.path.join(entrenamientos_dir, f"labels-{fecha_hora_actual}.txt")
with open(labels_filename, "w") as f:
    for lbl, nombre in label_map.items():
        f.write(f"{lbl},{nombre}\n")
print(f"Archivo de etiquetas guardado como '{labels_filename}'.")
