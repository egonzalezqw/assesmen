import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Assessment Tecnológico — TIS Solutions",
    page_icon="🛡️",
    layout="centered"
)

# Estilo personalizado
st.markdown("""
    <style>
    .main-title { color: #0A2540; font-weight: 700; text-align: center; }
    .sub-title { color: #4A5568; text-align: center; margin-bottom: 2rem; }
    .card { background-color: #F8FAFC; padding: 1.5rem; border-radius: 8px; border-left: 5px solid #0066CC; }
    .score-badge { font-size: 1.5rem; font-weight: bold; color: #0066CC; }
    </style>
""", unsafe_allow_html=True)

# Encabezado
st.markdown("<h1 class='main-title'>TIS Solutions</h1>", unsafe_allow_html=True)
st.markdown("<h4 class='sub-title'>Diagnóstico de Productividad, Seguridad y Continuidad Operativa</h4>", unsafe_allow_html=True)

st.write("""
Evalúa el nivel de riesgo y madurez tecnológica de tu empresa completando este test de **10 preguntas**. 
Obtendrás un diagnóstico automático y recomendaciones sobre tu infraestructura.
""")

st.divider()

# Formulario de Evaluación
with st.form("assessment_form"):
    st.subheader("📋 1. Datos de la Empresa")
    col1, col2 = st.columns(2)
    with col1:
        empresa = st.text_input("Nombre de la Empresa *")
        nombre = st.text_input("Nombre del Contacto *")
    with col2:
        email = st.text_input("Correo Electrónico *")
        usuarios = st.selectbox("Número de usuarios/equipos", ["1 - 10", "11 - 50", "51 - 250", "Más de 250"])

    st.divider()
    st.subheader("💻 2. Productividad y Colaboración (Microsoft)")
    
    q1 = st.radio(
        "1. ¿Cómo gestionan el correo electrónico empresarial?",
        [
            "Correo gratuito/webmail sin dominio propio o sin administración central (0 pts)",
            "Servidor propio antiguo o proveedor básico de hosting (1 pt)",
            "Microsoft 365 con dominio corporativo y administración de usuarios (2 pts)"
        ]
    )

    q2 = st.radio(
        "2. ¿Cómo almacenan y comparten archivos de trabajo diario?",
        [
            "Guardados localmente en cada computadora o en carpetas compartidas sin respaldo (0 pts)",
            "Servidor de archivos físico local sin acceso remoto seguro (1 pt)",
            "OneDrive / SharePoint en la nube con permisos por usuario y acceso desde cualquier lugar (2 pts)"
        ]
    )

    q3 = st.radio(
        "3. ¿Qué herramientas utilizan para videollamadas y trabajo en equipo?",
        [
            "Aplicaciones informales/personales sin control de la empresa (0 pts)",
            "Herramientas variadas no integradas entre sí (1 pt)",
            "Microsoft Teams integrado con el calendario y documentos corporativos (2 pts)"
        ]
    )

    st.divider()
    st.subheader("🛡️ 3. Ciberseguridad y Protección de Dispositivos")

    q4 = st.radio(
        "4. ¿Cómo protegen las computadoras y servidores contra malware o ciberataques?",
        [
            "Cada usuario usa antivirus gratuito o el que viene por defecto en Windows (0 pts)",
            "Antivirus tradicional pagado, pero administrado de forma individual en cada PC (1 pt)",
            "Protección Endpoint avanzada (EDR/XDR) administrada de forma centralizada (2 pts)"
        ]
    )

    q5 = st.radio(
        "5. ¿Tienen medidas contra correos de Phishing o suplantación de identidad?",
        [
            "No contamos con filtros de correo avanzados ni protección anti-phishing (0 pts)",
            "Filtro básico de spam del proveedor de correo (1 pt)",
            "Protección avanzada de correo con filtrado de enlaces y adjuntos maliciosos (2 pts)"
        ]
    )

    q6 = st.radio(
        "6. ¿Cómo gestionan las contraseñas y accesos de los empleados?",
        [
            "Sin políticas de contraseñas; se comparten accesos abiertamente (0 pts)",
            "Contraseñas requeridas pero sin autenticación de dos factores (MFA) (1 pt)",
            "Autenticación de Dos Factores (MFA) obligatoria en todos los accesos corporativos (2 pts)"
        ]
    )

    st.divider()
    st.subheader("🔄 4. Respaldo y Continuidad del Negocio (Acronis)")

    q7 = st.radio(
        "7. ¿Con qué frecuencia se realizan respaldos de la información crítica?",
        [
            "No realizamos respaldos o los hacemos manualmente de forma esporádica (0 pts)",
            "Respaldos semanales/diarios guardados solo en discos duros locales (1 pt)",
            "Respaldos automatizados diarios en la nube con solución tipo Acronis (2 pts)"
        ]
    )

    q8 = st.radio(
        "8. En caso de un ataque de Ransomware (secuestro de datos), ¿cuál es su nivel de respuesta?",
        [
            "Perderíamos la información o tendría que detenerse la operación por varios días (0 pts)",
            "Podríamos recuperar algo de información, pero llevaría mucho tiempo reconfigurar todo (1 pt)",
            "Contamos con protección activa contra Ransomware y restauración rápida de imágenes completas (2 pts)"
        ]
    )

    q9 = st.radio(
        "9. ¿Realizan pruebas periódicas de restauración de datos?",
        [
            "Nunca hemos probado recuperar un respaldo completo (0 pts)",
            "Probamos recuperar archivos individuales únicamente cuando ocurre un problema (1 pt)",
            "Ejecutamos pruebas periódicas planificadas de recuperación de desastres (2 pts)"
        ]
    )

    q10 = st.radio(
        "10. ¿Tienen respaldadas las cuentas de Microsoft 365 (correo, OneDrive, SharePoint)?",
        [
            "No, asumimos que Microsoft respalda todo automáticamente (0 pts)",
            "Respaldamos manualmente algunos archivos críticos (1 pt)",
            "Contamos con respaldo dedicado Cloud-to-Cloud (ej. Acronis para M365) (2 pts)"
        ]
    )

    # Botón de envío
    submitted = st.form_submit_button("Ver Diagnóstico y Recomendación")

# Procesamiento de resultados
if submitted:
    if not empresa or not email or not nombre:
        st.error("Por favor completa los campos obligatorios (*).")
    else:
        # Cálculo de puntajes por sección
        respuestas = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]
        
        total_score = 0
        for r in respuestas:
            if "2 pts" in r:
                total_score += 2
            elif "1 pt" in r:
                total_score += 1

        st.success("¡Diagnóstico completado con éxito!")
        st.subheader(f"Resultado de Evaluación para {empresa}")
        
        # Métrica global (Máximo 20 puntos)
        st.metric(label="Puntuación de Madurez Tecnológica", value=f"{total_score} / 20 pts")

        # Nivel y recomendación
        st.divider()
        if total_score <= 7:
            nivel = "Riesgo Alto 🔴"
            paquete = "Paquete 1: Productividad Esencial"
            mensaje = "Su empresa presenta vulnerabilidades críticas en respaldo y seguridad. Una falla de disco o infección de ransomware podría pausar las operaciones por tiempo indefinido."
        elif total_score <= 14:
            nivel = "Madurez Intermedia 🟡"
            paquete = "Paquete 2: Protección Empresarial"
            mensaje = "Cuenta con bases operativas, pero existen brechas importantes en la automatización de respaldos en la nube, protección contra ransomware y autenticación segura."
        else:
            nivel = "Protección Avanzada 🟢"
            paquete = "Paquete 3: Continuidad 360°"
            mensaje = "Su empresa cuenta con una postura sólida. Le recomendamos auditorías periódicas y mantener monitoreo administrado para prevenir nuevas amenazas."

        # Muestra del resultado
        st.markdown(f"""
        <div class="card">
            <h3>Estado Actual: {nivel}</h3>
            <p><b>Diagnóstico General:</b> {mensaje}</p>
            <hr>
            <h4>Paquete Sugerido para {empresa}:</h4>
            <p class="score-badge">{paquete}</p>
        </div>
        """, unsafe_allow_html=True)

        st.info("Un especialista de **TIS Solutions** revisará sus respuestas y le enviará el informe detallado al correo proporcionado.")
