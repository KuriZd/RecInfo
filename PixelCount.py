import cv2
import numpy as np

imagen = cv2.imread("assets/frutas.png")

if imagen is None:
    print("No se pudo cargar la imagen.")
    exit()

hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

verde_bajo = np.array([35, 40, 40])
verde_alto = np.array([85, 255, 255])

mascara_verde = cv2.inRange(hsv, verde_bajo, verde_alto)

pixeles_verdes = cv2.countNonZero(mascara_verde)

alto, ancho = mascara_verde.shape
total_pixeles = alto * ancho

porcentaje_verde = (pixeles_verdes / total_pixeles) * 100

print(f"Píxeles verdes: {pixeles_verdes}")
print(f"Total de píxeles: {total_pixeles}")
print(f"Porcentaje de píxeles verdes: {porcentaje_verde:.2f}%")

cv2.imshow("Imagen original", imagen)
cv2.imshow("Mascara verde", mascara_verde)
cv2.waitKey(0)
cv2.destroyAllWindows()