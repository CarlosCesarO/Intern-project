import streamlit as st
from roboflow import Roboflow
from PIL import Image
import os

import streamlit as st  # Importa o Streamlit para criar a interface web
from roboflow import Roboflow  # Importa a biblioteca Roboflow para usar o modelo de detecção
from PIL import Image  # Importa a PIL para manipulação de imagens
import os  # Importa o módulo os para operações com arquivos

API_KEY = "zpY7kScsVS5pX7ypwnX1"  # Chave de API do Roboflow
WORKSPACE = "broca-ai"  # Nome do workspace no Roboflow
PROJECT = "projeto_inova_coc_2025"  # Nome do projeto no Roboflow
VERSION = 3  # Versão do modelo

rf = Roboflow(api_key=API_KEY)  # Cria uma instância do Roboflow usando a chave de API
project = rf.workspace(WORKSPACE).project(PROJECT)  # Seleciona o projeto dentro do workspace
model = project.version(VERSION).model  # Seleciona a versão do modelo para detecção

st.set_page_config(page_title="Broca AI", layout="centered")  # Configura o título e layout da página
st.title("♻️ Detecção de Mariposas com Roboflow + Streamlit")  # Adiciona o título principal na interface

uploaded_file = st.file_uploader("Envie uma imagem para detecção", type=["jpg", "jpeg", "png", "heic"])  # Cria um campo para upload de imagem

if uploaded_file is not None:  # Se o usuário enviou uma imagem
    image = Image.open(uploaded_file)  # Abre a imagem enviada
    image = image.resize((640, 640))  # Redimensiona a imagem para 640x640 pixels
    image.save("temp_image.jpg", format="JPEG")  # Salva a imagem temporariamente em disco

    st.info("Realizando detecção...")  # Mostra mensagem de processamento

    result = model.predict("temp_image.jpg", confidence=50, overlap=50)  # Faz a predição usando o modelo Roboflow
    result.save("detected.jpg")  # Salva a imagem com as detecções desenhadas

    predictions = result.json()["predictions"]  # Extrai as predições do resultado em formato JSON

    num_mariposas = 0  # Inicializa o contador de mariposas
    num_vespas = 0  # Inicializa o contador de vespas
    num_cigarrinhas = 0  # Inicializa o contador de cigarrinhas
    num_outros = 0  # Inicializa o contador de outros insetos

    # Conta quantos insetos de cada categoria foram detectados
    for pred in predictions:
        class_id = pred.get("class_id")  # Pega o id da classe detectada
        if class_id == 0:
            num_mariposas += 1  # Incrementa mariposas
        elif class_id == 1:
            num_vespas += 1  # Incrementa vespas
        elif class_id == 2:
            num_cigarrinhas += 1  # Incrementa cigarrinhas
        elif class_id == 3:
            num_outros += 1  # Incrementa outros insetos

    total_insetos = len(predictions)  # Conta o total de insetos detectados

    os.remove("temp_image.jpg")  # Remove a imagem temporária do disco

    st.image("detected.jpg", caption="Resultado da Detecção", use_column_width=True)  # Mostra a imagem com as detecções

    st.success(f"✅ {total_insetos} insetos detectados na imagem")  # Mostra o total de insetos detectados

    col1, col2 = st.columns(2)  # Cria duas colunas para exibir métricas
    col3, col4 = st.columns(2)  # Cria mais duas colunas para exibir métricas

    with col1:
        st.metric("🦋 Mariposas", num_mariposas)  # Mostra o número de mariposas
    with col2:
        st.metric("🐝 Vespas", num_vespas)  # Mostra o número de vespas
    with col3:
        st.metric("🐞 Cigarrinhas", num_cigarrinhas)  # Mostra o número de cigarrinhas
    with col4:
        st.metric("🐜 Outros Insetos", num_outros)  # Mostra o número de outros insetos

    # Se houver insetos detectados, mostra detalhes de cada detecção
    if total_insetos > 0:
        st.write("### Detalhes das detecções:")  # Título da seção de detalhes
        for i, prediction in enumerate(predictions):  # Para cada predição
            class_id = prediction.get("class_id")  # Pega o id da classe
            confidence = round(prediction["confidence"] * 100, 1)  # Pega a confiança da detecção

            if class_id == 0:
                insect_type = "Mariposa"
            elif class_id == 1:
                insect_type = "Vespa"
            elif class_id == 2:
                insect_type = "Cigarrinha"
            elif class_id == 3:
                insect_type = "Outro Inseto"
            else:
                insect_type = "Inseto"

            st.write(f"**{insect_type} {i+1}:** Confiança de {confidence}%")  # Mostra o tipo e a confiança

        st.json(predictions)  # Mostra o JSON completo das predições