import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm

# Cargar el CSV con los datos de la bounding box
df = pd.read_csv('./output_data.csv')

# Calcular el tamaño de la bounding box en x
df['box_size_x'] = df['x_max'] - df['x_min']

# Calcular el tamaño promedio y la desviación estándar
mean_size_x = df['box_size_x'].mean()
std_dev_size_x = df['box_size_x'].std()

# Imprimir resultados
print(f"Tamaño promedio de la bounding box en x: {mean_size_x:.2f}")
print(f"Desviación estándar del tamaño en x: {std_dev_size_x:.2f}")

# Graficar la distribución del tamaño de la bounding box en x
plt.figure(figsize=(10, 6))
sns.histplot(df['box_size_x'], bins=30, kde=True, color='skyblue', stat='density', label='Datos')
xmin, xmax = plt.xlim()

# Superponer la curva de distribución normal
x_values = np.linspace(xmin, xmax, 100)
plt.plot(x_values, norm.pdf(x_values, mean_size_x, std_dev_size_x), 'r-', lw=2, label='Curva Normal')

# Etiquetas y título
plt.xlabel('Tamaño de la Bounding Box en x (pixeles)')
plt.ylabel('Densidad')
plt.title('Distribución del Tamaño de la Bounding Box en x')
plt.legend()
plt.grid(True)
plt.show()