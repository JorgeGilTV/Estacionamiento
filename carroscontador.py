import cv2
import numpy as np
import imutils

cap = cv2.VideoCapture('C:/Users/Python Scripts/car/carPark.mp4')

fgbg = cv2.createBackgroundSubtractorMOG2()
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
car_counter = 0

while True:

    ret, frame = cap.read()
    if ret == False: break

    frame = imutils.resize(frame, width=640)
    cv2.imshow('Imagen Original',frame)

    # Especificamos los puntos extremos del área a analizar
    area_pts = np.array([[160, 290], [frame.shape[1]-380, 290], [frame.shape[1]-350, 220], [230, 220]])
   
    # Con ayuda de una imagen auxiliar, determinamos el área
    # sobre la cual actuará el detector de movimiento
    imAux = np.zeros(shape=(frame.shape[:2]), dtype=np.uint8)
    imAux = cv2.drawContours(imAux, [area_pts], -1, (255), -1)
    image_area = cv2.bitwise_and(frame, frame, mask=imAux)    
   
    # Obtendremos la imagen binaria donde la región en blanco representa
    # la existencia de movimiento
    fgmask = fgbg.apply(image_area)

    cv2.imshow('Fondo',fgmask)

    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    cv2.imshow('Filtro Morfologico 1',fgmask)

    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
    
    cv2.imshow('Filtro Morfologico 2',fgmask)

    fgmask = cv2.dilate(fgmask, None, iterations=5)
   
    cv2.imshow('Dilatacion',fgmask)
    # Encontramos los contornos presentes de fgmask, para luego basándonos
    # en su área poder determinar si existe movimiento (autos)

    cnts = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    for cnt in cnts:
        if cv2.contourArea(cnt) > 2500 and cv2.contourArea(cnt) < 5000:
            
            x, y, w, h = cv2.boundingRect(cnt)
            #print(x,w, 'and', y,h)
            
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,255), 1)
            
            
        # Si el auto ha cruzado entre 440 y 460 abierto, se incrementará
        # en 1 el contador de autos
            if 265 < (x + w) < 300:
                if 282 < (y + h) < 290:
                    #if 59 < h < 100:
                        print(x+w, 'and', y+h)
                       
                        #print(x,w,y,h)
                        car_counter = car_counter + 1
                        #print(car_counter)
                        #print(cv2.contourArea(cnt))
    cv2.line(frame, (295, 150), (315, 150), (0, 255, 0), 3)         # Visualización del conteo de autos
    cv2.drawContours(frame, [area_pts], -1, (0, 0, 255), 2)
    cv2.line(frame, (295, 150), (315, 150), (0, 255, 255), 1)
    cv2.line(frame, (150, 290), (270, 290), (0, 255, 0), 3)
    cv2.rectangle(frame, (frame.shape[1]-70, 215), (frame.shape[1]-5, 270), (0, 255, 0), 2)
    cv2.putText(frame, str(car_counter), (frame.shape[1]-55, 250),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,0), 2)
    cv2.imshow('frame', frame)

    k = cv2.waitKey(70) & 0xFF
    if k ==27:
        break

cap.release()
cv2.destroyAllWindows()