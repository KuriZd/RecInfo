import cv2
import numpy as np
import glob
import os
import csv

RANGOS = {
    'rojo':    [(np.array([0, 100, 100]),   np.array([10, 255, 255])),
                (np.array([170, 100, 100]), np.array([180, 255, 255]))],
    'naranja': [(np.array([11, 100, 100]),  np.array([25, 255, 255]))],
    'amarillo':[(np.array([26, 100, 100]),  np.array([34, 255, 255]))],
    'verde':   [(np.array([35, 50, 50]),    np.array([85, 255, 255]))],
    'azul':    [(np.array([100, 100, 100]), np.array([130, 255, 255]))],
}

CARPETA = 'assets/imgV'
SALIDA  = 'hsv_resultados.csv'

def contar_pixeles(hsv_img, rangos_lista):
    mascara = np.zeros(hsv_img.shape[:2], dtype=np.uint8)
    for bajo, alto in rangos_lista:
        mascara = cv2.bitwise_or(mascara, cv2.inRange(hsv_img, bajo, alto))
    return cv2.countNonZero(mascara), mascara

def analizar_imagen(ruta):
    img = cv2.imread(ruta)
    if img is None:
        return None

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    alto, ancho = img.shape[:2]
    total = alto * ancho

    resultados = {}
    mascaras = {}
    for color, rangos in RANGOS.items():
        pixeles, mascara = contar_pixeles(hsv, rangos)
        resultados[color] = round((pixeles / total) * 100, 2)
        mascaras[color] = mascara

    dominante = max(resultados, key=resultados.get)
    return resultados, dominante, img, mascaras

def main():
    extensiones = ['*.jpg', '*.jpeg', '*.png', '*.bmp']
    rutas = []
    for ext in extensiones:
        rutas += glob.glob(os.path.join(CARPETA, ext))

    if not rutas:
        print(f"No se encontraron imágenes en '{CARPETA}'.")
        return

    filas_csv = []

    for ruta in rutas:
        nombre = os.path.basename(ruta)
        resultado = analizar_imagen(ruta)
        if resultado is None:
            print(f"  [!] No se pudo leer: {nombre}")
            continue

        porcentajes, dominante, img, mascaras = resultado

        print(f"\nImagen: {nombre}")
        for color, pct in porcentajes.items():
            barra = '#' * int(pct / 2)
            print(f"  {color:10s}: {pct:5.2f}%  {barra}")
        print(f"  → Color dominante: {dominante.upper()}")

        fila = {'archivo': nombre, 'dominante': dominante}
        fila.update(porcentajes)
        filas_csv.append(fila)

        cv2.imshow(f"{nombre} — original", img)
        cv2.imshow(f"{nombre} — mascara {dominante}", mascaras[dominante])
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    columnas = ['archivo', 'dominante'] + list(RANGOS.keys())
    with open(SALIDA, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=columnas)
        writer.writeheader()
        writer.writerows(filas_csv)

    print(f"\nResultados guardados en '{SALIDA}'.")

if __name__ == '__main__':
    main()
