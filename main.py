from inference import InferencePipeline 
from inference.core.interfaces.stream.sinks import render_boxes

# Creamos una tubería de inferencia y la configuramos
pipeline = InferencePipeline.init(
    model_id='golf-j71gp/1',  
    video_reference='./test.mp4',  
    on_prediction=render_boxes,  
    api_key='rSItXiQ0hHO8DMAOCbTe'  
)

# Iniciamos el proceso de inferencia en el video
pipeline.start()

# Esperamos a que el proceso de inferencia termine
pipeline.join()