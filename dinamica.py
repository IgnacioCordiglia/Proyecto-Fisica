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

df['cantidad_de_movimiento'] = masa * df['velocidad']

df['fuerza'] = masa * df['aceleracion']

fuerza_rozamiento = masa * df_filtrado['aceleracion'].mean()

error_fuerza_rozamiento = sqrt(((media_aceleracion**2)*(error_masa**2))+((masa**2)*(error_aceleracion**2)))

coeficiente_rozamiento = abs(fuerza_rozamiento/(masa * 9.81))

fig, axs = plt.subplots(3, 1, figsize=(10, 8))


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

text_str = (f"Fuerza de rozamiento: {fuerza_rozamiento:.2f} N\n"
            f"Error: {error_fuerza_rozamiento:.2f} N\n"
            f"Coef. de rozamiento: {coeficiente_rozamiento:.2f}")
axs[1].text(0.95, 0.95, text_str, transform=axs[1].transAxes, fontsize=10,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))


plt.tight_layout()

plt.show()