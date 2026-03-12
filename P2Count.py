import cv2
import numpy as np
import glob
import os

# 1. Obtener todas las rutas de imágenes en una carpeta
rutas_imagenes = glob.glob('carpeta_imagenes/*.jpg')

# Si quieres aceptar más formatos:
rutas_imagenes += glob.glob('carpeta_imagenes/*.png')
rutas_imagenes += glob.glob('carpeta_imagenes/*.jpeg')

# 2. Leer imágenes y guardarlas en una lista junto con su nombre
imagenes = []

for ruta in rutas_imagenes:
    img = cv2.imread(ruta)
    if img is not None:
        imagenes.append((ruta, img))

# Rangos HSV para colores primarios
rangos_colores = {
    'rojo_1': (np.array([0, 100, 100]), np.array([10, 255, 255])),
    'rojo_2': (np.array([170, 100, 100]), np.array([180, 255, 255])),
    'verde': (np.array([35, 100, 100]), np.array([85, 255, 255])),
    'azul': (np.array([100, 100, 100]), np.array([130, 255, 255]))
}

# 3. Procesar cada imagen cargada
for i, (ruta, img) in enumerate(imagenes):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    alto, ancho = img.shape[:2]
    total_pixeles = alto * ancho

    mascara_rojo_1 = cv2.inRange(hsv, rangos_colores['rojo_1'][0], rangos_colores['rojo_1'][1])
    mascara_rojo_2 = cv2.inRange(hsv, rangos_colores['rojo_2'][0], rangos_colores['rojo_2'][1])
    mascara_rojo = cv2.bitwise_or(mascara_rojo_1, mascara_rojo_2)

    mascara_verde = cv2.inRange(hsv, rangos_colores['verde'][0], rangos_colores['verde'][1])
    mascara_azul = cv2.inRange(hsv, rangos_colores['azul'][0], rangos_colores['azul'][1])

    pixeles_rojos = cv2.countNonZero(mascara_rojo)
    pixeles_verdes = cv2.countNonZero(mascara_verde)
    pixeles_azules = cv2.countNonZero(mascara_azul)

    porcentaje_rojo = (pixeles_rojos / total_pixeles) * 100
    porcentaje_verde = (pixeles_verdes / total_pixeles) * 100
    porcentaje_azul = (pixeles_azules / total_pixeles) * 100

    nombre_archivo = os.path.basename(ruta)

    print(f'\nImagen {i}: {nombre_archivo}')
    print(f'Rojo: {porcentaje_rojo:.2f}%')
    print(f'Verde: {porcentaje_verde:.2f}%')
    print(f'Azul: {porcentaje_azul:.2f}%')

    cv2.imshow(f'Imagen {i} - {nombre_archivo}', img)
    cv2.imshow(f'Mascara roja {i}', mascara_rojo)
    cv2.imshow(f'Mascara verde {i}', mascara_verde)
    cv2.imshow(f'Mascara azul {i}', mascara_azul)

    cv2.waitKey(0)
    cv2.destroyAllWindows()