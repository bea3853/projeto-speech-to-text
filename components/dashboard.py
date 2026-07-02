import streamlit as st
import pandas as pd
from typing import List, Any

def render_dashboard_metrics(records: List[Any]) -> None:
    """Processa dados históricos agregados exibindo estatísticas executivas e gráficas na tela."""
    st.subheader("📊 Painel Analítico Geral")
    
    if not records:
        st.info("Dados insuficientes para consolidação de métricas gráficas.")
        return

    total_analises = len(records)
    total_rostos = sum([r.rostos for r in records if r.rostos])
    
    # Renderização de Cards informativos de alto impacto
    col1, col2, col3 = st.columns(3)
    col1.metric("Análises Executadas", total_analises)
    col2.metric("Total Rostos Identificados", total_rostos)
    
    nitidos = sum([1 for r in records if r.nitidez and "Alta" in r.nitidez])
    pct_nitidez = (nitidos / total_analises) * 100 if total_analises > 0 else 0
    col3.metric("Aproveitamento Nitidez", f"{pct_nitidez:.1f}%")

    # Geração de dataframe temporal para visualização gráfica inline
    chart_data = []
    for r in records:
        chart_data.append({
            "Data": r.created_at.date(),
            "Rostos Detectados": r.rostos if r.rostos else 0
        })
    
    df = pd.DataFrame(chart_data).groupby("Data").sum().reset_index()
    st.markdown("**Evolução Temporal de Detecções de Rostos:**")
    st.line_chart(data=df, x="Data", y="Rostos Detectados")