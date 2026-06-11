import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- CONFIGURATION & THEME ---
API_BASE_URL = "http://localhost:8080"
st.set_page_config(layout="wide", page_title="Museo Analytics | Pro Edition", page_icon="🏛️")

# Custom CSS for a professional "Dark Cyber" aesthetic
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=JetBrains+Mono&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .stApp {
        background-color: #050505;
        color: #f3f4f6;
    }
    .main-header {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        background: linear-gradient(90deg, #f97316 0%, #fbbf24 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        color: #9ca3af;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    div.stMetric {
        background: rgba(31, 41, 55, 0.4);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(249, 115, 22, 0.2);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    div[data-testid="stExpander"] {
        background: rgba(31, 41, 55, 0.2);
        border: 1px solid rgba(249, 115, 22, 0.1);
        border-radius: 8px;
    }
    .timeline-card {
        padding: 1rem;
        border-left: 3px solid #f97316;
        background: rgba(31, 41, 55, 0.3);
        margin-bottom: 1rem;
        border-radius: 0 8px 8px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3659/3659815.png", width=80)
    st.title("Centro de Control")
    st.markdown("---")
    st.markdown("### Estado del Sistema")
    st.success("🟢 Operacional")
    st.markdown("---")
    st.info("Sistema de Auditoría v2.0\n\nMuseo de Arte Moderno")

# --- DATA FETCHING HELPERS ---
@st.cache_data(ttl=60)
def fetch_financial_data(anio, mes):
    fact_res = requests.get(f"{API_BASE_URL}/reportes/facturacion", params={"anio": anio, "mes": mes})
    memb_res = requests.get(f"{API_BASE_URL}/reportes/membresias", params={"anio": anio, "mes": mes})
    return (fact_res.json() if fact_res.status_code == 200 else []), \
           (memb_res.json() if memb_res.status_code == 200 else [])

# --- HEADER SECTION ---
st.markdown('<h1 class="main-header">MUSEO ANALYTICS</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Plataforma de Inteligencia y Auditoría de Activos Artísticos</p>', unsafe_allow_html=True)

# --- MAIN TABS ---
tab_fin, tab_obras, tab_seg, tab_audit = st.tabs([
    "📈 FINANZAS", 
    "🎨 TRAZABILIDAD", 
    "🛡️ SEGURIDAD", 
    "🔍 AUDITORÍA"
])

# --- TAB 1: FINANZAS ---
with tab_fin:
    # Move filters here
    st.subheader("Parámetros de Análisis Fiscal")
    f_col1, f_col2 = st.columns(2)
    with f_col1:
        anio_fiscal = st.selectbox("Año Fiscal", [2026, 2025], index=0)
    with f_col2:
        mes_fiscal = st.select_slider("Mes de Análisis", options=list(range(1, 13)), value=6)
    
    st.markdown("---")

    # Fetch data inside tab
    fact_data, memb_data = fetch_financial_data(anio_fiscal, mes_fiscal)
    df_fact = pd.DataFrame(fact_data)
    df_memb = pd.DataFrame(memb_data)

    # Tab-specific KPIs
    kpi1, kpi2, kpi3 = st.columns(3)

    if not df_fact.empty:
        df_fact['ganancia_museo'] = pd.to_numeric(df_fact['ganancia_museo'])
        df_fact['monto_neto'] = pd.to_numeric(df_fact['monto_neto'])
        total_rev = df_fact['monto_neto'].sum()
        net_profit = df_fact['ganancia_museo'].sum()
    else:
        total_rev = net_profit = 0

    if not df_memb.empty:
        df_memb['monto_cobrado'] = pd.to_numeric(df_memb['monto_cobrado'])
        total_memb = df_memb['monto_cobrado'].sum()
    else:
        total_memb = 0

    kpi1.metric("Ingresos Totales", f"${total_rev:,.2f}")
    kpi2.metric("Ganancia Neta", f"${net_profit:,.2f}")
    kpi3.metric("Recaudación Membresías", f"${total_memb:,.2f}")

    st.markdown("<br>", unsafe_allow_html=True)

    if df_fact.empty and df_memb.empty:
        st.warning("No hay datos financieros para este periodo.")
    else:
        c1, c2 = st.columns([1, 1])
        
        with c1:
            st.subheader("Estado de Facturación")
            if not df_fact.empty:
                fig_status = px.pie(df_fact, names='estado', hole=0.6, 
                                  color_discrete_sequence=px.colors.sequential.Oranges_r)
                fig_status.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                       font_color='white', showlegend=True, margin=dict(t=0, b=0, l=0, r=0))
                st.plotly_chart(fig_status, use_container_width=True)
        
        with c2:
            st.subheader("Tendencia de Ingresos")
            if not df_fact.empty:
                df_fact['fecha_emision'] = pd.to_datetime(df_fact['fecha_emision'])
                daily_rev = df_fact.groupby(df_fact['fecha_emision'].dt.date)['monto_neto'].sum().reset_index()
                fig_rev = px.area(daily_rev, x='fecha_emision', y='monto_neto', 
                                 line_shape='spline', color_discrete_sequence=['#f97316'])
                fig_rev.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                    font_color='white', xaxis_title=None, yaxis_title="Monto ($)",
                                    margin=dict(t=20, b=20, l=0, r=0))
                st.plotly_chart(fig_rev, use_container_width=True)
        
        st.subheader("Detalle de Transacciones (Facturación)")
        st.dataframe(df_fact, use_container_width=True)

        st.subheader("Detalle de Membresías")
        if not df_memb.empty:
            st.dataframe(df_memb, use_container_width=True)
        else:
            st.info("No hay registros de membresías para este periodo.")

# --- TAB 2: TRAZABILIDAD ---
with tab_obras:
    st.subheader("Historial de Estatus de Obra")
    id_obra = st.number_input("Ingrese ID de la Obra", min_value=1, value=28, step=1)
    
    if st.button("Rastrear Activo"):
        with st.spinner("Consultando registros históricos..."):
            res = requests.get(f"{API_BASE_URL}/obras/historico/{id_obra}")
            if res.status_code == 200:
                obras_data = res.json()
                if not obras_data:
                    st.info("No se encontró historial para esta obra.")
                else:
                    for item in obras_data:
                        fecha_raw = item['fecha_evento'].replace('Z', '')
                        fecha = datetime.fromisoformat(fecha_raw).strftime("%d %b %Y, %H:%M")
                        st.markdown(f"""
                            <div class="timeline-card">
                                <strong>{fecha}</strong><br>
                                <span style="color: #f97316;">{item['estatus_anterior']}</span> ➔ 
                                <span style="color: #fbbf24;">{item['estatus_nuevo']}</span><br>
                                <small>Usuario: {item['usuario_id']} | IP: {item['ip_origen']}</small>
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.error("Error al consultar el repositorio de obras.")

# --- TAB 3: SEGURIDAD ---
with tab_seg:
    st.subheader("Monitor de Eventos de Seguridad")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        user_log = st.text_input("Usuario a auditar", value="frantest")
    with col_s2:
        date_range = st.date_input("Rango de fechas", [datetime(2025, 1, 1), datetime.now() + timedelta(days=1)])
    
    if st.button("Generar Reporte de Seguridad"):
        params = {
            "login_usuario": user_log,
            "desde": date_range[0].isoformat(),
            "hasta": date_range[1].isoformat()
        }
        res_seg = requests.get(f"{API_BASE_URL}/seguridad/logs", params=params)
        if res_seg.status_code == 200:
            df_seg = pd.DataFrame(res_seg.json())
            if df_seg.empty:
                st.info("Sin eventos detectados para este usuario en el rango seleccionado.")
            else:
                s_c1, s_c2 = st.columns([1, 1])
                with s_c1:
                    fig_seg = px.histogram(df_seg, x='evento_tipo', color='evento_tipo',
                                         color_discrete_sequence=px.colors.qualitative.Bold)
                    fig_seg.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
                    st.plotly_chart(fig_seg, use_container_width=True)
                with s_c2:
                    st.metric("Alertas Críticas", len(df_seg[df_seg['evento_tipo'].str.contains("FALLIDO")]))
                    st.dataframe(df_seg[['fecha_evento', 'evento_tipo', 'ip_origen']], use_container_width=True)
        else:
            st.error("Error en el servicio de seguridad.")

# --- TAB 4: AUDITORÍA ---
with tab_audit:
    st.subheader("Auditoría de Códigos de Membresía")
    id_comp = st.number_input("ID del Comprador", min_value=1, value=26, step=1)
    
    if st.button("Consultar Auditoría"):
        res_audit = requests.get(f"{API_BASE_URL}/membresias/codigos", params={"id_comprador": id_comp})
        if res_audit.status_code == 200:
            audit_data = res_audit.json().get('datos', [])
            if not audit_data:
                st.info("No se encontraron códigos emitidos para este comprador.")
            else:
                df_audit = pd.DataFrame(audit_data)
                
                # Visual summary instead of a redundant bar chart
                a1, a2 = st.columns(2)
                total_codes = len(df_audit)
                
                with a1:
                    st.metric("Total Códigos Emitidos", total_codes)
                with a2:
                    st.info("Todos los códigos se encuentran en estado **EMITIDO**")
                
                st.markdown("---")
                st.dataframe(df_audit[['fecha_registro', 'codigo_seguridad', 'correo_envio', 'estado']], use_container_width=True)
        else:
            st.error("Error al consultar el servicio de auditoría.")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #4b5563;'>© 2026 Museo Auditoria System | Confidential & Restricted Access</p>", unsafe_allow_html=True)
