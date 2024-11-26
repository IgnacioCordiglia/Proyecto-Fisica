import pandas as pd
from math import sqrt
from pixel_to_meters import conversor

df = pd.read_csv('./output_data.csv')

masa = 0.04593  # en kg
error_masa = 0.00001
#velocidad_post_golpe = df['velocidad'].max()
#cant_mov_final = velocidad_post_golpe * masa

#df['fuerza'] = masa * df['aceleracion']

#fuerza_rozamiento = masa * df_filtrado['aceleracion'].mean()

#error_fuerza_rozamiento = sqrt(((media_aceleracion**2)*(error_masa**2))+((masa**2)*(error_aceleracion**2)))

#df['trabajo'] = df['x_centro_metros'] * -fuerza_rozamiento

#df['energia_cinetica'] = 1/2 * masa * (df['velocidad']**2)

#coeficiente_rozamiento = abs(fuerza_rozamiento/(masa * 9.81))

#fuerza_golpe = cant_mov_final / 0.0125

def getDFTiempo():
    FPS = 60
    return df['frame_index'] / FPS

def getDFPosicion():  
    pixels_to_meters = conversor()
    df['x_centro_metros'] = df['x_center'] * pixels_to_meters
    initial_x = df['x_centro_metros'].iloc[0]
    return df['x_centro_metros'] - initial_x

def getDFVelocidad():
    return getDFPosicion().diff(periods=3) / getDFTiempo().diff(periods=3)

def getDFAceleracion():
    return getDFVelocidad().diff(periods=7) / getDFTiempo().diff(periods=7)

def getDFFiltrado():
    t_min = 1
    t_max = getDFTiempo().max()
    dfFiltrado = df[(getDFTiempo() >= t_min) & (getDFTiempo() <= t_max)]
    return df , {'dfFiltrado': dfFiltrado,
                 'media': dfFiltrado['aceleracion'].mean(),
                 'error':dfFiltrado['aceleracion'].std()}
