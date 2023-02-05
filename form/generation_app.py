import os
import requests
import logging
import streamlit as st
import yaml

from typing import List

logger = logging.getLevelName(__name__)

with open("./configs/streamlit.yaml", 'r') as stream:
    streamlit_config = yaml.safe_load(stream)

st.title("Generate 2D Game Assets")
existen_models = streamlit_config["existing_model"]


def train_request(uploaded_files: List[str], asset_type: str):
    url = streamlit_config["backend_hostname"] + \
        streamlit_config["train_endpoint"]
    files = [
        ('images', file.getvalue())
        for file in uploaded_files
    ]
    result = requests.post(
        url,
        files=files,
        data={"asset_type": asset_type}
    )
    return result


def generate_request(asset_type: str):
    url = streamlit_config["backend_hostname"] + \
        streamlit_config["generate_endpoint"]
    print(url, asset_type)
    result = requests.post(
        url,
        json={"asset_type": asset_type}  # diferent between json and data
    )
    return result


if __name__ == "__main__":
    uploaded_files = st.file_uploader(
        "Please choose a file",
        accept_multiple_files=True
    )

    datasets_names = os.listdir(existen_models)

    if uploaded_files:
        n = st.slider(
            label="Select a number of image in raw",
            min_value=1,
            max_value=len(uploaded_files) + 1,
            value=(len(uploaded_files) + 1) // 2
        )

        groups = []
        for i in range(0, len(uploaded_files), n):
            groups.append(uploaded_files[i: i + n])

        for group in groups:
            cols = st.columns(n)
            for i, image_file in enumerate(group):
                cols[i].image(image_file)

    with st.sidebar:
        if len(datasets_names) != 0:
            selected_dataset = st.selectbox(
                label="Select dataset",
                options=datasets_names
            )

            if selected_dataset:
                if st.button("Generate"):
                    images = generate_request(selected_dataset)

            asset_type = st.text_input(label="Asset type")
            if asset_type != "":
                if st.button("Train"):
                    images = train_request(uploaded_files, asset_type)
