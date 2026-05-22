import cv2
import numpy as np
import os
import sys

RANGOS = {
    'rojo':    [(np.array([0, 100, 100]),   np.array([10, 255, 255])),
                (np.array([170, 100, 100]), np.array([180, 255, 255]))],
    'naranja': [(np.array([11, 100, 100]),  np.array([25, 255, 255]))],
    'amarillo':[(np.array([26, 100, 100]),  np.array([34, 255, 255]))],
    'verde':   [(np.array([35, 50, 50]),    np.array([85, 255, 255]))],
    'azul':    [(np.array([100, 100, 100]), np.array([130, 255, 255]))],
}

CARPETA_SALIDA = 'capturas'
INTERVALO      = 30   # extraer 1 frame cada N frames

def color_dominante(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    total = frame.shape[0] * frame.shape[1]
    maxpix, dominante = 0, 'ninguno'
    for color, rangos in RANGOS.items():
        mascara = np.zeros(hsv.shape[:2], dtype=np.uint8)
        for bajo, alto in rangos:
            mascara = cv2.bitwise_or(mascara, cv2.inRange(hsv, bajo, alto))
        pixeles = cv2.countNonZero(mascara)
        if pixeles > maxpix:
            maxpix, dominante = pixeles, color
    porcentaje = round((maxpix / total) * 100, 2)
    return dominante, porcentaje

def procesar_video(ruta_video):
    cap = cv2.VideoCapture(ruta_video)
    if not cap.isOpened():
        print(f"No se pudo abrir el video: {ruta_video}")
        return

    nombre_video = os.path.splitext(os.path.basename(ruta_video))[0]
    carpeta = os.path.join(CARPETA_SALIDA, nombre_video)
    os.makedirs(carpeta, exist_ok=True)

    fps_total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps       = cap.get(cv2.CAP_PROP_FPS) or 30
    print(f"\nVideo: {nombre_video}  |  {fps_total} frames  |  {fps:.1f} fps")
    print(f"Extrayendo 1 frame cada {INTERVALO} frames...\n")

    timeline = []
    frame_num = 0
    guardados = 0

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        if frame_num % INTERVALO == 0:
            dominante, pct = color_dominante(frame)
            segundo = round(frame_num / fps, 1)

            nombre_frame = f"{nombre_video}_f{frame_num:06d}.jpg"
            ruta_frame   = os.path.join(carpeta, nombre_frame)
            cv2.imwrite(ruta_frame, frame)

            timeline.append((segundo, dominante, pct))
            print(f"  [{segundo:7.1f}s]  frame {frame_num:6d}  →  {dominante:10s} {pct:.1f}%")
            guardados += 1

        frame_num += 1

        if cv2.waitKey(1) == 27:
            print("\nInterrumpido por el usuario.")
            break

    cap.release()

    print(f"\n{guardados} frames guardados en '{carpeta}/'")
    print("\n--- Línea de tiempo cromática ---")
    for segundo, color, pct in timeline:
        bloque = '█' * int(pct / 5)
        print(f"  {segundo:7.1f}s  {color:10s}  {bloque}")

def main():
    if len(sys.argv) > 1:
        rutas = sys.argv[1:]
    else:
        print("Uso: python HSV_Video.py <video.mp4> [video2.mp4 ...]")
        print("Buscando videos en la carpeta actual...")
        import glob
        rutas = glob.glob('*.mp4') + glob.glob('*.avi') + glob.glob('*.mkv')
        if not rutas:
            print("No se encontraron videos. Proporciona la ruta como argumento.")
            return

    for ruta in rutas:
        procesar_video(ruta)

if __name__ == '__main__':
    main()
