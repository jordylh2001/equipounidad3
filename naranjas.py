import cv2
import numpy as np

print('Introduce el video')
video = input()

capture = cv2.VideoCapture(video)
aux = 0
aux2 = aux
while capture.isOpened():
    ret, frame = capture.read()
    if ret:

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # cv2.imshow("Colores", hsv)

        lower = np.array([0, 50, 50])
        upper = np.array([70, 255, 255])

        mask = cv2.inRange(hsv, lower, upper)
        contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
        # cv2.drawContours(frame, contornos, -1, (0, 0, 255), 3)
        # cv2.imshow('mask',mask)

        for c in contornos:
            area = cv2.contourArea(c)
            if area > 3000:
                M = cv2.moments(c)
                if M["m00"] == 0:
                    M["m00"] = 1

                x = int(M["m10"] / M["m00"])
                # print(x)
                if x <= 30:
                    aux += 1
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

        cv2.imshow("Cinta", frame)
        if cv2.waitKey(30) == ord('s'):
            break
    else:
        break

capture.release()
cv2.destroyAllWindows()
