import supervision as sv
import pandas as pd
from inference import get_model

# Carga el modelo preentrenado de un repositorio externo utilizando la API key
# El modelo "golf-j71gp/1" está diseñado específicamente para detectar pelotas de golf
model = get_model(
    model_id='golf-j71gp/1',
    api_key='rSItXiQ0hHO8DMAOCbTe'
)

# Crea un generador para obtener los cuadros individuales del video "test.mp4"
# Cada iteración de este generador proporcionará un cuadro del video
frames_generator = sv.get_video_frames_generator('./test.mp4')

# Abre un archivo CSV para almacenar los resultados de la detección
# El bloque "with" asegura que el archivo se cierre correctamente
with sv.CSVSink('./output_data.csv') as sink:
    # Itera sobre cada cuadro del video
    for frame_index, frame in enumerate(frames_generator):
        # Realiza la inferencia del modelo en el cuadro actual
        # Los resultados de la inferencia suelen ser una lista de detecciones
        results = model.infer(frame)[0]
        
        # Convierte los resultados de la inferencia en un objeto Detections
        # Esto facilita el manejo de las detecciones y permite agregar datos adicionales
        detections = sv.Detections.from_inference(results)

        # Crea un diccionario con información adicional sobre el cuadro
        extra_data = {
            "frame_index": frame_index  # Índice del cuadro actual
        }

        # Agrega las detecciones y los datos adicionales al archivo CSV
        sink.append(detections, extra_data)

# Carga los datos del archivo CSV en un DataFrame de pandas
df = pd.read_csv('./output_data.csv')

# Filtra el DataFrame para obtener solo las detecciones de la clase "golf ball"
new_df = df[df['class_id'] == 1].copy()

# Calcula las coordenadas del centro de cada detección
new_df['x_center'] = round(((new_df['x_min'] + new_df['x_max']) / 2))
new_df['y_center'] = round(((new_df['y_min'] + new_df['y_max']) / 2))

# Sobreescribe el archivo CSV con los datos filtrados y procesados
new_df.to_csv('./output_data.csv', index=False)