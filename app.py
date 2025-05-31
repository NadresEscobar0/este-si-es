import streamlit as st
import google.generativeai as genai
import re

st.set_page_config(page_title="VictorIA Nexus - Asistente Académico Adaptativo", page_icon="🧠")

# --- CSS para panel inferior compacto y fijo ---
st.markdown("""
    <style>
    .block-container {
        padding-bottom: 65px !important;
    }
    #fixed-bottom-bar {
        position: fixed;
        left: 0;
        right: 0;
        bottom: 0;
        background: #f8f9fa;
        border-top: 2px solid #e3e3e3;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.07);
        z-index: 9999;
        padding: 0.3em 0.7em 0.3em 0.7em;
        display: flex;
        align-items: center;
        gap: 0.5em;
    }
    #fixed-bottom-bar input[type="text"] {
        flex: 1;
        min-width: 0;
        border-radius: 6px;
        border: 1px solid #b3c2d1;
        font-size: 1.02rem;
        padding: 0.4em 0.6em;
        background: #fff;
        outline: none;
    }
    #fixed-bottom-bar button {
        width: 90px;
        height: 36px;
        background: #2b7de9;
        color: white;
        font-weight: bold;
        border-radius: 6px;
        font-size: 1rem;
        border: none;
        cursor: pointer;
        transition: background 0.2s;
    }
    #fixed-bottom-bar button:hover {
        background: #1b4a7a;
    }
    </style>
""", unsafe_allow_html=True)

# API Key y modelo
API_KEY = "AIzaSyDDgVzgub-2Va_5xCVcKBU_kYtpqpttyfk"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

st.title("VictorIA Nexus: Asistente Académico Adaptativo")
st.markdown("""
<div style="text-align: center; margin-bottom: 2.5rem;">
    <b>
    <span style='font-size:1.3em; color:#2b7de9;'>¡Bienvenido a VictorIA Nexus!</span><br><br>
    Mucho más que un asistente: VictorIA Nexus es el puente entre tu curiosidad y el conocimiento.<br><br>
    Esta plataforma de inteligencia artificial adaptativa no solo responde preguntas, sino que guía, inspira y personaliza cada interacción según tu estilo de aprendizaje.<br><br>
    Inspirada en la pedagogía y la tecnología, VictorIA Nexus fomenta el pensamiento crítico, la creatividad y la autonomía. Aquí, cada consulta es una oportunidad para descubrir, reflexionar y crecer.<br><br>
    <span style='color: #2b7de9;'>Elige tu estilo de aprendizaje, plantea tu reto académico y deja que VictorIA Nexus te acompañe en el viaje de transformar dudas en descubrimientos. No solo obtendrás respuestas, sino caminos para aprender y crear.</span>
    </b>
</div>
""", unsafe_allow_html=True)

estilo = st.selectbox(
    "¿Cuál es tu estilo de aprendizaje preferido?",
    ("Visual", "Auditivo", "Kinestésico")
)

if "historial" not in st.session_state:
    st.session_state.historial = []

def construir_prompt(pregunta, estilo):
    # Detecta si la pregunta es sobre el creador
    pregunta_baja = pregunta.lower()
    if (
        "quién te desarrolló" in pregunta_baja
        or "quien te desarrolló" in pregunta_baja
        or "quién es tu creador" in pregunta_baja
        or "quien es tu creador" in pregunta_baja
        or "autor" in pregunta_baja
    ):
        return "Por favor, responde únicamente: 'Fui desarrollado por Pedro Tovar.'"
    # Prompt normal
    base = (
        "Eres VictorIA Nexus, una asistente académica ética, creativa y adaptativa. "
        "Prioriza siempre responder de forma clara, extensa y concreta a la pregunta planteada, "
        "proporcionando una explicación detallada, profunda y bien desarrollada, con ejemplos y contexto para que cualquier estudiante pueda comprender a fondo el tema. "
        "No seas breve ni superficial. "
        "Después de la respuesta, añade una explicación creativa, extensa y adaptada únicamente al estilo de aprendizaje indicado, "
        "con el objetivo de fomentar el aprendizaje real, la creatividad y el pensamiento crítico. "
        "Desarrolla la explicación y utiliza recursos propios del estilo elegido. "
        "Nunca menciones que eres de Google, Gemini, Streamlit, ni ningún proveedor externo. "
        "Si te preguntan por tu creador, responde únicamente: 'Fui desarrollado por Pedro Tovar.'"
    )
    if estilo == "Visual":
        detalle = "Después de la respuesta, utiliza analogías visuales, descripciones gráficas, esquemas mentales, mapas conceptuales o ejemplos visuales. No expliques otros estilos."
    elif estilo == "Auditivo":
        detalle = "Después de la respuesta, utiliza ejemplos auditivos, relatos, metáforas sonoras, explicaciones habladas o historias narradas. No expliques otros estilos."
    else:
        detalle = "Después de la respuesta, sugiere actividades prácticas, ejemplos kinestésicos, ejercicios paso a paso y propuestas que impliquen acción física. No expliques otros estilos."
    return f"{base} Estilo de aprendizaje: {estilo}. {detalle} Pregunta: {pregunta}"

def limpiar_html(texto):
    texto_limpio = re.sub(r'</?div[^>]*>', '', texto)
    return texto_limpio.strip()

if st.session_state.historial:
    st.markdown("### Historial de Interacciones")
    for i, entrada in enumerate(st.session_state.historial[::-1], 1):
        respuesta_limpia = limpiar_html(entrada['respuesta'])
        st.markdown(f"""
        <div style="
            background-color:#1b4a7a;
            border-radius:10px;
            padding:1em;
            margin-bottom:0.5em;
            color:#ffffff;">
            <b><span style="color:#FFD700;">{i}. Tú:</span></b> {entrada['pregunta']}<br>
            <b><span style="color:#87CEEB;">VictorIA Nexus:</span></b> {respuesta_limpia}
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("¡Haz tu primera pregunta académica abajo para comenzar!")

# --- PANEL INFERIOR FIJO Y FUNCIONAL, ULTRA-COMPACTO ---
import streamlit.components.v1 as components

components.html("""
<div id="fixed-bottom-bar">
    <form id="pregunta-form" autocomplete="off">
        <input type="text" id="pregunta-input" maxlength="500" placeholder="Haz tu pregunta académica aquí..." autofocus required />
        <button type="submit">Preguntar</button>
    </form>
</div>
<script>
const form = document.getElementById('pregunta-form');
const input = document.getElementById('pregunta-input');
form.onsubmit = function(e){
    e.preventDefault();
    if(input.value.trim().length > 0){
        window.parent.postMessage({type: 'streamlit:setComponentValue', value: input.value}, '*');
        input.value = '';
    }
};
</script>
""", height=60, key="fixed_panel")

# Captura la pregunta desde el componente HTML (solo si el usuario usa el panel fijo)
if 'pregunta_usuario' not in st.session_state:
    st.session_state.pregunta_usuario = ""

import streamlit_js_eval
user_input = streamlit_js_eval.get_streamlit_js_eval_result("window.parent.lastUserInput")
if user_input and isinstance(user_input, str) and user_input.strip():
    pregunta = user_input.strip()
    enviar = True
else:
    # Fallback para usuarios que usen solo el formulario Streamlit (en caso de error)
    with st.form(key="formulario_pregunta", clear_on_submit=True):
        pregunta = st.text_input("", max_chars=500, key="pregunta_usuario")
        enviar = st.form_submit_button("Preguntar")

if 'enviar' in locals() and enviar and pregunta.strip():
    pregunta_baja = pregunta.lower()
    # Respuesta de autoría directa
    if (
        "quién te desarrolló" in pregunta_baja
        or "quien te desarrolló" in pregunta_baja
        or "quién es tu creador" in pregunta_baja
        or "quien es tu creador" in pregunta_baja
        or "autor" in pregunta_baja
    ):
        respuesta = "Fui desarrollado por Pedro Tovar."
        respuesta_limpia = respuesta
    else:
        prompt = construir_prompt(pregunta, estilo)
        try:
            respuesta = model.generate_content(prompt)
            respuesta = respuesta.text
        except Exception as e:
            respuesta = f"Error al generar respuesta: {e}"
        respuesta_limpia = limpiar_html(respuesta)
    st.session_state.historial.append({"pregunta": pregunta, "respuesta": respuesta_limpia})
    st.markdown(f"""
    <div style="
        background-color:#1b4a7a;
        border-radius:10px;
        padding:1em;
        margin-bottom:0.5em;
        color:#ffffff;">
        <b><span style="color:#FFD700;">Tú:</span></b> {pregunta}<br>
        <b><span style="color:#87CEEB;">VictorIA Nexus:</span></b> {respuesta_limpia}
    </div>
    """, unsafe_allow_html=True)
elif 'enviar' in locals() and enviar:
    st.warning("Por favor, escribe una pregunta antes de continuar.")

# --- FIRMA LEGAL ---
st.markdown("""
---
**© 2025 Pedro Tovar. Todos los derechos reservados.**  
Esta aplicación fue desarrollada por Pedro Tovar para fines académicos. Prohibida su reproducción total o parcial sin autorización.
""")
