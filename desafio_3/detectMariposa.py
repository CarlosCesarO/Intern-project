from roboflow import Roboflow
from PIL import Image
import os

API_KEY = ""
WORKSPACE = ""
PROJECT = ""
VERSION = 3

rf = Roboflow(api_key=API_KEY)
project = rf.workspace(WORKSPACE).project(PROJECT)
model = project.version(VERSION).model

image = Image.open("./mariposas.jpeg")
image = image.resize((640, 640))  
image.save("temp_image.jpg", format="JPEG")

result = model.predict("temp_image.jpg", confidence=50, overlap=50)
result.save("detected.jpg")

predictions = result.json()["predictions"]

num_mariposas = 0  
num_vespas = 0     
num_cigarrinhas = 0  
num_outros = 0     

for pred in predictions:
    class_id = pred.get("class_id")
    if class_id == 0:
        num_mariposas += 1
    elif class_id == 1:
        num_vespas += 1
    elif class_id == 2:
        num_cigarrinhas += 1
    elif class_id == 3:
        num_outros += 1

total_insetos = len(predictions)

os.remove("temp_image.jpg")

print(f"{total_insetos} insetos detectados na imagem")
print(f"Mariposas: {num_mariposas}")
print(f"Vespas: {num_vespas}")
print(f"Cigarrinhas: {num_cigarrinhas}")
print(f"Outros Insetos: {num_outros}")

