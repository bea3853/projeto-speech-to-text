import streamlit as st
from typing import Optional

def render_camera_component() -> Optional[bytes]:
    """Renderiza a interface do feed de vídeo nativo da câmera utilizando a API estável do Streamlit."""
    st.subheader("📷 Entrada de Vídeo / Câmera")
    
    img_file = st.camera_input("Alinhe o objeto e dispare a captura")
    
    if img_file is not None:
        bytes_data = img_file.getvalue()
        return bytes_data
    return None