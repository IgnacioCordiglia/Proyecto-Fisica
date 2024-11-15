import pandas as pd
import matplotlib.pyplot as plt
from math import sqrt
from pixel_to_meters import conversor

pixels_to_meters = conversor()
df = pd.read_csv('./output_data.csv')
FPS = 60

df['x_centro_metros'] = df['x_center'] * pixels_to_meters
df['tiempo'] = df['frame_index'] / FPS

initial_x = df['x_centro_metros'].iloc[0]
df['x_centro_metros'] = df['x_centro_metros'] - initial_x

initial_time = df['tiempo'].iloc[0]
df['tiempo'] = df['tiempo'] - initial_time

df['velocidad'] = df['x_centro_metros'].diff(periods=15) / df['tiempo'].diff(periods=15)

velocidad_post_golpe = df['velocidad'].max()

df['aceleracion'] = df['velocidad'].diff(periods=15) / df['tiempo'].diff(periods=15)
media_aceleracion = df['aceleracion'].mean()
error_aceleracion = df['aceleracion'].std()

masa = 0.04593  # en kg
error_masa = 0.00001

cant_mov_final = velocidad_post_golpe * masa

df['fuerza'] = masa * df['aceleracion']

fuerza_rozamiento = df['fuerza'].mean()

error_fuerza_rozamiento = sqrt(((media_aceleracion**2)*(error_masa**2))+((masa**2)*(error_aceleracion**2)))

df['trabajo'] = df['x_centro_metros'] * -fuerza_rozamiento

df['energia_cinetica'] = 1/2 * masa * df['velocidad']

coeficiente_rozamiento = abs(fuerza_rozamiento/(masa * 9.81))

fig, axs = plt.subplots(2, 1, figsize=(10, 8))

# Gráfico de trabajo - energia cinetica
axs[0].plot(df['x_centro_metros'], df['trabajo'], label='Trabajo (J)', color='purple')
axs[0].plot(df['x_centro_metros'], df['energia_cinetica'], label='Energia Cinetica (J)', color='red')
axs[0].set_xlabel('Posicion (m)')
axs[0].set_ylabel('Cantidad de movimiento (kg·m/s)')
axs[0].set_title('Cantidad de movimiento - tiempo')
axs[0].legend()
axs[0].grid(True)

# Ajustar el espacio entre los subplots
plt.tight_layout()

# Mostrar los gráficos en una ventana
plt.show()