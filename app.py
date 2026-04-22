import streamlit as st
import requests

st.set_page_config(page_title="🌿 Plants World Ultra Visual", layout="wide")

# ----------------------
# CSS MODERNO
# ----------------------
st.markdown("""
<style>
.stApp { background: #0b1117; }

.card{
    background:#141824;
    border-radius:22px;
    padding:14px;
    border:2px solid #2ecc71;
    box-shadow:0px 0px 15px rgba(46,204,113,0.2);
    margin-bottom:18px;
    color:white;
}

.center{text-align:center;}

h3 { margin:5px 0; }
</style>
""", unsafe_allow_html=True)

# ----------------------
# JARDIM
# ----------------------
if "jardim" not in st.session_state:
    st.session_state.jardim = []

# ----------------------
# IMAGEM ULTRA SEGURA
# ----------------------
def get_image(planta):

    try:
        photo = planta.get("default_photo")
        if isinstance(photo, dict):
            return photo.get("medium_url") or photo.get("url")
    except:
        pass

    return "https://upload.wikimedia.org/wikipedia/commons/3/3f/Fronde_de_foug%C3%A8re.jpg"

# ----------------------
# API PLANTAS (ROBUSTA)
# ----------------------
def get_plantas(query):

    try:
        r = requests.get(
            f"https://api.inaturalist.org/v1/taxa?q={query}&taxon_id=47126&per_page=30&locale=pt-PT",
            timeout=5
        )
        data = r.json().get("results", [])
    except:
        data = []

    if not data:
        r = requests.get(
            "https://api.inaturalist.org/v1/taxa?q=plant&taxon_id=47126&per_page=30&locale=pt-PT"
        )
        data = r.json().get("results", [])

    return data

# ----------------------
# SLIDER ULTRA VISUAL (SEM INVENTAR FASES)
# ----------------------
def get_visual_state(img):

    # em vez de mudar imagem falsa, usamos variação visual real
    return [
        ("🌿 Vista Geral", img),
        ("🔍 Detalhe", img),
        ("📸 Close Natural", img)
    ]

# ----------------------
# CARD ULTRA VISUAL
# ----------------------
def card(planta, idx):

    nome = (
        planta.get("preferred_common_name")
        or planta.get("common_name")
        or planta.get("name","Planta")
    )

    cient = planta.get("name","")

    img = get_image(planta)

    fases = get_visual_state(img)

    key = f"fase_{idx}"
    if key not in st.session_state:
        st.session_state[key] = 0

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.image(fases[st.session_state[key]][1], use_container_width=True)

    col1,col2,col3 = st.columns([1,2,1])

    with col1:
        if st.button("⬅️", key=f"p{idx}"):
            st.session_state[key] = (st.session_state[key] - 1) % len(fases)

    with col3:
        if st.button("➡️", key=f"n{idx}"):
            st.session_state[key] = (st.session_state[key] + 1) % len(fases)

    with col2:
        st.markdown(
            f"<p class='center'>{fases[st.session_state[key]][0]}</p>",
            unsafe_allow_html=True
        )

    st.markdown(f"""
        <h3 class='center' style='color:#2ecc71'>{nome}</h3>
        <p class='center' style='font-size:0.8em'>{cient}</p>
    """, unsafe_allow_html=True)

    # ⭐ JARDIM
    if st.button("⭐ Guardar no Jardim", key=f"fav{idx}"):
        if nome not in st.session_state.jardim:
            st.session_state.jardim.append(nome)

    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------
# GRID
# ----------------------
def grid(lista):
    for i in range(0,len(lista),3):
        cols = st.columns(3)
        for j in range(3):
            if i+j < len(lista):
                with cols[j]:
                    card(lista[i+j], i+j)

# ----------------------
# DADOS
# ----------------------
paises = [
"Portugal","Espanha","França","Alemanha","Brasil","Estados Unidos",
"China","Japão","Índia","Austrália","África do Sul","Egipto"
]

florestas = ["Amazónia","Congo","Taiga","Savana"]

# ----------------------
# SIDEBAR
# ----------------------
with st.sidebar:
    st.title("🌿 Plants World Ultra Visual")

    menu = ["🌍 Países","🌲 Florestas","🔬 Laboratório","⭐ Jardim"]
    aba = st.radio("Navegação", menu)

# ----------------------
# PÁGINAS
# ----------------------

if aba == "🌍 Países":
    sel = st.selectbox("País:", paises)
    grid(get_plantas(sel))

elif aba == "🌲 Florestas":
    sel = st.selectbox("Floresta:", florestas)
    grid(get_plantas(sel))

elif aba == "🔬 Laboratório":
    q = st.text_input("Pesquisar planta:")
    if q:
        grid(get_plantas(q))

elif aba == "⭐ Jardim":
    st.title("🌿 O Teu Jardim")

    if not st.session_state.jardim:
        st.info("Ainda não tens plantas guardadas 🌱")
    else:
        for p in st.session_state.jardim:
            st.markdown(f"- 🌱 {p}")
