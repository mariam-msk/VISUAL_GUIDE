import gradio as gr
import cv2
import base64
import requests
import pyttsx3
import tempfile

# OpenAI API Key
OPENAI_API_KEY = "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"

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def analyze_image(image):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        image.save(temp_file.name)
        temp_file_path = temp_file.name
    
    base64_image = image_to_base64(temp_file_path)
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {"role": "system", "content": "You are an AI assistant that describes images for visually impaired users."},
            {"role": "user", "content": "Describe this image:"}
        ],
        "max_tokens": 200,
        "temperature": 0.7,
        "image": {
            "type": "base64",
            "data": base64_image
        }
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        description = result['choices'][0]['message']['content']
        return description
    else:
        return "Error analyzing image: " + response.text

def speak_text(description):
    tts_engine.say(description)
    tts_engine.runAndWait()
    return "Speaking..."

def gradio_interface(image):
    description = analyze_image(image)
    return description, speak_text(description)

# Gradio UI
iface = gr.Interface(
    fn=gradio_interface,
    inputs=gr.Image(type="pil"),
    outputs=[gr.Textbox(label="Image Description"), gr.Textbox(label="Text-to-Speech Status")],
    title="AI Vision Assistant for the Visually Impaired",
    description="Upload an image and get a spoken description using AI."
)

iface.launch()
