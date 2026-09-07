import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Assessment Tecnológico — TIS Solutions",
    page_icon="🛡️",
    layout="centered"
)

# Estilo personalizado básico
st.markdown("""
    <style>
    .main-title { color: #0A2540; font-weight: 700; text-align: center; }
    .sub-title { color: #4A5568; text-align: center; margin-bottom: 2rem; }
    .card { background-color: #F8FAFC; padding: 1.5rem; border-radius: 8px; border-left: 5px solid #0066CC; }
    </style>
""", unsafe_allow_html=True)

# Encabezado
st.markdown("<h1 class='main-title'>TIS Solutions</h1>", unsafe_allow_html=True)
st.markdown("<h4 class='sub-title'>Diagnóstico Rápido de Protección, Productividad y Continuidad</h4>", unsafe_allow_html=True)

st.write("""
Responde estas breves preguntas sobre la infraestructura de tu empresa para conocer el nivel actual de madurez tecnológica y recibir recomendaciones personalizadas.
""")

st.divider()

# Formulario de Evaluación
with st.form("assessment_form"):
    st.subheader("1. Datos de Contacto")
    col1, col2 = st.columns(2)
    with col1:
        empresa = st.text_input("Nombre de la Empresa *")
        nombre = st.text_input("Nombre del Contacto *")
    with col2:
        email = st.text_input("Correo Electrónico *")
        usuarios = st.selectbox("Número de usuarios/equipos", ["1 - 10", "11 - 50", "51 - 250", "Más de 250"])

    st.divider()
    st.subheader("2. Colaboración y Productividad (Microsoft)")
    q1 = st.radio(
        "¿Cómo gestiona su equipo el correo y los archivos corporativos?",
        [
            "Usamos correo gratuito o servidores locales sin administración centralizada (0 pts)",
            "Usamos Microsoft 365 / Google Workspace pero solo para correo básico (1 pt)",
            "Usamos Microsoft 365 con almacenamiento en la nube y trabajo colaborativo completo (2 pts)"
        ]
    )

    st.divider()
    st.subheader("3. Seguridad y Protección de Equipos (Kaspersky)")
    q2 = st.radio(
        "¿Qué nivel de protección antimalware/antivirus tienen los dispositivos de la empresa?",
        [
            "Los usuarios usan el antivirus por defecto o herramientas gratuitas individuales (0 pts)",
            "Tenemos un antivirus pagado pero no se administra de manera centralizada (1 pt)",
            "Contamos con protección Endpoint (ej. Kaspersky) centralizada y monitoreada (2 pts)"
        ]
    )

    st.divider()
    st.subheader("4. Respaldo y Continuidad del Negocio (Acronis)")
    q3 = st.radio(
        "En caso de ransomware o falla crítica de servidor/PC, ¿cómo respaldan la información?",
        [
            "No tenemos respaldos automáticos o dependemos de copias manuales en discos externos (0 pts)",
            "Hacemos respaldos locales pero no tenemos respaldo en la nube ni pruebas de restauración (1 pt)",
            "Tenemos respaldos automatizados (locales/nube) con solución tipo Acronis y plan de recuperación (2 pts)"
        ]
    )

    # Botón de envío
    submitted = st.form_submit_button("Generar Diagnóstico")

# Procesamiento de resultados
if submitted:
    if not empresa or not email or not nombre:
        st.error("Por favor completa los campos obligatorios de contacto (*).")
    else:
        # Puntuación
        score_m365 = 0 if "0 pts" in q1 else (1 if "1 pt" in q1 else 2)
        score_kas = 0 if "0 pts" in q2 else (1 if "1 pt" in q2 else 2)
        score_acronis = 0 if "0 pts" in q3 else (1 if "1 pt" in q3 else 2)
        
        total_score = score_m365 + score_kas + score_acronis

        st.success("¡Diagnóstico generado con éxito!")
        st.subheader(f"Resultado para {empresa}")
        
        # Métrica global
        st.metric(label="Puntuación Total de Madurez Tecnológica", value=f"{total_score} / 6 pts")

        # Diagnóstico y Recomendación
        st.divider()
        if total_score <= 2:
            nivel = "Riesgo Alto 🔴"
            paquete = "Paquete 1: Productividad Esencial o Paquete 2: Protección Empresarial"
            mensaje = "Su empresa presenta brechas críticas en seguridad y continuidad. Una falla de equipo o incidente de malware podría detener la operación."
        elif total_score <= 4:
            nivel = "Madurez Intermedia 🟡"
            paquete = "Paquete 2: Protección Empresarial"
            mensaje = "Cuenta con herramientas básicas, pero existen vulnerabilidades en la centralización de seguridad o en el plan de respaldo ante desastres."
        else:
            nivel = "Protección Avanzada 🟢"
            paquete = "Paquete 3: Continuidad 360°"
            mensaje = "Su infraestructura cuenta con buenas bases. Le recomendamos auditar periódicamente sus respaldos y mantener soporte administrado."

        # Mostrar resultado en caja destacada
        st.markdown(f"""
        <div class="card">
            <h3>Nivel de Evaluación: {nivel}</h3>
            <p><b>Diagnóstico:</b> {mensaje}</p>
            <hr>
            <h4>Paquete Sugerido para {empresa}:</h4>
            <p style="font-size:1.2rem; color:#0066CC; font-weight:bold;">{paquete}</p>
        </div>
        """, unsafe_allow_html=True)

        st.info("Un especialista comercial de **TIS Solutions** se pondrá en contacto al correo proporcionado para agendar la evaluación técnica sin costo de 30 minutos.")
