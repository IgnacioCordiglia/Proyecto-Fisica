import math
import supervision as sv
import cv2


def conversor():
    #Coordenadas en test.mp4
    ball_position = (185, 844)
    hole_position = (1716, 876)

    #Distancia en pixeles equivalente a 3 metros:
    distance_pixels = math.sqrt((hole_position[0] - ball_position[0])**2 + (hole_position[1] - ball_position[1])**2)

    distance_meters = 3

    pixels_to_meters = distance_meters / distance_pixels

    return pixels_to_meters
