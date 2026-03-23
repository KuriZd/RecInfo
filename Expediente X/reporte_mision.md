# Reporte de Misión: Recuperación de la Información
**Agente Especial:** [Oscar kuricaveri zamudio/22120729]

---
## Misión 1, 2 y 3

### Misión 1: Esteganografía LSB en escala de grises

**Objetivo:** Extraer un mensaje oculto en el bit menos significativo de cada píxel de `evidencia_1.png`.

#### Código Python
```python
import cv2
import numpy as np

# 1. Cargar la imagen interceptada (en escala de grises)
img = cv2.imread('evidencia_1.png', cv2.IMREAD_GRAYSCALE)

if img is None:
    raise FileNotFoundError("No se pudo cargar la imagen 'evidencia_1.png'")

# 2. Aplanar la imagen
pixels = img.flatten()

# 3. Extraer el último bit de cada píxel
bits = pixels & 1

# 4. Agrupar en bytes y convertir a ASCII
mensaje = ""

for i in range(0, len(bits), 8):
    byte_bits = bits[i:i+8]

    if len(byte_bits) < 8:
        break

    byte_str = ''.join(str(int(bit)) for bit in byte_bits)
    caracter = chr(int(byte_str, 2))
    mensaje += caracter

    if "###FIN###" in mensaje:
        mensaje = mensaje.split("###FIN###")[0]
        break

print("Mensaje oculto encontrado:")
print(mensaje)
```

#### Evidencia recuperada
**Texto revelado:**
```text
[OPERACION_LECHUZA_APROBADA]
```

**Imagen de la misión:**
![Misión 1](./assets/mision1.jpg)

---

### Misión 2: Operación Camaleón (Recuperación por color HSV)

**Objetivo:** Aislar en `evidencia_2.png` el texto cuya diferencia está únicamente en el matiz (Hue) usando el espacio de color HSV.

#### Código Python
```python
import cv2
import numpy as np

# 1. Cargar evidencia_2.png
img = cv2.imread('evidencia_2.png')

if img is None:
    raise FileNotFoundError("No se pudo cargar la imagen 'evidencia_2.png'")

# 2. Convertir a HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# 3. Definir el rango de la tinta enemiga
lower = np.array([63, 50, 50], dtype=np.uint8)
upper = np.array([66, 255, 255], dtype=np.uint8)

# 4. Aplicar cv2.inRange para revelar el mensaje
mascara = cv2.inRange(hsv, lower, upper)

cv2.imshow('Imagen original', img)
cv2.imshow('Mascara del mensaje', mascara)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Opcional: guardar la máscara
cv2.imwrite('mensaje_revelado_mision2.png', mascara)
```

#### Evidencia recuperada
**Texto o forma revelada:**
```text
[No encontrada]
```

**Imagen de la misión:**
![Misión 2](./assets/mision2.jpg)

---

### Misión 3: El Cifrado Cromático (Reto híbrido HSV + LSB)

**Objetivo:** Filtrar primero los píxeles amarillo pardo en `evidencia_3.png` y después extraer de ellos el LSB del canal V para reconstruir el mensaje oculto.

#### Código Python
```python
import cv2
import numpy as np

# 1. Cargar evidencia_3.png y convertir a HSV
img = cv2.imread('evidencia_3.png')

if img is None:
    raise FileNotFoundError("No se pudo cargar la imagen 'evidencia_3.png'")

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# 2. Crear máscara para el Amarillo Pardo
lower = np.array([15, 100, 100], dtype=np.uint8)
upper = np.array([20, 255, 255], dtype=np.uint8)
mascara = cv2.inRange(hsv, lower, upper)

# 3. Extraer canal V y obtener solo los píxeles donde la máscara es válida
canal_v = hsv[:, :, 2]
pixeles_objetivo = canal_v[mascara > 0]

# 4. Aplicar decodificación LSB a ese subconjunto de píxeles
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
```

#### Evidencia recuperada
**Texto revelado:**
```text
[Pega aquí el mensaje recuperado al ejecutar el programa]
```

**Imagen de la misión:**
![Misión 3](./assets/mision3.jpg)

---
## Análisis del Analista (Reflexiones Finales)

### 1. Sobre la Investigación (Misión 1)
**Explica con tus propias palabras qué es la Esteganografía LSB. ¿Por qué cambiar el último bit de un píxel no altera la imagen de forma visible para el ojo humano?**

[LSB es un metodo usado en este caso para esconder un mensaje en el bit menos significativo, remplazando el ultimo bit de cada pixel lo que genera un pequeno cambio en la imagen y aunque el ojo humano es bueno para reconocer cambio o patrones, en este caso la diferencia es tan infima, aprox. un 0.39%, como para notarla a simple vista por lo que es perfecto para ocultar mensajes simples]

### 2. Sobre los Espacios de Color (Misión 2)
**Intenta aislar el texto de la Misión 2 usando directamente los canales BGR. ¿Por qué crees que es casi imposible recuperar esa información en BGR, pero resultó tan fácil usando el canal 'H' (Hue) del modelo HSV?**

[En teoria lo que estamos haciendo es pasar la imagen por distintas mascaras, lo cual extrae un rango especifico del color verde, que tiene una ligera vaciacion en contraste con el resto del fondo, tan pequena como para que el ojo humano sea incapas de detectarla pero facil de filtrar cambiando el HUE]

### 3. Sobre la Lógica de Recuperación (Misión 3)
**Si en la Misión 3 intentaras extraer el mensaje LSB de toda la imagen completa (sin usar la máscara amarilla primero), ¿qué obtendrías como texto? ¿Cómo demuestra esto que el color actuó como una 'llave de acceso'?**

[al intenta extraer el texto directamente no encontramos con una secuencia de caracteres sin sentido, con símbolos extraños, letras desordenadas o texto corrupto, y es ahi donde el HUE amarillo entra como llave al filtrar solo los pixeles amarillos y leer el bit menos significativo solo de estos.
sin embargo, la decodificación LSB del canal V no produjo un mensaje ASCII legible ni encontró el delimitador. Esto sugiere que la imagen analizada probablemente no corresponde al archivo correcto de la misión]

---
## Referencias breves

- La esteganografía consiste en ocultar la existencia de la comunicación dentro de otro medio.
- OpenCV recomienda el uso de `cvtColor()` y `inRange()` para trabajar con segmentación por color en HSV.

