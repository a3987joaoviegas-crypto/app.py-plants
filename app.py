import streamlit as st
import requests

st.set_page_config(page_title="🌿 Plants World", layout="wide")

# ----------------------
# ESTADO
# ----------------------
if "jardim" not in st.session_state:
    st.session_state.jardim = []

# ----------------------
# IMAGEM SEGURA
# ----------------------
def get_image(taxon):
    try:
        photo = taxon.get("default_photo")
        if isinstance(photo, dict):
            return photo.get("medium_url") or photo.get("url")
    except:
        pass

    return "https://upload.wikimedia.org/wikipedia/commons/3/3f/Fronde_de_foug%C3%A8re.jpg"

# ----------------------
# API PLANTAS
# ----------------------
def get_plants(query):
    try:
        r = requests.get(
            f"https://api.inaturalist.org/v1/taxa?q={query}&taxon_id=47126&per_page=25",
            timeout=5
        )
        return r.json().get("results", [])
    except:
        return []

# ----------------------
# IA IDENTIFICAÇÃO (CÂMARA)
# ----------------------
def identify(file):
    try:
        r = requests.post(
            "https://api.inaturalist.org/v1/computervision/score_image",
            files={"file": file},
            timeout=15
        )
        return r.json().get("results", [])
    except:
        return []

# ----------------------
# CARD
# ----------------------
def card(taxon, idx):

    nome = (
        taxon.get("preferred_common_name")
        or taxon.get("name")
        or "Planta"
    )

    cient = taxon.get("name", "")
    img = get_image(taxon)

    st.markdown("""
    <div style="border:2px solid #2ecc71;padding:10px;border-radius:15px;margin-bottom:10px">
    """, unsafe_allow_html=True)

    st.image(img, use_container_width=True)

    st.markdown(f"### 🌱 {nome}")
    st.markdown(f"*{cient}*")

    if st.button(f"⭐ Guardar {nome}", key=idx):
        if nome not in st.session_state.jardim:
            st.session_state.jardim.append(nome)

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------
# GRID
# ----------------------
def grid(lista):
    for i in range(0, len(lista), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(lista):
                with cols[j]:
                    card(lista[i + j], i + j)

# ----------------------
# DADOS
# ----------------------
paises = ["Portugal","Espanha","França","Brasil","Estados Unidos","China","Japão"]
florestas = ["Amazónia","Congo","Taiga","Savana"]

# ----------------------
# VISION AI (CÂMARA REAL)
# ----------------------
def vision():

    st.title("📸 Vision AI")

    file = st.camera_input("Tira uma foto da planta")

    if file:

        st.image(file, use_container_width=True)

        st.info("A identificar planta...")

        results = identify(file)

        if not results:
            st.warning("🌱 Não foi possível identificar com certeza.")
            return

        for r in results[:5]:

            taxon = r.get("taxon", {})

            nome = (
                taxon.get("preferred_common_name")
                or taxon.get("name")
                or "Desconhecido"
            )

            cient = taxon.get("name", "")
            img = get_image(taxon)
            score = round(r.get("score", 0) * 100, 2)

            if score < 10:
                continue

            st.markdown("---")
            st.image(img, width=250)

            st.markdown(f"### 🌱 {nome}")
            st.markdown(f"🧬 {cient}")
            st.markdown(f"🎯 Confiança: {score}%")

            if st.button(f"⭐ Guardar {nome}", key=nome):
                if nome not in st.session_state.jardim:
                    st.session_state.jardim.append(nome)

# ----------------------
# JARDIM
# ----------------------
def garden():

    st.title("🌿 Jardim")

    if not st.session_state.jardim:
        st.info("Ainda vazio 🌱")
    else:
        for p in st.session_state.jardim:
            st.write("🌱", p)

# ----------------------
# SIDEBAR
# ----------------------
with st.sidebar:
    st.title("🌿 Plants World")

    menu = ["🌍 Países","🌲 Florestas","🔬 Laboratório","📸 Vision AI","⭐ Jardim"]
    aba = st.radio("Menu", menu)

# ----------------------
# ROUTER
# ----------------------
if aba == "🌍 Países":
    sel = st.selectbox("País", paises)
    grid(get_plants(sel))

elif aba == "🌲 Florestas":
    sel = st.selectbox("Floresta", florestas)
    grid(get_plants(sel))

elif aba == "🔬 Laboratório":
    q = st.text_input("Pesquisar planta")
    if q:
        grid(get_plants(q))

elif aba == "📸 Vision AI":
    vision()

elif aba == "⭐ Jardim":
    garden()
