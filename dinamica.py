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

df['aceleracion'] = df['velocidad'].diff(periods=15) / df['tiempo'].diff(periods=15)
media_aceleracion = df['aceleracion'].mean()
error_aceleracion = df['aceleracion'].std()

masa = 0.04593  # en kg
error_masa = 0.00001

df['cantidad_de_movimiento'] = masa * df['velocidad']

df['fuerza'] = masa * df['aceleracion']

fuerza_rozamiento = df['fuerza'].mean()

error_fuerza_rozamiento = sqrt(((media_aceleracion**2)*(error_masa**2))+((masa**2)*(error_aceleracion**2)))


print("Fuerza rozamiento: ", fuerza_rozamiento , "+-", error_fuerza_rozamiento)

coeficiente_rozamiento = abs(fuerza_rozamiento/(masa * 9.81))
print("Coeficiente rozamiento: ", coeficiente_rozamiento)


fig, axs = plt.subplots(2, 1, figsize=(10, 8))


# Gráfico de cantidad de movimiento
axs[0].plot(df['tiempo'], df['cantidad_de_movimiento'], label='Cantidad de movimiento (kg·m/s)', color='purple')
axs[0].set_xlabel('Tiempo (s)')
axs[0].set_ylabel('Cantidad de movimiento (kg·m/s)')
axs[0].set_title('Cantidad de movimiento - tiempo')
axs[0].set_xlim(left=0)
axs[0].set_ylim(bottom=0)
axs[0].legend()
axs[0].grid(True)

limite_superior = fuerza_rozamiento + error_fuerza_rozamiento
limite_inferior = fuerza_rozamiento - error_fuerza_rozamiento

axs[1].plot(df['tiempo'], df['fuerza'], label='Fuerza (N)', color='red')
axs[1].set_xlabel('Tiempo (s)')
axs[1].set_ylabel('Fuerza (N)')
axs[1].set_title('Fuerza - tiempo')
axs[1].set_xlim(left=0)
axs[1].axhline(y=fuerza_rozamiento, color='purple', linestyle='--', label=f'Fuerza media: {fuerza_rozamiento:.2f} N')
axs[1].axhline(y=limite_superior, color='blue', linestyle='--', label=f'Fuerza + error: {limite_superior:.2f} N')
axs[1].axhline(y=limite_inferior, color='green', linestyle='--', label=f'Fuerza - error: {limite_inferior:.2f} N')
axs[1].fill_between(df['tiempo'], limite_superior, limite_inferior, color='gray', alpha=0.3, label='Error en fuerza')

# Ajustar el espacio entre los subplots
plt.tight_layout()

# Mostrar los gráficos en una ventana
plt.show()