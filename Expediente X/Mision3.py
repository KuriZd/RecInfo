import cv2
import numpy as np


img = cv2.imread('./assets/evidencia_3.png')

if img is None:
    raise FileNotFoundError("No se pudo cargar la imagen 'evidencia_3.png'")

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


lower = np.array([15, 100, 100], dtype=np.uint8)
upper = np.array([20, 255, 255], dtype=np.uint8)

mascara = cv2.inRange(hsv, lower, upper)


canal_v = hsv[:, :, 2]
pixeles_objetivo = canal_v[mascara > 0]


bits = pixeles_objetivo & 1

mensaje = ""

for i in range(0, len(bits), 8):
    byte = bits[i:i+8]

    if len(byte) < 8:
        break

    byte_str = ''.join(str(int(bit)) for bit in byte)
    caracter = chr(int(byte_str, 2))
    mensaje += caracter

    if "###FIN###" in mensaje:
        mensaje = mensaje.split("###FIN###")[0]
        break

print("Mensaje oculto encontrado:")
print(mensaje)


cv2.imshow("Mascara Amarillo Pardo", mascara)
cv2.waitKey(0)
cv2.destroyAllWindows()