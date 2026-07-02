import streamlit as st
import datetime
from database.connection import init_db
from controllers.app_controller import AppController
from components.camera import render_camera_component
from components.audio import render_audio_recorder
from components.dashboard import render_dashboard_metrics
from components.history_view import render_history_section
from utils.exporters import convert_to_csv, convert_to_json

# Configuração de Layout unificada
st.set_page_config(page_title="VisionAI Platform", layout="wide", initial_sidebar_state="expanded")

# Inicialização automática das tabelas relacionais do banco Neon.tech
init_db()

# Instanciação estática do orquestrador
controller = AppController()

st.title("🖥️ Plataforma Avançada de Visão Computacional & Áudio")

# 📊 MENU LATERAL / SIDEBAR
with st.sidebar:
    st.header("⚙️ Painel de Operações")
    st.success("Conexão Neon.tech: Ativa ✅")
    
    st.subheader("🔍 Filtros de Consulta do Histórico")
    search_term = st.text_input("Buscar palavra-chave:")
    
    start_d = st.date_input("Data inicial:", datetime.date.today() - datetime.timedelta(days=7))
    end_d = st.date_input("Data final:", datetime.date.today())

    st.subheader("📦 Exportações de Dados")
    records_to_export = controller.fetch_records(search_term, start_d, end_d)
    
    if records_to_export:
        csv_bytes = convert_to_csv(records_to_export)
        st.download_button("📥 Exportar para CSV", data=csv_bytes, file_name="export_analytics.csv", mime="text/csv")
        
        json_bytes = convert_to_json(records_to_export)
        st.download_button("📥 Exportar para JSON", data=json_bytes, file_name="export_analytics.json", mime="application/json")
    else:
        st.caption("Nenhum dado disponível para exportação no momento.")

# 🏛️ DISPOSIÇÃO DO LAYOUT PRINCIPAL (2 COLUNAS)
col_left, col_right = st.columns([1, 1])

with col_left:
    st.header("📸 Captura em Tempo Real")
    captured_image = render_camera_component()
    
    # Incorporação do fluxo de gravação de voz na captura ativa
    captured_audio = render_audio_recorder("main_screen")

    if captured_image:
        if st.button("🚀 Processar e Persistir Dados automaticamente"):
            with st.spinner("Executando pipeline de visão computacional e transcrição de áudio..."):
                saved_record = controller.handle_capture_and_analysis(
                    image_bytes=captured_image, 
                    audio_bytes=captured_audio
                )
                if saved_record:
                    st.success(f"Análise persistida com sucesso! Registro gerado ID: {saved_record.id}")
                    if saved_record.transcricao:
                        st.info(f"📝 Transcrição gerada: {saved_record.transcricao}")
                else:
                    st.error("Erro crítico ao processar o pipeline operacional de dados.")

with col_right:
    # Renderização síncrona do painel de controle e analytics
    all_current_records = controller.fetch_records(search_term, start_d, end_d)
    render_dashboard_metrics(all_current_records)

st.divider()

# Exibição do gerenciamento histórico unificado abaixo das colunas principais
render_history_section(all_current_records, controller)