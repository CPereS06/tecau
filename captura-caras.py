import cv2
import os
import sys
import time
from datetime import datetime

if len(sys.argv) > 2:
    nombrePersona = sys.argv[1]
    cuantosRostros = int(sys.argv[2])
else:
    nombrePersona = input("Introduce el nombre de la persona a capturar: ")
    cuantosRostros = int(input("Introduce el número de capturas a realizar: "))

fecha_hora = datetime.now().strftime("%Y-%m-%d-%H-%M")
carpeta = f"personas/{nombrePersona}-{fecha_hora}"

if not os.path.exists(carpeta):
    print(f'Carpeta creada: {carpeta}')
    os.makedirs(carpeta)
cap = cv2.VideoCapture(0)
faceClassif =cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
count = 0
while True:
    ret,frame = cap.read()
    frame = cv2.flip(frame,1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    auxFrame = frame.copy()
    time.sleep(0.1)
    faces = faceClassif.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y),(x+w,y+h),(128,0,255),2)
        rostro = auxFrame[y:y+h,x:x+w]
        rostro = cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)
        nombre_imagen = f"captura-{count+1:05d}.jpg"
        cv2.imwrite(f"{carpeta}/{nombre_imagen}",rostro)
        cv2.imshow('rostro',rostro)
        count = count +1
    cv2.rectangle(frame,(10,5),(450,25),(255,255,255),-1)
    cv2.putText(frame,'Pendientes de capturar:{}'.format(cuantosRostros-count),(10,20), 2, 0.5,(128,0,255),1,cv2.LINE_AA)
    cv2.imshow('frame',frame)
    if (cuantosRostros - count) <= 0  or cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()