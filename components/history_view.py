import streamlit as st
import os
from PIL import Image
from typing import List, Any
from controllers.app_controller import AppController
from components.audio import render_audio_recorder

def render_history_section(records: List[Any], controller: AppController) -> None:
    """Lista o histórico estruturado em cards organizados permitindo mutabilidade de áudio e exclusões."""
    st.subheader("🗄️ Histórico de Capturas e Insights")
    
    if not records:
        st.info("Nenhum registro encontrado para os filtros selecionados.")
        return

    for item in records:
        with st.container():
            c1, c2 = st.columns([1, 2])
            
            with c1:
                if os.path.exists(item.image_path):
                    try:
                        img = Image.open(item.image_path)
                        st.image(img, use_container_width=True)
                        
                        # Botão de download da imagem original
                        with open(item.image_path, "rb") as file:
                            st.download_button(
                                label="💾 Baixar Foto",
                                data=file,
                                file_name=os.path.basename(item.image_path),
                                mime="image/jpeg",
                                key=f"dl_img_{item.id}"
                            )
                    except Exception:
                        st.error("Erro ao carregar miniatura.")
                else:
                    st.warning("Arquivo de mídia físico deletado/indisponível.")

            with c2:
                st.markdown(f"**Registro ID:** `{item.id}` | **Data:** {item.created_at.strftime('%d/%m/%Y %H:%M:%S')}")
                st.markdown(f"**🔍 Objetos:** {item.objetos}")
                st.markdown(f"**👥 Pessoas/Rostos:** {item.quantidade_pessoas}")
                st.markdown(f"**💡 Iluminação:** {item.luminosidade} | **✨ Nitidez:** {item.nitidez}")
                
                if item.transcricao:
                    st.info(f"🎤 **Transcrição por Voz:** {item.transcricao}")
                    if st.button("🗑️ Remover Observação de Áudio", key=f"del_audio_{item.id}"):
                        if controller.clear_audio_transcription(item.id):
                            st.toast("Áudio removido do registro.")
                            st.rerun()
                else:
                    st.caption("Sem notas de áudio vinculadas.")
                    # Expandir área para gravar áudio direto no histórico
                    with st.expander("➕ Adicionar Comentário por Voz"):
                        audio_data = render_audio_recorder(f"hist_{item.id}")
                        if audio_data:
                            if st.button("Confirmar e Processar Áudio", key=f"btn_proc_audio_{item.id}"):
                                with st.spinner("Transcrevendo áudio..."):
                                    controller.update_audio_transcription(item.id, audio_data)
                                st.toast("Transcrição processada com sucesso!")
                                st.rerun()

                if st.button("❌ Excluir Registro Completo", key=f"del_rec_{item.id}"):
                    if controller.remove_record(item.id):
                        st.success(f"Registro {item.id} removido.")
                        st.rerun()
            st.divider()