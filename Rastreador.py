from abc import ABC
import math

class Rastreador:

    def __init__(self) -> None:
        self.centro_puntos={}
        self.id_count = 1
        #print(self.id_count)

    
    def rastreo(self,objetos):

        #print(self.centro_puntos)
        objetos_id=[]

        #print("here" + str(objetos))

        for rect in objetos:
            x,y,w,h=rect
            cx=(x+x+y)//2
            cy=(y+y+h)//2

            #print(cy)

            objeto_det=False
            
            #abc=self.centro_puntos.items()
            #print(abc)

            for id,pt in self.centro_puntos.items():
                #print(id)
                dist=math.hypot(cx-pt[0],cy-pt[1])

                #print(dist)
                #print("ya") 

                if dist<50:
                    self.centro_puntos[id]=(cx,cy)
                    #print(self.centro_puntos)
                    objetos_id.append([x,y,w,h,id])
                    objeto_det=True
                    break
        
            if objeto_det is False:
                self.centro_puntos[self.id_count]=(cx,cy)
                objetos_id.append([x,y,w,h,self.id_count])
                self.id_count=self.id_count+1
            
        new_center_points={}

        for obj_bb_id in objetos_id:
            _,_,_,_,object_id = obj_bb_id
            center=self.centro_puntos[object_id]
            new_center_points[object_id]=center
            
        self.centro_puntos=new_center_points.copy()
        return objetos_id
