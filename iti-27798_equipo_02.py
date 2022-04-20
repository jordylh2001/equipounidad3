import cv2
import numpy as np


def document(cant,doc):
    doc=doc
    #print(doc)
    text=""
    f=open(r"result.txt","w")
    f.write("Id,Size,Color,Moment \n")
    for x in range(len(cant)):
        text=cant[x]+","+doc[x]+","+"\n"
        f.write(text)
    f.close()

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
doc=[]
cant=[]
capture = cv2.VideoCapture(video)
aux = 0
aux2 = aux
width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
writer = cv2.VideoWriter('result.mp4', cv2.VideoWriter_fourcc(*'XVID'),25, (width, height))
while capture.isOpened():
    ret, frame = capture.read()
    if ret:
        kernel=np.ones((5,5),np.float32)/25
        dst=cv2.filter2D(frame,-1,kernel)
        #cv2.imshow("Suavizado", dst)
        #cv2.imshow("Original", frame)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #cv2.imshow("Colores", hsv)

        #Naranjas
        lower = np.array([0, 50, 50])
        upper = np.array([85, 255, 255])

        #naranja
        mask= cv2.inRange(hsv, lower, upper)
        contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(frame, contornos, -1, (0, 0, 255), 3)
        #cv2.imshow('naranja',mask)

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
                if x <= 50:
                    aux += 1
                    if area>LimG:size="Grande"
                    if (LimM2>10000)& (LimM1<20000):size="Mediana"
                    if area<LimP:size="Pequena"
                    cant.append(str(aux))
                    doc.append(size)

                y = int(M['m01'] / M['m00'])
                if aux != aux2:
                    print("Total de naranjas", aux)
                    aux2 = aux
                # cv2.circle(frame, (x, y), 7, (0, 255, 0), -1)
                # font = cv2.FONT_HERSHEY_SIMPLEX
                # cv2.putText(frame, '{},{}'.format(x, y), (x + 10, y), font, 0.75, (0, 255, 0), 1, cv2.LINE_AA)
                nuevoContorno = cv2.convexHull(c)
                cv2.drawContours(frame, [nuevoContorno], 0, (0, 0, 255), 3)

        # result=cv2.bitwise_and(frame,frame,mask=mask)
        # cv2.imshow("Result", result)
        writer.write(frame)
        cv2.imshow("Cinta", frame)
        if cv2.waitKey(30) == ord('s'):
            break
    else:
        break

capture.release()
writer.release()
cv2.destroyAllWindows()
document(cant,doc)
