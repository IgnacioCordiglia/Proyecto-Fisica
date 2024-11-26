import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from pixel_to_meters import conversor

def quadratic_model(t, a, b, c):
    return a * t**2 + b * t + c

def lineaRecta(t,a,b):
    return a*t + b

# Cargar los datos de posición y tiempo desde el CSV
df = pd.read_csv('./output_data.csv')

# Factor de conversión de píxeles a metros
pixels_to_meters = conversor()

# Convertir 'x_centro' de píxeles a metros y alinear la posición inicial al origen
df['x_centro_metros'] = (df['x_center'] * pixels_to_meters) - (df['x_center'].iloc[0] * pixels_to_meters)

# Velocidad de fotogramas (FPS)
FPS = 60
df['tiempo'] = (df['frame_index'] / FPS) - (df['frame_index'].iloc[0] / FPS)

# Datos de tiempo y posición
t = df['tiempo'].values
x = df['x_centro_metros'].values

# Ajustar el modelo cuadrático para obtener a, b y c
params_quadratic, _ = curve_fit(quadratic_model, t, x)
a_quad, b_quad, c_quad = params_quadratic

# Derivadas analíticas de la función cuadrática
# Velocidad (primera derivada): v(t) = 2*a*t + b
velocity_fit = 2 * a_quad * t + b_quad
# Aceleración (segunda derivada): a(t) = 2*a
acceleration_fit = np.full_like(t, 2 * a_quad)

# Calcular velocidad y aceleración a través de diferencias finitas (originales)
df['velocidad'] = df['x_centro_metros'].diff(periods=2) / df['tiempo'].diff(periods=2)
df['aceleracion'] = df['velocidad'].diff(periods=5) / df['tiempo'].diff(periods=5)
masa = 0.04593  # en kg

df['cantidad_de_movimiento'] = masa * df['velocidad']
df['fuerza'] = masa * df['aceleracion']

cant_mov_fit = velocity_fit * masa
fuerza_fit = acceleration_fit * masa

# Comparar graficando
fig, axs = plt.subplots(4, 1, figsize=(12, 8))

# Gráfico de comparación de velocidades
axs[0].plot(t, velocity_fit, label='Velocidad (curve_fit)', color='black')
axs[0].plot(df['tiempo'], df['velocidad'], label='Velocidad (original)', color='g', alpha=0.5)
axs[0].set_xlabel('Tiempo (s)')
axs[0].set_ylabel('Velocidad (m/s)')
axs[0].set_title('Comparación de Velocidad')
axs[0].legend()
axs[0].grid(True)

# Gráfico de comparación de aceleraciones
axs[1].plot(t, acceleration_fit, label='Aceleración (curve_fit)', color='black')
axs[1].plot(df['tiempo'], df['aceleracion'], label='Aceleración (original)', color='r', alpha=0.5)
axs[1].set_xlabel('Tiempo (s)')
axs[1].set_ylabel('Aceleración (m/s²)')
axs[1].set_title('Comparación de Aceleración')
axs[1].legend()
axs[1].grid(True)

axs[2].plot(t, cant_mov_fit, label='Cantidad de movimiento (curve_fit)', color='black')
axs[2].plot(df['tiempo'], df['cantidad_de_movimiento'], label='Cantidad de movimiento (original)', color='purple', alpha=0.5)
axs[2].set_xlabel('Tiempo (s)')
axs[2].set_ylabel('Cant. de movimiento (kg·m/s)')
axs[2].set_title('Comparación de Cantidad de Movimiento')
axs[2].legend()
axs[2].grid(True)

axs[3].plot(t, fuerza_fit, label='Fuerza (curve_fit)', color='black')
axs[3].plot(df['tiempo'], df['fuerza'], label='Fuerza (original)', color='orange', alpha=0.5)
axs[3].set_xlabel('Tiempo (s)')
axs[3].set_ylabel('Fuerza (N)')
axs[3].set_title('Comparación de Fuerza')
axs[3].legend()
axs[3].grid(True)

plt.tight_layout()
plt.show()
