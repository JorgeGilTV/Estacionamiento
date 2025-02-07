import cv2
import pickle

rectW,rectH=107,48

try:
    with open('C:/Users/Python Scripts/Car/carParkPos','rb') as f:
        posList=pickle.load(f)
except:
    posList=[]

def mouseClick(events,x,y,flags,params):
    if events==cv2.EVENT_LBUTTONDOWN:
        posList.append((x,y))
    if events==cv2.EVENT_RBUTTONDOWN:
        for i,pos in enumerate(posList):
            x1,y1=pos
            if x1<x<x1+rectW and y1<y<y1+rectH:
                posList.pop(i)
    with open('c:/Programas/Car/carParkPos','wb') as f:
        pickle.dump(posList,f)
    
            

while True:
    img=cv2.imread("c:/Programas/Car/img.png")
    for pos in posList: cv2.rectangle(img,pos,(pos[0]+rectW,pos[1]+rectH),(0,0,255),2)
    
    cv2.imshow("c:/Programas/Car/Image",img)
    cv2.setMouseCallback("c:/Programas/Car/Image",mouseClick)
    if cv2.waitKey(5) & 0xFF == 27:
      break
