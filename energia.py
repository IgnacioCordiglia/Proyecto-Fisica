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

df['velocidad'] = df['x_centro_metros'].diff(periods=3) / df['tiempo'].diff(periods=3)

df['aceleracion'] = df['velocidad'].diff(periods=7) / df['tiempo'].diff(periods=7)
t_min = 1
t_max = df['tiempo'].max()
df_filtrado = df[(df['tiempo'] >= t_min) & (df['tiempo'] <= t_max)]
media_aceleracion = df_filtrado['aceleracion'].mean()
error_aceleracion = df_filtrado['aceleracion'].std()

masa = 0.04593  # en kg
error_masa = 0.00001
velocidad_post_golpe = df['velocidad'].max()
cant_mov_final = velocidad_post_golpe * masa

df['fuerza'] = masa * df['aceleracion']

fuerza_rozamiento = masa * df_filtrado['aceleracion'].mean()

error_fuerza_rozamiento = sqrt(((media_aceleracion**2)*(error_masa**2))+((masa**2)*(error_aceleracion**2)))

df['trabajo'] = df['x_centro_metros'] * -fuerza_rozamiento

df['energia_cinetica'] = 1/2 * masa * (df['velocidad']**2)

coeficiente_rozamiento = abs(fuerza_rozamiento/(masa * 9.81))

fuerza_golpe = cant_mov_final / 0.0125

# Crear un diseño con dos columnas
fig, axs = plt.subplots(1, 2, figsize=(14, 8), gridspec_kw={'width_ratios': [2, 1]})

# Gráfico en la primera columna
axs[0].plot(df['x_centro_metros'], df['trabajo'], label='Trabajo (J)', color='purple')
axs[0].plot(df['x_centro_metros'], df['energia_cinetica'], label='Energia Cinetica (J)', color='red')
axs[0].set_xlabel('Posicion (m)')
axs[0].set_ylabel('Cantidad de movimiento (kg·m/s)')
axs[0].set_title('Cantidad de movimiento - tiempo')
axs[0].legend()
axs[0].grid(True)

texto = (
    f"Velocidad post-golpe: {velocidad_post_golpe:.2f} m/s\n"
    f"Fuerza de golpe: {fuerza_golpe:.2f} N"
)
axs[1].axis('off')  # Apagar los ejes de la segunda columna
axs[1].text(0.1, 0.5, texto, ha='left', va='center', fontsize=12)

# Ajustar el espacio entre los subplots
plt.tight_layout()

# Mostrar los gráficos
plt.show()
