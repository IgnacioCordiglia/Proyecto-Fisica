import pandas as pd
import matplotlib.pyplot as plt
from pixel_to_meters import conversor

# Convertidor de pixeles a metros
pixels_to_meters = conversor()

# Cargar los datos desde el archivo CSV
df = pd.read_csv('./output_data.csv')

FPS = 60  # Frames por segundo

# Convertir los pixeles a metros y calcular el tiempo
df['x_centro_metros'] = df['x_center'] * pixels_to_meters
df['tiempo'] = df['frame_index'] / FPS

# Alinear la posición inicial al origen
initial_x = df['x_centro_metros'].iloc[0]
df['x_centro_metros'] = df['x_centro_metros'] - initial_x

# Alinear el tiempo inicial al origen
initial_time = df['tiempo'].iloc[0]
df['tiempo'] = df['tiempo'] - initial_time

# Calcular la velocidad como Δx / Δt (diferencias finitas)
df['velocidad'] = df['x_centro_metros'].diff(periods=15) / df['tiempo'].diff(periods=15)

# Calcular la aceleración como Δv / Δt (diferencias finitas)
df['aceleracion'] = df['velocidad'].diff(periods=15) / df['tiempo'].diff(periods=15)

# Calcula la media de la aceleración
media_aceleracion = df['aceleracion'].mean()
error_aceleracion = df['aceleracion'].std()

# Crear una figura con 3 subplots (uno para cada gráfico)
fig, axs = plt.subplots(3, 1, figsize=(10, 8))

# Gráfico de posición
axs[0].plot(df['tiempo'], df['x_centro_metros'], label='Posición (m)', color='b')
axs[0].set_xlabel('Tiempo (s)')
axs[0].set_ylabel('Posición (m)')
axs[0].set_title('Posición-tiempo')
axs[0].set_xlim(left=0)
axs[0].set_ylim(bottom=0)
axs[0].legend()
axs[0].grid(True)

# Gráfico de velocidad
axs[1].plot(df['tiempo'], df['velocidad'], label='Velocidad (m/s)', color='g')
axs[1].set_xlabel('Tiempo (s)')
axs[1].set_ylabel('Velocidad (m/s)')
axs[1].set_title('Velocidad-tiempo')
axs[1].set_xlim(left=0)
axs[1].set_ylim(bottom=0)
axs[1].legend()
axs[1].grid(True)

limite_superior = media_aceleracion + error_aceleracion
limite_inferior = media_aceleracion - error_aceleracion
# Gráfico de aceleración
axs[2].plot(df['tiempo'], df['aceleracion'], label='Aceleración (m/s²)', color='r')
axs[2].axhline(y=media_aceleracion, color='purple', linestyle='--', label=f'Aceleración media: {media_aceleracion:.2f} m/s²')
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
