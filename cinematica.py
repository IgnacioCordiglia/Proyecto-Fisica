import pandas as pd
import matplotlib.pyplot as plt
from pixel_to_meters import conversor

pixels_to_meters = conversor()

df = pd.read_csv('./output_data.csv')

FPS = 60

df['x_centro_metros'] = df['x_center'] * pixels_to_meters
df['tiempo'] = df['frame_index'] / FPS

initial_x = df['x_centro_metros'].iloc[0]
df['x_centro_metros'] = df['x_centro_metros'] - initial_x

df['velocidad'] = df['x_centro_metros'].diff(periods=3) / df['tiempo'].diff(periods=3)

df['aceleracion'] = df['velocidad'].diff(periods=20) / df['tiempo'].diff(periods=20)

t_min = 1
t_max = df['tiempo'].max()
df_filtrado = df[(df['tiempo'] >= t_min) & (df['tiempo'] <= t_max)]
media_aceleracion = df_filtrado['aceleracion'].mean()
error_aceleracion = df_filtrado['aceleracion'].std()

fig, axs = plt.subplots(3, 1, figsize=(10, 8))

axs[0].plot(df['tiempo'], df['x_centro_metros'], label='Posición (m)', color='b')
axs[0].set_xlabel('Tiempo (s)')
axs[0].set_ylabel('Posición (m)')
axs[0].set_title('Posición-tiempo')
axs[0].set_xlim(left=0)
axs[0].set_ylim(bottom=0)
axs[0].legend()
axs[0].grid(True)


axs[1].plot(df['tiempo'], df['velocidad'], label='Velocidad (m/s)', color='g')
axs[1].set_xlabel('Tiempo (s)')
axs[1].set_ylabel('Velocidad (m/s)')
axs[1].set_title('Velocidad-tiempo')
axs[1].set_xlim(left=0)
axs[1].set_ylim(bottom=-0.2)
axs[1].legend()
axs[1].grid(True)

limite_superior = media_aceleracion + error_aceleracion
limite_inferior = media_aceleracion - error_aceleracion


axs[2].plot(df['tiempo'], df['aceleracion'], label='Aceleración (m/s²)', color='r')
axs[2].axhline(y=media_aceleracion, color='purple', linestyle='--', label=f'Desaceleración media: {media_aceleracion:.4f} m/s²')
axs[2].set_xlabel('Tiempo (s)')
axs[2].set_ylabel('Aceleración (m/s²)')
axs[2].set_title('Aceleración-tiempo')
axs[2].axhline(y=limite_superior, color='blue', linestyle='--', label=f'error: +-{error_aceleracion}')
axs[2].axhline(y=limite_inferior, color='green', linestyle='--')
axs[2].fill_between(df['tiempo'], limite_superior, limite_inferior, color='gray', alpha=0.3)
axs[2].set_xlim(left=0)
axs[2].legend()
axs[2].grid(True)

# Ajustar el espacio entre los subplots
plt.tight_layout()

# Mostrar los gráficos en una ventana
plt.show()
