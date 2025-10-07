# frontend.py (v1 - State Reset Fix)

import streamlit as st
import requests
from PIL import Image
import io
import os

# --- CONFIGURATION ---
API_URL = os.getenv("API_URL_V1")
# --- END CONFIGURATION ---

# --- SESSION STATE INITIALIZATION ---
if "active_effect" not in st.session_state:
    st.session_state.active_effect = None
if "processed_image" not in st.session_state:
    st.session_state.processed_image = None
if "processed_image_bytes" not in st.session_state:
    st.session_state.processed_image_bytes = None
if "last_uploaded_bytes" not in st.session_state:
    st.session_state.last_uploaded_bytes = None
# --- END SESSION STATE ---

st.title("FocalPoint AI - v1")
st.write("Upload an image and select an effect to apply.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

if uploaded_file is not None:
    current_file_bytes = uploaded_file.getvalue()
    
    # --- LOGIC TO RESET STATE ---
    if st.session_state.last_uploaded_bytes != current_file_bytes:
        st.session_state.last_uploaded_bytes = current_file_bytes
        st.session_state.active_effect = None
        st.session_state.processed_image = None
        st.session_state.processed_image_bytes = None
    # --- END OF NEW LOGIC ---
    
    # --- CONTROLS SECTION ---
    st.subheader("Apply an Effect")
    effects = {"Remove BG": "remove_bg", "Bokeh": "bokeh", "Anonymize": "anonymize"}

    def handle_effect_click(effect_name):
        st.session_state.active_effect = effect_name
        with st.spinner(f'Applying {effect_name}...'):
            try:
                files = {'file': st.session_state.last_uploaded_bytes}
                params = {'effect': effect_name}
                response = requests.post(API_URL, files=files, data=params, timeout=60)
                if response.status_code == 200:
                    st.session_state.processed_image_bytes = response.content
                    st.session_state.processed_image = Image.open(io.BytesIO(response.content))
                else:
                    st.error(f"Error from API: {response.status_code} - {response.text}")
                    st.session_state.processed_image = None
            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {e}")
                st.session_state.processed_image = None

    # st.markdown('<div class="effect-buttons">', unsafe_allow_html=True)
    button_cols = st.columns(len(effects))
    for i, (btn_label, effect_key) in enumerate(effects.items()):
        button_type = "primary" if st.session_state.active_effect == effect_key else "secondary"
        button_cols[i].button(
            btn_label,
            key=effect_key,
            type=button_type,
            on_click=handle_effect_click,
            args=(effect_key,)
        )
    # --- END CONTROLS SECTION ---

    st.divider()

    # --- DISPLAY SECTION ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original Image")
        st.image(current_file_bytes, caption='Your uploaded image.', width='stretch')

    with col2:
        st.subheader("Processed Image")
        if st.session_state.processed_image:
            st.image(st.session_state.processed_image, caption='The result of the effect.', width='stretch')
            
            file_extension = "png" if st.session_state.active_effect == 'remove_bg' else "jpg"
            file_name = f"processed_image.{file_extension}"
            st.download_button(
                label="Download Image",
                data=st.session_state.processed_image_bytes,
                file_name=file_name,
                mime=f"image/{file_extension}"
            )
        else:
            st.info("Click an effect button above to see the result here.")
    # --- END DISPLAY SECTION ---