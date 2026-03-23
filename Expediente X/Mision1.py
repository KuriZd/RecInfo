import cv2
import numpy as np

# 1. Cargar la imagen interceptada (en escala de grises)
img = cv2.imread('./assets/evidencia_1.png', cv2.IMREAD_GRAYSCALE)

if img is None:
    raise FileNotFoundError("No se pudo cargar la imagen 'evidencia_1.png'")

# 2. Aplanar la imagen para convertirla en un arreglo de 1 dimensión
pixels = img.flatten()

# 3. Extraer el último bit de cada píxel
bits = pixels & 1

# 4. Agrupar los bits de 8 en 8 y convertirlos a caracteres ASCII
mensaje = ""

for i in range(0, len(bits), 8):
    byte_bits = bits[i:i+8]

    # Si ya no hay 8 bits completos, detenemos
    if len(byte_bits) < 8:
        break

    # Convertir los 8 bits en una cadena binaria
    byte_str = ''.join(str(int(bit)) for bit in byte_bits)

    # Convertir el byte binario a entero y luego a carácter ASCII
    caracter = chr(int(byte_str, 2))
    mensaje += caracter

    # 5. Detenerse al encontrar la palabra clave ###FIN###
    if "###FIN###" in mensaje:
        mensaje = mensaje.split("###FIN###")[0]
        break

print("Mensaje oculto encontrado:")
print(mensaje)