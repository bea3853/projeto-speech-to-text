import streamlit as st
from typing import Optional

def render_audio_recorder(key_suffix: str) -> Optional[bytes]:
    """
    Renderiza um gravador de áudio nativo utilizando st.audio_input.
    """
    st.markdown("🎙️ **Grave uma observação por voz:**")
    audio_file = st.audio_input("Clique para gravar o áudio", key=f"audio_input_{key_suffix}")
    
    if audio_file is not None:
        return audio_file.read()
    return None