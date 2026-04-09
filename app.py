import streamlit as st
from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# =========================
# CONFIGURACIÓN GENERAL
# =========================
st.set_page_config(
    page_title="Termómetro Emocional",
    page_icon="💭",
    layout="wide"
)

# =========================
# ESTILOS
# =========================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%);
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }

    .hero-box {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 20px;
        padding: 1.4rem 1.6rem;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.07);
        margin-bottom: 1rem;
    }

    .card-box {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 1.2rem 1.3rem;
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.06);
        margin-bottom: 1rem;
    }

    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #111827;
        margin-bottom: 0.2rem;
    }

    .sub-title {
        font-size: 1.08rem;
        color: #4b5563;
        margin-bottom: 0.3rem;
    }

    .small-text {
        color: #6b7280;
        font-size: 0.95rem;
    }

    .stButton > button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(90deg, #2563eb 0%, #4f46e5 100%);
        color: white;
        font-weight: 700;
        border: none;
        padding: 0.7rem 1rem;
    }

    .stButton > button:hover {
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# FUNCIONES
# =========================
def analizar_sentimiento(texto):
    blob = TextBlob(texto)
    polaridad = round(blob.sentiment.polarity, 2)
    subjetividad = round(blob.sentiment.subjectivity, 2)

    if polaridad > 0.15:
        etiqueta = "Positivo"
        emoji = "😊"
        color = "#16a34a"
        mensaje = "El texto transmite una emoción favorable, optimista o motivadora."
    elif polaridad < -0.15:
        etiqueta = "Negativo"
        emoji = "😟"
        color = "#dc2626"
        mensaje = "El texto refleja malestar, tensión, tristeza o una valoración desfavorable."
    else:
        etiqueta = "Neutral"
        emoji = "😐"
        color = "#ca8a04"
        mensaje = "El texto se percibe equilibrado o con poca carga emocional marcada."

    return polaridad, subjetividad, etiqueta, emoji, color, mensaje


def generar_nube(texto):
    stopwords_extra = STOPWORDS.union(
        {"really", "very", "just", "like", "thing", "things"}
    )

    nube = WordCloud(
        width=900,
        height=450,
        background_color="white",
        stopwords=stopwords_extra,
        colormap="viridis"
    ).generate(texto)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(nube, interpolation="bilinear")
    ax.axis("off")
    return fig


# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("## ℹ️ Guía de lectura")
    st.write("**Polaridad** indica si el texto es positivo, negativo o neutral.")
    st.write("**Subjetividad** muestra qué tanto el mensaje expresa opiniones, emociones o juicios.")
    st.markdown("---")
    st.markdown("### ✅ Recomendaciones")
    st.write("- Escribe una frase o un párrafo breve.")
    st.write("- Puedes usar inglés o español, pero TextBlob funciona mejor en inglés.")
    st.write("- Después del análisis, revisa la interacción que aparece según el resultado.")

# =========================
# ENCABEZADO
# =========================
st.markdown("""
<div class="hero-box">
    <div class="main-title">💭 Termómetro Emocional</div>
    <div class="sub-title">
        Analiza el sentimiento de un texto, identifica su nivel de subjetividad y visualiza sus palabras clave.
    </div>
    <div class="small-text">
        Esta versión integra análisis de sentimiento con nube de palabras e interacción personalizada según el resultado obtenido.
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# ENTRADA
# =========================
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown('<div class="card-box">', unsafe_allow_html=True)
    st.markdown("### ✍️ Texto de entrada")
    texto_usuario = st.text_area(
        "Escribe aquí la frase o párrafo que deseas analizar",
        height=220,
        placeholder="Ejemplo: I feel happy because I finished my project successfully."
    )
    analizar = st.button("Analizar sentimiento")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card-box">', unsafe_allow_html=True)
    st.markdown("### 📌 ¿Qué mide esta app?")
    st.write("**Polaridad:** valor entre -1 y 1.")
    st.write("- Cerca de **-1**: sentimiento negativo")
    st.write("- Cerca de **0**: sentimiento neutral")
    st.write("- Cerca de **1**: sentimiento positivo")
    st.write("")
    st.write("**Subjetividad:** valor entre 0 y 1.")
    st.write("- Cerca de **0**: texto más objetivo")
    st.write("- Cerca de **1**: texto más subjetivo")
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# RESULTADOS
# =========================
if analizar:
    if not texto_usuario.strip():
        st.warning("Primero debes escribir un texto para analizar.")
    else:
        polaridad, subjetividad, etiqueta, emoji, color, mensaje = analizar_sentimiento(texto_usuario)

        st.markdown('<div class="card-box">', unsafe_allow_html=True)
        st.markdown("### 📊 Resultado del análisis")

        met1, met2, met3 = st.columns(3)
        met1.metric("Polaridad", polaridad)
        met2.metric("Subjetividad", subjetividad)
        met3.metric("Clasificación", f"{etiqueta} {emoji}")

        st.markdown(
            f"""
            <div style="
                margin-top: 0.8rem;
                padding: 1rem;
                border-radius: 14px;
                background: #f8fafc;
                border-left: 6px solid {color};
                color: #111827;
                font-size: 1rem;">
                <strong>Interpretación:</strong> {mensaje}
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card-box">', unsafe_allow_html=True)
        st.markdown("### ☁️ Nube de palabras")
        fig = generar_nube(texto_usuario)
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card-box">', unsafe_allow_html=True)
        st.markdown("### 🤝 Interacción según el sentimiento")

        if etiqueta == "Positivo":
            st.success("Tu texto tiene una carga positiva.")
            accion = st.text_input("¿Qué acción concreta quieres realizar aprovechando este estado?")
            if accion:
                st.write(f"Buen paso. Podrías comenzar hoy con: **{accion}**")

        elif etiqueta == "Negativo":
            st.error("Tu texto tiene una carga negativa.")
            opcion = st.selectbox(
                "Elige una forma de responder a este estado",
                [
                    "Identificar la causa principal",
                    "Reformular el mensaje",
                    "Escribir una versión más amable"
                ]
            )

            if opcion == "Identificar la causa principal":
                causa = st.text_input("¿Qué palabra resume mejor lo que te afecta?")
                if causa:
                    st.write(f"Reconocer **{causa}** ya es un primer paso para manejar la situación.")

            elif opcion == "Reformular el mensaje":
                nuevo_texto = st.text_area("Escribe una versión más clara de tu mensaje")
                if nuevo_texto:
                    st.write("Muy bien. Reescribir el mensaje ayuda a organizar mejor lo que sientes.")

            else:
                texto_amable = st.text_area("Escribe una versión más amable contigo o con otra persona")
                if texto_amable:
                    st.write("Ese cambio de tono puede ayudarte a reducir tensión y comunicar mejor.")

        else:
            st.info("Tu texto es neutral.")
            enfoque = st.radio(
                "¿Cómo quieres enriquecer tu mensaje?",
                ["Agregar una emoción", "Agregar una opinión", "Agregar una situación concreta"]
            )
            st.write(f"Sugerencia: intenta reescribir el texto incorporando **{enfoque.lower()}**.")
        st.markdown('</div>', unsafe_allow_html=True)
