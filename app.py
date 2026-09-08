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
st.markdown("<h4 class='sub-title'>Diagnóstico de Productividad, Protección y Continuidad Operativa</h4>", unsafe_allow_html=True)

st.write("""
Complete este breve test de **10 preguntas** para conocer la postura tecnológica de su empresa. 
Al finalizar, obtendrá su diagnóstico en pantalla y podrá **descargar el Informe Ejecutivo en PDF**.
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
    st.subheader("💻 2. Trabajo en Equipo y Productividad")
    
    q1_txt = "1. ¿Cómo manejan los correos electrónicos de la empresa?"
    q1_opts = [
        "Usamos cuentas gratuitas o proveedores básicos sin control central",
        "Tenemos un servidor propio o correo corporativo básico",
        "Usamos Microsoft 365 administrado profesionalmente"
    ]
    q1 = st.radio(q1_txt, q1_opts)

    q2_txt = "2. ¿Dónde guardan y comparten los documentos de trabajo?"
    q2_opts = [
        "En la computadora de cada empleado o en carpetas sin copia de seguridad",
        "En un servidor físico dentro de la oficina",
        "En la nube (OneDrive / SharePoint) accesibles de forma segura desde cualquier lugar"
    ]
    q2 = st.radio(q2_txt, q2_opts)

    q3_txt = "3. ¿Qué herramientas usan para comunicarse y hacer reuniones?"
    q3_opts = [
        "Aplicaciones personales e informales (como WhatsApp personal sin control)",
        "Varias herramientas distintas que no están conectadas entre sí",
        "Una plataforma corporativa integrada (como Microsoft Teams)"
    ]
    q3 = st.radio(q3_txt, q3_opts)

    st.divider()
    st.subheader("🛡️ 3. Protección de Equipos y Accesos")

    q4_txt = "4. ¿Cómo protegen las computadoras de la empresa contra virus o ataques?"
    q4_opts = [
        "Cada usuario usa el antivirus gratuito que viene en su equipo",
        "Compramos un antivirus tradicional, pero no lo monitoreamos centralmente",
        "Contamos con una solución de protección profesional administrada por expertos"
    ]
    q4 = st.radio(q4_txt, q4_opts)

    q5_txt = "5. ¿Cómo evitan que el personal abra correos sospechosos o engañosos?"
    q5_opts = [
        "No tenemos ningún filtro de seguridad en el correo",
        "Solo tenemos el filtro de correo no deseado (spam) habitual",
        "Contamos con protección avanzada que analiza enlaces y archivos peligrosos"
    ]
    q5 = st.radio(q5_txt, q5_opts)

    q6_txt = "6. ¿Cómo controlan los accesos y contraseñas de los empleados?"
    q6_opts = [
        "No hay políticas; las claves se comparten libremente",
        "Se exigen claves, pero solo ingresan un nombre de usuario y contraseña",
        "Es obligatorio confirmar el ingreso mediante un código en el celular (doble factor)"
    ]
    q6 = st.radio(q6_txt, q6_opts)

    st.divider()
    st.subheader("🔄 4. Respaldo y Continuidad del Negocio")

    q7_txt = "7. ¿Con qué frecuencia guardan copias de respaldo de su información?"
    q7_opts = [
        "No hacemos respaldos o se hacen de forma manual de vez en cuando",
        "Guardamos copias en discos duros externos o memorias USB dentro de la oficina",
        "Tenemos un sistema que respalda todo automáticamente en la nube todos los días"
    ]
    q7 = st.radio(q7_txt, q7_opts)

    q8_txt = "8. Si un virus bloquea sus computadoras, ¿qué sucedería con su operación?"
    q8_opts = [
        "Perderíamos la información o la empresa se detendría por varios días",
        "Recuperaríamos algo, pero tomaría mucho tiempo y esfuerzo volver a trabajar",
        "Podríamos restaurar todo el sistema rápidamente desde nuestros respaldos"
    ]
    q8 = st.radio(q8_txt, q8_opts)

    q9_txt = "9. ¿Han probado recuperar la información de sus respaldos para comprobar que funcionan?"
    q9_opts = [
        "Nunca hemos probado recuperar una copia de respaldo",
        "Solo intentamos buscar un archivo cuando alguien pierde algo de forma accidental",
        "Hacemos pruebas periódicas para verificar que las copias funcionen correctamente"
    ]
    q9 = st.radio(q9_txt, q9_opts)

    q10_txt = "10. ¿Tienen una copia de respaldo independiente de su correo y archivos en la nube?"
    q10_opts = [
        "No, asumimos que el proveedor de correo respalda todo automáticamente",
        "Guardamos copias manuales de algunos archivos importantes",
        "Tenemos un respaldo automático independiente dedicado a la nube"
    ]
    q10 = st.radio(q10_txt, q10_opts)

    submitted = st.form_submit_button("Generar Diagnóstico")

# Mapeo interno de puntuación por opción seleccionada
scores_map = {
    # Puntuación Q1
    q1_opts[0]: 0, q1_opts[1]: 1, q1_opts[2]: 2,
    # Puntuación Q2
    q2_opts[0]: 0, q2_opts[1]: 1, q2_opts[2]: 2,
    # Puntuación Q3
    q3_opts[0]: 0, q3_opts[1]: 1, q3_opts[2]: 2,
    # Puntuación Q4
    q4_opts[0]: 0, q4_opts[1]: 1, q4_opts[2]: 2,
    # Puntuación Q5
    q5_opts[0]: 0, q5_opts[1]: 1, q5_opts[2]: 2,
    # Puntuación Q6
    q6_opts[0]: 0, q6_opts[1]: 1, q6_opts[2]: 2,
    # Puntuación Q7
    q7_opts[0]: 0, q7_opts[1]: 1, q7_opts[2]: 2,
    # Puntuación Q8
    q8_opts[0]: 0, q8_opts[1]: 1, q8_opts[2]: 2,
    # Puntuación Q9
    q9_opts[0]: 0, q9_opts[1]: 1, q9_opts[2]: 2,
    # Puntuación Q10
    q10_opts[0]: 0, q10_opts[1]: 1, q10_opts[2]: 2,
}

# Procesar resultados
if submitted:
    if not empresa or not email or not nombre:
        st.error("Por favor completa todos los campos marcados con asterisco (*).")
    else:
        respuestas = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]
        
        # Conteo interno de puntos mediante el diccionario
        total_score = sum(scores_map.get(r, 0) for r in respuestas)

        # Diagnóstico y paquete sugerido
        if total_score <= 7:
            nivel = "Riesgo Alto"
            paquete = "Paquete 1: Productividad Esencial"
            mensaje = "Su empresa presenta vulnerabilidades críticas en respaldo y seguridad. Una falla en un equipo o un ataque informático podría pausar sus operaciones indefinidamente."
        elif total_score <= 14:
            nivel = "Madurez Intermedia"
            paquete = "Paquete 2: Protección Empresarial"
            mensaje = "Cuenta con buenas bases operativas, pero existen brechas importantes en la automatización de respaldos en la nube y en la protección de sus cuentas."
        else:
            nivel = "Protección Avanzada"
            paquete = "Paquete 3: Continuidad 360°"
            mensaje = "Su empresa cuenta con una postura tecnológica sólida. Le recomendamos mantener revisiones periódicas para prevenir nuevas amenazas."

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

        # Agrupar preguntas para el PDF
        respuestas_detalle = {
            "Trabajo en Equipo y Productividad (Microsoft)": [(q1_txt, q1), (q2_txt, q2), (q3_txt, q3)],
            "Protección de Equipos y Accesos (Acronis / Microsoft)": [(q4_txt, q4), (q5_txt, q5), (q6_txt, q6)],
            "Respaldo y Continuidad del Negocio (Acronis)": [(q7_txt, q7), (q8_txt, q8), (q9_txt, q9), (q10_txt, q10)]
        }

        # Generar PDF en memoria
        pdf_bytes = generar_pdf(empresa, nombre, email, usuarios, total_score, nivel, paquete, mensaje, respuestas_detalle)

        # Botón de Descarga del PDF
        st.subheader("📥 Descargar Informe Ejecutivo")
        st.write("Obtenga el reporte completo en PDF con el desglose de sus respuestas y las recomendaciones de TIS Solutions.")
        
        st.download_button(
            label="📄 Descargar Informe Ejecutivo (PDF)",
            data=pdf_bytes,
            file_name=f"Informe_Ejecutivo_TIS_{empresa.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
