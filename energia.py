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

df['cantidad_de_movimiento'] = masa * df['velocidad']

df['fuerza'] = masa * df['aceleracion']

fuerza_rozamiento = masa * df_filtrado['aceleracion'].mean()

error_fuerza_rozamiento = sqrt(((media_aceleracion**2)*(error_masa**2))+((masa**2)*(error_aceleracion**2)))

df['trabajo'] = df['x_centro_metros'] * -fuerza_rozamiento

df['energia_cinetica'] = 1/2 * masa * (df['velocidad']**2)

t = df['tiempo'].values
velocity_fit = 2.05 - 0.7054 * t
velocidad_max_fit = velocity_fit.max()
cant_mov_final_fit = velocidad_max_fit * masa

coeficiente_rozamiento = abs(fuerza_rozamiento/(masa * 9.81))

energia_cinetica_inicial = df['trabajo'].max()
energia_cinetica_fit = energia_cinetica_inicial - df['x_centro_metros'] * -fuerza_rozamiento

radio = 0.021 # en m

inercia = 3/5 * masa * radio**2

df['velocidad_angular'] = df['velocidad'] / radio

df['energia_cinetica_rotacional'] = 1/2 * inercia * df['velocidad_angular']

df['energia_cinetica_total'] = df['energia_cinetica'] + df['energia_cinetica_rotacional']

fuerza_golpe = cant_mov_final / 0.0125 #Tiempo de contacto con la pelota
fuerza_golpe_fit = cant_mov_final_fit / 0.0125


fig, axs = plt.subplots(1, 2, figsize=(14, 8), gridspec_kw={'width_ratios': [2, 1]})


axs[0].plot(df['x_centro_metros'], df['trabajo'], label='Trabajo (J)', color='purple')
axs[0].plot(df['x_centro_metros'], df['energia_cinetica'], label='Energia Cinetica (J)', color='red')
axs[0].plot(df['x_centro_metros'], df['energia_cinetica_rotacional'], label='Energia Cinetica rotacional (J)', color='pink')
axs[0].plot(df['x_centro_metros'], df['energia_cinetica_total'], label='Energia Cinetica total (J)', color='brown')
axs[0].plot(df['x_centro_metros'], energia_cinetica_fit, label='Energia cinetica (curve_fit)', color='black')
axs[0].set_xlabel('Posicion (m)')
axs[0].set_ylabel('Energia (J)')
axs[0].set_title('Energia - posicion')
axs[0].legend()
axs[0].grid(True)

texto = (
    f"Impulso: {df['cantidad_de_movimiento'].max():.4f} N·s\n"
    f"Impulso (curve fit): {cant_mov_final_fit:.4f} N·s\n"
    f"Velocidad post-golpe: {velocidad_post_golpe:.4f} m/s\n"
    f"Velocidad post-golpe (curve fit): {velocidad_max_fit:.4f} m/s\n"
    f"Fuerza contacto del golpe: {fuerza_golpe:.4f} N\n"
    f"Fuerza contacto del golpe (curve fit): {fuerza_golpe_fit:.4f} N\n"
)
axs[1].axis('off') 
axs[1].text(0.1, 0.5, texto, ha='left', va='center', fontsize=12)


plt.tight_layout()

# Mostrar los gráficos
plt.show()
