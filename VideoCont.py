from itertools import count
from sqlite3 import register_converter
import cv2
import numpy as np
import time
from time import sleep

cap=cv2.VideoCapture('C:/Users/jorgil/Documents/Python Scripts/ContadorCarros/carros.mp4')

count_line_position=550
count_line_position2=350

min_width_react=80
min_hight_react=80

subst=cv2.createBackgroundSubtractorMOG2(history=100)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
car_counter = 0


def centro_handle(x,y,w,h):
    x1=int(w/2)
    y1=int(h/2)
    cx=x+x1
    cy=y+y1
    return cx,cy

detect=[]
offset=4  #error permitible entre pixeles
counter=0
counter2=0
fin=0
star=[]
fin=[]
calculo=0
vel=0
car_counter=0
pos1=0
pos2=0

while True:
    ret,frame=cap.read()
    if ret == False: break
    #frame = imutils.resize(frame, width=640)
    #print(frame.shape)
    tempo=float(1/60)
    sleep(tempo)
    
    cv2.imshow('Video Original', frame)
    
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    # Especificamos los puntos extremos del área a analizar
    area_pts = np.array([[0, 710], [frame.shape[1]-750, 710], [frame.shape[1]-670, 350], [250, 350]])
   
    # Con ayuda de una imagen auxiliar, determinamos el área
    # sobre la cual actuará el detector de movimiento
    imAux = np.zeros(shape=(frame.shape[:2]), dtype=np.uint8)
    imAux = cv2.drawContours(imAux, [area_pts], -1, (255), -1)
    image_area = cv2.bitwise_and(gray, gray, mask=imAux)    
   
    # Obtendremos la imagen binaria donde la región en blanco representa
    # la existencia de movimiento
    fgmask = subst.apply(image_area)
    
    img_sub = subst.apply(fgmask)

    cv2.imshow('Video con fondo',img_sub)
    
    fgmask = cv2.morphologyEx(img_sub, cv2.MORPH_OPEN, kernel)

    cv2.imshow('Filtro Morfologico 1',fgmask)
       
    
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
    
    cv2.imshow('Filtro Morfologico 2',fgmask)

    dilat=cv2.dilate(fgmask,np.ones((5,5)))

    cv2.imshow('Video con dilatacion',dilat)

    kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))

    dilatada=cv2.morphologyEx(dilat,cv2.MORPH_CLOSE,kernel)

    cv2.imshow('Video dilatado',dilatada)

    dilatada=cv2.morphologyEx(dilatada,cv2.MORPH_CLOSE,kernel)
    #dilatada=cv2.morphologyEx(dilatada,cv2.MORPH_CLOSE,kernel)
    cv2.imshow('Video 2 dilatacion',dilatada)

    contador,h=cv2.findContours(dilatada,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    #cv2.line(frame,(25,count_line_position),(5000,count_line_position),(255,127,127),3)

    #cv2.imshow('Video con linea',frame)

    for (i,c) in enumerate(contador):
        (x,y,w,h)=cv2.boundingRect(c)
        if cv2.contourArea(c) > 1000:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,255), 1)
            if count_line_position2-offset < y < count_line_position2+offset:
                car_counter = car_counter + 1
                print('contador alterno:'+str(car_counter))
                pos1=x
                pos2=y-20           
            cv2.putText(frame,'V:'+str(int(car_counter)),(pos1,pos2),cv2.FONT_HERSHEY_TRIPLEX,1,(255,244,0),2)

        valcounter=(w>=min_width_react)and (h>=min_hight_react)
        
        if not valcounter:
            continue

        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.putText(frame,'Auto '+str(counter),(x,y-20),cv2.FONT_HERSHEY_TRIPLEX,1,(255,244,0),2)

        center = centro_handle(x,y,w,h)
        detect.append(center)
        cv2.circle(frame,center,4,(0,0,255),-1)

        #detección uno
        for (x,y) in detect:
            if y<(count_line_position2+offset) and y>(count_line_position2-offset):
                star.append(time.time())
                #print(star)
                counter+=1
                #star=time.time()
                #print(star)
                #cv2.line(frame,(25,count_line_position),(1200,count_line_position),(0,127,255),3)
                detect.remove((x,y))
                cv2.line(frame,(25,count_line_position),(600,count_line_position),(0,127,255),3)
                print('Contador vehículos:'+str(counter))
    
        for (x,y) in detect:
            if y<(count_line_position+offset) and y>(count_line_position-offset):
                counter2+=1
                fin.append(time.time())
                print(fin)
                #cv2.line(frame,(25,count_line_position),(1200,count_line_position),(0,127,255),3)
                detect.remove((x,y))
                print('Contador vehículos 2:'+str(counter2))
                valor=fin[calculo]-star[calculo]
                #print(valor)        
                calculo+=1
                vel=(50/valor)*(3.6)
        

        print(x)

        cv2.putText(frame,'V:'+str(int(vel)),(x,y-20),cv2.FONT_HERSHEY_TRIPLEX,1,(255,244,0),2)

    cv2.putText(frame,"Vehiculos:"+str(counter),(450,70),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),5)
    #cv2.imshow('Rec',frame)
    cv2.line(frame, (130, 550), (550, 550), (0, 255, 0), 3)         # Visualización del conteo de autos
    cv2.drawContours(frame, [area_pts], -1, (0, 0, 255), 2)
    cv2.line(frame, (130, 550), (550, 550), (0, 255, 255), 1)
    cv2.line(frame, (460, 350), (610, 350), (0, 255, 0), 3)
    #cv2.rectangle(frame, (frame.shape[1]-70, 215), (frame.shape[1]-5, 270), (0, 255, 0), 2)
    #cv2.putText(frame, str(car_counter), (frame.shape[1]-55, 250),
    #            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,0), 2)
    cv2.imshow('frame', frame)


    if cv2.waitKey(5) & 0xFF == 27:
        break

cv2.destroyAllWindows()
cap.release()