import math
import supervision as sv
import cv2


def conversor():
    #Coordenadas en test.mp4
    tee1 = (288, 1154)
    tee2 = (3114, 1154)

    #Distancia en pixeles equivalente a 3 metros:
    distance_pixels = math.sqrt((tee2[0] - tee1[0])**2 + (tee2[1] - tee1[1])**2)

    distance_meters = 3

    pixels_to_meters = distance_meters / distance_pixels

    return pixels_to_meters
