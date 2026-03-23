import cv2
import numpy as np

img = cv2.imread('./assets/evidencia_2.png')

if img is None:
    raise FileNotFoundError("No se pudo cargar la imagen 'evidencia_2.png'")

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

for h1, h2 in [(60, 62), (62, 64), (63, 66), (64, 68), (66, 70)]:
    lower = np.array([h1, 40, 40], dtype=np.uint8)
    upper = np.array([h2, 255, 255], dtype=np.uint8)

    mask = cv2.inRange(hsv, lower, upper)
    cv2.imshow(f"H {h1}-{h2}", mask)

cv2.imshow('Imagen original', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

