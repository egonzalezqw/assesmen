import streamlit as st
from fpdf import FPDF

# Configuración de la página
st.set_page_config(
    page_title="Assessment Tecnológico — TIS Solutions",
    page_icon="🛡️",
    layout="centered"
)

# Estilo personalizado en CSS
st.markdown("""
    <style>
    .main-title { color: #0A2540; font-weight: 700; text-align: center; }
    .sub-title { color: #4A5568; text-align: center; margin-bottom: 2rem; }
    .card { background-color: #F8FAFC; padding: 1.5rem; border-radius: 8px; border-left: 5px solid #0066CC; margin-top: 1rem; }
    .score-badge { font-size: 1.4rem; font-weight: bold; color: #0066CC; }
    </style>
""", unsafe_allow_html=True)

# Función para sanitizar textos y evitar errores de codificación Unicode en FPDF
def clean_text(text):
    if not isinstance(text, str):
        return str(text)
    replacements = {
        '—': '-',
        '–': '-',
        '“': '"',
        '”': '"',
        '’': "'",
        '•': '*',
        '🔴': '[Riesgo Alto]',
        '🟡': '[Madurez Intermedia]',
        '🟢': '[Protección Avanzada]',
        '📋': '',
        '💻': '',
        '🛡️': '',
        '🔄': '',
        '📄': ''
    }
    for orig, repl in replacements.items():
        text = text.replace(orig, repl)
    # Convertir caracteres especiales a latin-1 seguro
    return text.encode('latin-1', 'replace').decode('latin-1')


# Clase para generar el PDF del Informe Ejecutivo
class PDFReport(FPDF):
    def header(self):
        self.set_fill_color(10, 37, 64) # Azul oscuro corporativo
        self.rect(0, 0, 210, 25, 'F')
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, clean_text('TIS SOLUTIONS - INFORME EJECUTIVO DE DIAGNOSTICO'), border=0, ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, clean_text(f'Página {self.page_no()} - TIS Solutions | www.tis-solutions.com'), align='C')


def generar_pdf(empresa, contacto, email, usuarios, total_score, nivel, paquete, mensaje, respuestas_detalle):
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Datos de la Empresa
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(10, 37, 64)
    pdf.cell(0, 8, clean_text('1. Información de la Empresa Evaluada'), ln=True)
    
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(100, 6, clean_text(f'Empresa: {empresa}'), ln=False)
    pdf.cell(90, 6, clean_text(f'Contacto: {contacto}'), ln=True)
    pdf.cell(100, 6, clean_text(f'Correo: {email}'), ln=False)
    pdf.cell(90, 6, clean_text(f'N° de Usuarios/Equipos: {usuarios}'), ln=True)
    pdf.ln(5)

    # Resumen del Diagnóstico
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(10, 37, 64)
    pdf.cell(0, 8, clean_text('2. Resumen Ejecutivo del Diagnóstico'), ln=True)
    
    pdf.set_fill_color(240, 244, 248)
    pdf.rect(10, pdf.get_y(), 190, 32, 'F')
    pdf.set_y(pdf.get_y() + 3)
    
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 6, clean_text(f' Puntuación de Madurez: {total_score} / 20 pts - Nivel: {nivel}'), ln=True)
    
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 6, clean_text(f' Paquete Comercial Sugerido: {paquete}'), ln=True)
    
    pdf.set_font('Helvetica', '', 9)
    pdf.multi_cell(180, 5, clean_text(f' Observaciones: {mensaje}'))
    pdf.ln(8)

    # Detalle por Pilar Tecnológico
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(10, 37, 64)
    pdf.cell(0, 8, clean_text('3. Detalle de Evaluación por Pilar Tecnológico'), ln=True)
    pdf.ln(2)

    for pilar, preguntas in respuestas_detalle.items():
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_fill_color(225, 235, 245)
        pdf.cell(0, 6, clean_text(f' {pilar}'), ln=True, fill=True)
        pdf.ln(2)
        
        pdf.set_font('Helvetica', '', 8.5)
        pdf.set_text_color(40, 40, 40)
        for p, r in preguntas:
            pdf.multi_cell(190, 4, clean_text(f'* {p}\n  Respuesta: {r}'))
            pdf.ln(1)
        pdf.ln(3)

    # Recomendación Final
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(10, 37, 64)
    pdf.cell(0, 8, clean_text('4. Próximos Pasos Recomendados por TIS Solutions'), ln=True)
    pdf.set_font('Helvetica', '', 9.5)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(190, 5, clean_text("Para profundizar en este diagnóstico y cerrar las brechas identificadas, TIS Solutions ofrece una evaluación técnica sin costo de 30 minutos donde nuestros ingenieros revisarán sus licencias, políticas de seguridad y esquema de respaldos."))

    return bytes(pdf.output())


# Encabezado Principal en Streamlit
st.markdown("<h1 class='main-title'>TIS Solutions</h1>", unsafe_allow_html=True)
st.markdown("<h4 class='sub-title'>Diagnóstico de Productividad, Seguridad y Continuidad Operativa</h4>", unsafe_allow_html=True)

st.write("""
Evalúa el nivel de riesgo y madurez tecnológica de tu empresa completando este test de **10 preguntas**. 
Obtendrás un diagnóstico automático en pantalla y podrás **descargar tu Informe Ejecutivo en PDF**.
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
    
    q1_txt = "1. ¿Cómo gestionan el correo electrónico empresarial?"
    q1 = st.radio(q1_txt, [
        "Correo gratuito/webmail sin dominio propio o sin administración central (0 pts)",
        "Servidor propio antiguo o proveedor básico de hosting (1 pt)",
        "Microsoft 365 con dominio corporativo y administración de usuarios (2 pts)"
    ])

    q2_txt = "2. ¿Cómo almacenan y comparten archivos de trabajo diario?"
    q2 = st.radio(q2_txt, [
        "Guardados localmente en cada computadora o en carpetas compartidas sin respaldo (0 pts)",
        "Servidor de archivos físico local sin acceso remoto seguro (1 pt)",
        "OneDrive / SharePoint en la nube con permisos por usuario y acceso desde cualquier lugar (2 pts)"
    ])

    q3_txt = "3. ¿Qué herramientas utilizan para videollamadas y trabajo en equipo?"
    q3 = st.radio(q3_txt, [
        "Aplicaciones informales/personales sin control de la empresa (0 pts)",
        "Herramientas variadas no integradas entre sí (1 pt)",
        "Microsoft Teams integrado con el calendario y documentos corporativos (2 pts)"
    ])

    st.divider()
    st.subheader("🛡️ 3. Ciberseguridad y Protección de Dispositivos (Acronis)")

    q4_txt = "4. ¿Cómo protegen las computadoras y servidores contra malware o ciberataques?"
    q4 = st.radio(q4_txt, [
        "Cada usuario usa antivirus gratuito o el que viene por defecto en Windows (0 pts)",
        "Antivirus tradicional pagado, pero administrado de forma individual en cada PC (1 pt)",
        "Protección Endpoint avanzada (EDR/Cyber Protect con Acronis) administrada de forma centralizada (2 pts)"
    ])

    q5_txt = "5. ¿Tienen medidas contra correos de Phishing o suplantación de identidad?"
    q5 = st.radio(q5_txt, [
        "No contamos con filtros de correo avanzados ni protección anti-phishing (0 pts)",
        "Filtro básico de spam del proveedor de correo (1 pt)",
        "Protección avanzada de correo con filtrado de enlaces y adjuntos maliciosos (2 pts)"
    ])

    q6_txt = "6. ¿Cómo gestionan las contraseñas y accesos de los empleados?"
    q6 = st.radio(q6_txt, [
        "Sin políticas de contraseñas; se comparten accesos abiertamente (0 pts)",
        "Contraseñas requeridas pero sin autenticación de dos factores (MFA) (1 pt)",
        "Autenticación de Dos Factores (MFA) obligatoria en todos los accesos corporativos (2 pts)"
    ])

    st.divider()
    st.subheader("🔄 4. Respaldo y Continuidad del Negocio (Acronis)")

    q7_txt = "7. ¿Con qué frecuencia se realizan respaldos de la información crítica?"
    q7 = st.radio(q7_txt, [
        "No realizamos respaldos o los hacemos manualmente de forma esporádica (0 pts)",
        "Respaldos semanales/diarios guardados solo en discos duros locales (1 pt)",
        "Respaldos automatizados diarios en la nube con solución tipo Acronis (2 pts)"
    ])

    q8_txt = "8. En caso de un ataque de Ransomware (secuestro de datos), ¿cuál es su nivel de respuesta?"
    q8 = st.radio(q8_txt, [
        "Perderíamos la información o tendría que detenerse la operación por varios días (0 pts)",
        "Podríamos recuperar algo de información, pero llevaría mucho tiempo reconfigurar todo (1 pt)",
        "Contamos con protección activa contra Ransomware y restauración rápida de imágenes completas (2 pts)"
    ])

    q9_txt = "9. ¿Realizan pruebas periódicas de restauración de datos?"
    q9 = st.radio(q9_txt, [
        "Nunca hemos probado recuperar un respaldo completo (0 pts)",
        "Probamos recuperar archivos individuales únicamente cuando ocurre un problema (1 pt)",
        "Ejecutamos pruebas periódicas planificadas de recuperación de desastres (2 pts)"
    ])

    q10_txt = "10. ¿Tienen respaldadas las cuentas de Microsoft 365 (correo, OneDrive, SharePoint)?"
    q10 = st.radio(q10_txt, [
        "No, asumimos que Microsoft respalda todo automáticamente (0 pts)",
        "Respaldamos manualmente algunos archivos críticos (1 pt)",
        "Contamos con respaldo dedicado Cloud-to-Cloud (ej. Acronis para M365) (2 pts)"
    ])

    submitted = st.form_submit_button("Generar Diagnóstico")

# Procesar resultados y habilitar descarga
if submitted:
    if not empresa or not email or not nombre:
        st.error("Por favor completa todos los campos marcados con asterisco (*).")
    else:
        respuestas = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]
        
        # Conteo de puntos
        total_score = sum(2 if "2 pts" in r else (1 if "1 pt" in r else 0) for r in respuestas)

        # Lógica de diagnóstico
        if total_score <= 7:
            nivel = "Riesgo Alto"
            paquete = "Paquete 1: Productividad Esencial"
            mensaje = "Su empresa presenta vulnerabilidades críticas en respaldo y seguridad. Una falla de disco o infección de ransomware podría pausar las operaciones por tiempo indefinido."
        elif total_score <= 14:
            nivel = "Madurez Intermedia"
            paquete = "Paquete 2: Protección Empresarial"
            mensaje = "Cuenta con bases operativas, pero existen brechas importantes en la automatización de respaldos en la nube, protección contra ransomware y autenticación segura."
        else:
            nivel = "Protección Avanzada"
            paquete = "Paquete 3: Continuidad 360°"
            mensaje = "Su empresa cuenta con una postura sólida. Le recomendamos auditorías periódicas y mantener monitoreo administrado para prevenir nuevas amenazas."

        st.success("¡Diagnóstico completado con éxito!")
        st.subheader(f"Resultado de Evaluación para {empresa}")
        st.metric(label="Puntuación de Madurez Tecnológica", value=f"{total_score} / 20 pts")

        # Tarjeta resumen en pantalla
        st.markdown(f"""
        <div class="card">
            <h3>Estado Actual: {nivel}</h3>
            <p><b>Diagnóstico General:</b> {mensaje}</p>
            <hr>
            <h4>Paquete Sugerido:</h4>
            <p class="score-badge">{paquete}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()

        # Agrupar preguntas para el reporte PDF
        respuestas_detalle = {
            "Productividad y Colaboración (Microsoft)": [(q1_txt, q1), (q2_txt, q2), (q3_txt, q3)],
            "Ciberseguridad y Accesos (Acronis)": [(q4_txt, q4), (q5_txt, q5), (q6_txt, q6)],
            "Respaldo y Continuidad (Acronis)": [(q7_txt, q7), (q8_txt, q8), (q9_txt, q9), (q10_txt, q10)]
        }

        # Generar el archivo PDF en memoria
        pdf_bytes = generar_pdf(empresa, nombre, email, usuarios, total_score, nivel, paquete, mensaje, respuestas_detalle)

        # Botón de Descarga del PDF
        st.subheader("📥 Descargar Informe Ejecutivo")
        st.write("Obtén el reporte completo en formato PDF con el desglose de preguntas, nivel de riesgo y las recomendaciones de TIS Solutions.")
        
        st.download_button(
            label="📄 Descargar Informe Ejecutivo (PDF)",
            data=pdf_bytes,
            file_name=f"Informe_Ejecutivo_TIS_{empresa.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
