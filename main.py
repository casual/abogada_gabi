import requests
import streamlit as st
import random
import time
import json


BASE_API_URL = "https://api.langflow.astra.datastax.com"
FLOW_ID = "3d0941d2-bfbb-45ec-acea-26a76ea9c61c"
ENDPOINT = "abogados" # You can set a specific endpoint name in the flow settings
TOKEN = "AstraCS:nKvakFfqBirsFDoLhRkomjaf:05f850a593878ac2672c53eca44338620461bd97aae5e6eab32d6699b6b60ded"

def run_flow(prompt: str) -> dict:
    with st.status("Procesando pedido..."):
        #api_url = f"{BASE_API_URL}/api/v1/run/{ENDPOINT}"

        api_url = f"{BASE_API_URL}/lf/{FLOW_ID}/api/v1/run/{ENDPOINT}"

        st.write("Ingresando a la base de conocimiento...")

        payload = {
        "input_value": prompt,
        "output_type": "chat",
        "input_type": "chat",
        }
        headers = {"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"}
        #headers = None

        st.write("Redactando la respuesta...")
        
        response = requests.post(api_url, json=payload, headers=headers)
        with st.chat_message("user"):
            st.markdown(response)

        return response.json()


def main():
    st.title("Estoy lista para ayudarte")

    #inicializa el historial
    if "messages" in st.session_state:
        st.session_state.messages = []

    #muestra el historial de mensajes
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdow(message["content"])

    if prompt := st.chat_input("Pídeme alguna tarea"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role":"user", "content": prompt})

        response = run_flow(prompt)
        response = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]

        st.session_state.messages.append({"role":"assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)


if __name__ == "__main__":
    main()