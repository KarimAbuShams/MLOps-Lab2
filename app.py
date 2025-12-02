import gradio as gr
import requests

RENDER_API_URL = "https://mlops-lab2-karim.onrender.com" 

def predict(image_file):
    try:
        files = {'file': open(image_file, 'rb')}
        response = requests.post(f"{RENDER_API_URL}/predict", files=files)
        return response.json()
    except Exception as e:
        return str(e)

interface = gr.Interface(
    fn=predict,
    inputs=gr.Image(type="filepath"),
    outputs="text",
    title="Image Clasificator MLOps Lab 2",
    description="Upload an image to get a prediction from the API."
)

if __name__ == "__main__":
    interface.launch()
