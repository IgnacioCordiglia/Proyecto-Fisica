import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from pixel_to_meters import conversor

def quadratic_model(t, a, b, c):
    return a * t**2 + b * t + c

# Cargar los datos de posición y tiempo desde el CSV
df = pd.read_csv('./output_data.csv')

# Factor de conversión de píxeles a metros
pixels_to_meters = conversor()

# Convertir 'x_centro' de píxeles a metros
df['x_centro_metros'] = df['x_center'] * pixels_to_meters
df['x_centro_metros'] = df['x_centro_metros'] - df['x_centro_metros'].iloc[0]

# Velocidad de fotogramas (FPS)
FPS = 60
df['tiempo'] = df['frame_index'] / FPS
df['tiempo'] = df['tiempo'] - df['tiempo'].iloc[0]

# Datos de tiempo y posición
t = df['tiempo'].values
x = df['x_centro_metros'].values

# Ajustar el modelo cuadrático
params_quadratic, covariance_quadratic = curve_fit(quadratic_model, t, x)
a_quad, b_quad, c_quad = params_quadratic

# Graficar los datos originales
plt.figure(figsize=(10,6))
plt.scatter(t, x, label='Datos originales', color='blue')
# Graficar el ajuste cuadrático
plt.plot(t, quadratic_model(t, *params_quadratic), label=f'Ajuste cuadrático: a={a_quad:.4f}, b={b_quad:.4f}, c={c_quad:.4f}', color='green')

plt.xlabel('Tiempo (segundos)')
plt.ylabel('Posición (metros)')
plt.title('Ajuste de Posición-Tiempo con curve_fit')
plt.legend()
plt.grid(True)
plt.show()

# Cálculo del error de ajuste (Error cuadrático medio)
residuals_quadratic = x - quadratic_model(t, *params_quadratic)

# Error cuadrático medio (RMSE)
rmse_quadratic = np.sqrt(np.mean(residuals_quadratic**2))

print(f"Error cuadrático medio - Ajuste cuadrático: {rmse_quadratic:.4f}")