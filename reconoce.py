import cv2
import os
import sys

entrenamientos_dir = 'entrenamientos'

if len(sys.argv) > 1:
    modelo_seleccionado = sys.argv[1]
    modelo_path = os.path.join(entrenamientos_dir, modelo_seleccionado)
    if not os.path.exists(modelo_path):
        print(f"Error: El modelo especificado '{modelo_path}' no existe.")
        exit()
else:
    if not os.path.exists(entrenamientos_dir):
        print(f"Error: No existe el directorio '{entrenamientos_dir}'.")
        exit()
    # Usar os.listdir en lugar de glob
    archivos = [f for f in os.listdir(entrenamientos_dir) if f.startswith("modelo-") and f.endswith(".yaml")]
    if not archivos:
        print("Error: No se encontró ningún modelo entrenado (.yaml). Ejecuta entrena.py primero.")
        exit()
    # Ordenamos para obtener el archivo más reciente
    archivos.sort()
    modelo_path = os.path.join(entrenamientos_dir, archivos[-1])

print(f"Cargando modelo: {modelo_path}")
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read(modelo_path)

# Extraer la fecha/hora del nombre del modelo para encontrar las etiquetas
# Formato esperado: modelo-YYYY-MM-DD-HH-MM.yaml
nombre_base = os.path.basename(modelo_path)
fecha_hora = nombre_base.replace('modelo-', '').replace('.yaml', '')
labels_path = os.path.join(entrenamientos_dir, f"labels-{fecha_hora}.txt")

# Cargar el archivo de etiquetas
label_map = {}
if os.path.exists(labels_path):
    with open(labels_path, "r") as f:
        for linea in f:
            lbl, nombre = linea.strip().split(',')
            label_map[int(lbl)] = nombre
else:
    print(f"Advertencia: No se encontró {labels_path}. No se podrán mostrar los nombres.")

# Inicializar captura de video y clasificador de caras
cap = cv2.VideoCapture(0)
faceClassif = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Captura de cara de la webcam en tiempo real en escala de grises
# y con las dimensiones con las que se trabaja en captura-caras.py
while True:
    ret, frame = cap.read()
    if not ret:
        break
        
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = faceClassif.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        # Usamos la imagen en escala de grises para extraer el rostro (igual que en el entrenamiento)
        rostro = gray[y:y+h, x:x+w]
        rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
        
        # Realizar predicción
        label, confidence = face_recognizer.predict(rostro)

        # Evaluar si la confianza es suficiente para considerar que es un usuario conocido
        # Para LBPHFaceRecognizer, una confianza menor significa mayor similitud. 
        # Un umbral aproximado de 75-80 suele ser el límite.
        if confidence < 75:
            # Si es usuario conocido, dibujar rectangulo verde y nombre
            nombre = label_map.get(label, "Conocido")
            # Recuadro alrededor de la cara en verde
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, nombre, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            
            # Banner superior
            cv2.rectangle(frame, (10, 5), (450, 25), (0, 255, 0), -1)
            cv2.putText(frame, f'Usuario: {nombre} (Dist: {confidence:.1f})', (10, 20), 2, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        else:
            # Si no es usuario conocido, dibujar rectangulo rojo y aviso de no reconocido  
            # Recuadro alrededor de la cara en rojo
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            cv2.putText(frame, 'No registrado', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            
            # Banner superior
            cv2.rectangle(frame, (10, 5), (450, 25), (0, 0, 255), -1)
            cv2.putText(frame, f'Usuario: NO REGISTRADO (Dist: {confidence:.1f})', (10, 20), 2, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    
    cv2.imshow('frame', frame)
    
    # Salir al pulsar 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
