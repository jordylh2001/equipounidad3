import cv2
import numpy as np
import time

def document(cant,doc,colors,mom):
    doc=doc
    #print(doc)
    text=""
    f=open(r"result.txt","w")
    f.write("Id,Size,Color,Moment \n")
    for x in range(len(cant)):
        text=cant[x]+","+doc[x]+","+colors[x]+","+mom[x]+"\n"
        f.write(text)
    f.close()

#Variables necesarias para los calculos
doc=[]
cant=[]
colors=[]
mom=[]
aux = 0
aux2 = aux
TIMER = int(0)
font = cv2.FONT_HERSHEY_SIMPLEX
prev = time.time()
frame_text=""
minute=0
seconds=0
moment=""
color=""
areaN=0
areaA=0
areaV=0

print("Introduzca el limites para clasificacion de los tamanos de las naranjas")

print('Introduzca el limite de las grandes')
LimG = int(input())

print('Introduzca el limite superior de las medianas')
LimM1 = int(input())

print('Introduzca el limite inferior de las medianas')
LimM2 = int(input())

print('Introduzca el partir de que rango es pequeno')
LimP = int(input())

print('Introduce el video')
video = input()

capture = cv2.VideoCapture(video)
width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
writer = cv2.VideoWriter('result.mp4', cv2.VideoWriter_fourcc(*'XVID'),25, (width, height))
while capture.isOpened():
    #Se obtienen los frames del video
    ret, frame = capture.read()
    if ret:
        kernel=np.ones((5,5),np.float32)/25
        dst=cv2.filter2D(frame,-1,kernel)
        #cv2.imshow("Suavizado", dst)
        #cv2.imshow("Original", frame)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #cv2.imshow("Colores", hsv)

        #Filtro para el conjunto de colores posibles en una naranja
        lower = np.array([0, 50, 50])
        upper = np.array([85, 255, 255])

        #naranjas
        mask= cv2.inRange(hsv, lower, upper)
        contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(frame, contornos, -1, (0, 0, 255), 3)
        #cv2.imshow('naranjas',mask)

        
        #cv2.imshow("Colores", hsv)

        #Filtro para el color naranja
        lower1 = np.array([0, 50, 50])
        upper1 = np.array([25, 255, 255])

        #naranja
        mask1= cv2.inRange(hsv, lower1, upper1)
        contornos1, _ = cv2.findContours(mask1, cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(frame, contornos1, -1, (0, 0, 255), 3)
        #cv2.imshow('naranja',mask1)

        #Filtro para el color amarillo
        lower2 = np.array([25, 50, 50])
        upper2 = np.array([35, 255, 255])

        #amarillo
        mask2= cv2.inRange(hsv, lower2, upper2)
        contornos2, _ = cv2.findContours(mask2, cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(frame, contornos2, -1, (0, 0, 255), 3)
        #cv2.imshow('Amarillo',mask2)

        #Filtro para el color verde
        lower3 = np.array([35, 50, 50])
        upper3 = np.array([85, 255, 255])

        #verde
        mask3= cv2.inRange(hsv, lower3, upper3)
        contornos3, _ = cv2.findContours(mask3, cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(frame, contornos3, -1, (0, 0, 255), 3)
        #cv2.imshow('Verde',mask3)

        #result=cv2.bitwise_and(frame,frame,mask=mask)
        #cv2.imshow("Result", result)

        #Obtenemos el tamano de las areas de cada color
        for c in contornos1:
            areaN = cv2.contourArea(c)
        for c in contornos2:
            areaA = cv2.contourArea(c)
        for c in contornos3:
            areaV = cv2.contourArea(c)

        #Se comparan los tamanos de las areas
        if  (areaN>areaA) & (areaN>areaV):
            color="Naranja"
        if  (areaA>areaN) & (areaA>areaV):
            color="Amarrillo"
        if  (areaV>areaA) & (areaV>areaN):
            color="Verde"

        #Se muestra la info asi como se hacen ciertos calculos
        for c in contornos:
            area = cv2.contourArea(c)
            size=""
            #Grandes

            if area > 3000:
                #print(area)
                M = cv2.moments(c)
                #print(M)
                if M["m00"] == 0:
                    M["m00"] = 1
                x = int(M["m10"] / M["m00"])
                # print(x)1
                if x <= 30:
                    aux += 1
                    if area>LimG:size="Grande"
                    if (area>LimM2)& (area<LimM1):size="Mediana"
                    if area<LimP:size="Pequena"
                    seconds=TIMER%60
                    minute=round((TIMER-seconds)/60)
                    moment=str(minute)+":"+str(seconds)
                    cant.append(str(aux))
                    doc.append(size)
                    mom.append(moment)
                    colors.append(color)
                    frame_text="Id:"+str(aux)+";"+"Size:"+size+";"+"Color:"+color+";"+"Minute:"+moment
                y = int(M['m01'] / M['m00'])
                if aux != aux2:
                    print("Total de naranjas", aux)
                    aux2 = aux
                # cv2.circle(frame, (x, y), 7, (0, 255, 0), -1)
                # font = cv2.FONT_HERSHEY_SIMPLEX
                # cv2.putText(frame, '{},{}'.format(x, y), (x + 10, y), font, 0.75, (0, 255, 0), 1, cv2.LINE_AA)
                nuevoContorno = cv2.convexHull(c)
                
                cv2.drawContours(frame, [nuevoContorno], 0, (0, 0, 255), 3)

        #Tiempo del video
        cur = time.time()
        if cur-prev >= 1:
            prev = cur
            TIMER = TIMER+1
            
        #Muestra la info en el video
        cv2.putText(frame,frame_text,(10,50),font,1,(0,255,255),)

        writer.write(frame)
        cv2.imshow("Cinta", frame)
        if cv2.waitKey(30) == ord('s'):
            break
    else:
        break

capture.release()
writer.release()
document(cant,doc,colors,mom)
cv2.destroyAllWindows()

