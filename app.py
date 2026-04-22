import streamlit as st
import requests

# ----------------------
# CONFIG
# ----------------------
st.set_page_config(page_title="🌿 Plants World", layout="wide")

# ----------------------
# CSS
# ----------------------
st.markdown("""
<style>
.stApp {
    background-color: #0b1117;
}
.card {
    background-color:#1a1c23;
    border-radius:20px;
    padding:12px;
    border:4px solid #2ecc71;
    margin-bottom:15px;
    color:white;
}
.img {
    width:100%;
    border-radius:15px;
}
.center {
    text-align:center;
}
</style>
""", unsafe_allow_html=True)

# ----------------------
# IMAGENS REAIS (UNSPLASH)
# ----------------------
def get_imgs(nome):
    base = "https://source.unsplash.com/400x300/?"
    return [
        base + nome + ",leaf,plant",
        base + nome + ",flower,plant",
        base + nome + ",fruit,plant"
    ]

# ----------------------
# API PLANTAS (TREFLE)
# ----------------------
API_KEY = "SUA_API_AQUI"  # mete a tua chave da Trefle

def get_plantas(query):
    url = f"https://trefle.io/api/v1/plants/search?token={API_KEY}&q={query}"
    r = requests.get(url)
    if r.status_code != 200:
        return []
    return r.json().get("data", [])

# ----------------------
# CARTÃO COM SLIDER REAL
# ----------------------
def card(planta, idx):
    nome = planta.get("common_name") or planta.get("scientific_name","Planta")
    cient = planta.get("scientific_name","Desconhecido")
    sol = planta.get("sunlight","Desconhecido")
    agua = planta.get("watering","Desconhecido")

    imagens = get_imgs(nome)

    key = f"fase_{idx}"
    if key not in st.session_state:
        st.session_state[key] = 0

    st.markdown('<div class="card">', unsafe_allow_html=True)

    # imagem atual
    st.image(imagens[st.session_state[key]], use_container_width=True)

    col1, col2, col3 = st.columns([1,2,1])

    with col1:
        if st.button("⬅️", key=f"prev_{idx}"):
            st.session_state[key] = (st.session_state[key] - 1) % 3

    with col3:
        if st.button("➡️", key=f"next_{idx}"):
            st.session_state[key] = (st.session_state[key] + 1) % 3

    fases = ["🌿 Folhas", "🌸 Flores", "🍎 Frutos"]

    with col2:
        st.markdown(
            f"<p class='center'>{fases[st.session_state[key]]}</p>",
            unsafe_allow_html=True
        )

    st.markdown(f"""
        <h3 class="center" style="color:#2ecc71;">{nome}</h3>
        <p class="center" style="font-size:0.8em;">{cient}</p>
        <p>☀️ Sol: {sol}</p>
        <p>💧 Água: {agua}</p>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------
# GRELHA
# ----------------------
def grid(lista):
    for i in range(0, len(lista), 3):
        cols = st.columns(3)
        for j in range(3):
            if i+j < len(lista):
                with cols[j]:
                    card(lista[i+j], i+j)

# ----------------------
# PAÍSES
# ----------------------
paises = [
    'Portugal','Espanha','França','Alemanha','Itália','Brasil','Estados Unidos',
    'Canadá','México','Argentina','Chile','Peru','Colômbia','China','Japão',
    'Índia','Austrália','África do Sul','Egipto','Marrocos','Nigéria','Quénia',
    'Turquia','Rússia','Ucrânia','Polónia','Suécia','Noruega','Finlândia',
    'Dinamarca','Grécia','Tailândia','Vietname','Indonésia','Filipinas',
    'Coreia do Sul','Arábia Saudita','Irão','Paquistão'
]

# ----------------------
# SIDEBAR
# ----------------------
with st.sidebar:
    st.title("🌿 Plants World")

    menu = ["🌍 Países", "🔬 Laboratório"]
    aba = st.radio("Navegação", menu)

# ----------------------
# PÁGINAS
# ----------------------
if aba == "🌍 Países":
    sel = st.selectbox("Escolhe um país:", paises)
    plantas = get_plantas(sel)
    grid(plantas)

elif aba == "🔬 Laboratório":
    query = st.text_input("Pesquisar planta:")
    if query:
        plantas = get_plantas(query)
        grid(plantas)
    else:
        st.info("Escreve o nome de uma planta 🌿")
