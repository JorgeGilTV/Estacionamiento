import cv2
from Rastreador import *
import numpy as np
import imutils

count_line_position2=500
offset=4  #error permitible entre pixeles

seguimiento=Rastreador()

#print(seguimiento.id_count)

cap=cv2.VideoCapture('C:/Users/jorgil/Documents/Python Scripts/ContadorCarros/carros.mp4')

subst=cv2.createBackgroundSubtractorMOG2(history=1000)


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
    frame = subst.apply(image_area)
    
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray,(3,3),5)

    img_sub = subst.apply(blur)

    dilat=cv2.dilate(img_sub,np.ones((5,5)))

    kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))

    dilatada=cv2.morphologyEx(dilat,cv2.MORPH_CLOSE,kernel)

    dilatada=cv2.morphologyEx(dilatada,cv2.MORPH_CLOSE,kernel)

    contornos,_=cv2.findContours(dilatada,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)




    #mascara=subst.apply(frame)
    #_,mascara=cv2.threshold(mascara,254,255,cv2.THRESH_BINARY)
    #contornos,_ = cv2.findContours(mascara,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    detecciones=[]

    for cont in contornos:
        area=cv2.contourArea(cont)
        if area > 1500:
            
            x,y,ancho,alto=cv2.boundingRect(cont)
            #if count_line_position2-offset < y < count_line_position2+offset:                    
            detecciones.append([x,y,ancho,alto])
            cv2.rectangle(frame,(x,y),(x+ancho,y+alto),(255,255,0),3)   
    
    #print(detecciones)

    info_id=seguimiento.rastreo(detecciones)
    
    print(info_id)
    
    #print(seguimiento.centro_puntos.items())

    for inf in info_id:
        x,y,ancho,alto,id= inf
        cv2.putText(frame,str(id),(x,y-15),cv2.FONT_HERSHEY_PLAIN,1,(0,255,255),2)
        cv2.rectangle(frame,(x,y),(x+ancho,y+alto),(255,255,0),3)
    
    #print(info_id)
    cv2.imshow("Frame",frame)
    
    k = cv2.waitKey(70) & 0xFF
    if k ==27:
        break

cap.release()
cv2.destroyAllWindows()

        