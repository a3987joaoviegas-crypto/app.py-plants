import streamlit as st
import requests

st.set_page_config(page_title="🌿 Plants World ULTRA PRO", layout="wide")

# ----------------------
# CSS
# ----------------------
st.markdown("""
<style>
.stApp { background:#0b1117; }

.card{
    background:#1a1c23;
    border-radius:20px;
    padding:12px;
    border:3px solid #2ecc71;
    color:white;
    margin-bottom:15px;
}

.img{
    width:100%;
    border-radius:15px;
}

.center{text-align:center;}
</style>
""", unsafe_allow_html=True)

# ----------------------
# STATE (JARDIM)
# ----------------------
if "jardim" not in st.session_state:
    st.session_state.jardim = []

# ----------------------
# IMAGENS POR FASE
# ----------------------
def get_imgs(nome):
    base = "https://source.unsplash.com/400x300/?"
    return [
        base + nome + ",plant,leaf",
        base + nome + ",plant,flower",
        base + nome + ",plant,fruit"
    ]

# ----------------------
# API PLANTAS (TREFLE + FALLBACK INATURALIST)
# ----------------------
def get_plantas(query):
    # TREFLE
    try:
        url = f"https://trefle.io/api/v1/plants/search?token=SUA_API_AQUI&q={query}"
        r = requests.get(url, timeout=5)
        data = r.json().get("data", [])
        if data:
            return data
    except:
        pass

    # FALLBACK iNaturalist
    r = requests.get(
        f"https://api.inaturalist.org/v1/taxa?q={query}&taxon_id=47126&per_page=20"
    )
    return r.json().get("results", [])

# ----------------------
# CARTÃO ULTRA PRO
# ----------------------
def card(planta, idx):

    nome = planta.get("common_name") or planta.get("preferred_common_name") or planta.get("name","Planta")
    cient = planta.get("scientific_name") or planta.get("name","")

    imagens = get_imgs(nome)

    key = f"fase_{idx}"
    if key not in st.session_state:
        st.session_state[key] = 0

    st.markdown('<div class="card">', unsafe_allow_html=True)

    # imagem
    st.image(imagens[st.session_state[key]], use_container_width=True)

    col1,col2,col3 = st.columns([1,2,1])

    with col1:
        if st.button("⬅️", key=f"p{idx}"):
            st.session_state[key] = (st.session_state[key] - 1) % 3

    with col3:
        if st.button("➡️", key=f"n{idx}"):
            st.session_state[key] = (st.session_state[key] + 1) % 3

    fases = ["🌿 Folhas","🌸 Flores","🍎 Frutos"]

    with col2:
        st.markdown(f"<p class='center'>{fases[st.session_state[key]]}</p>", unsafe_allow_html=True)

    # dados
    st.markdown(f"""
        <h3 class='center' style='color:#2ecc71'>{nome}</h3>
        <p class='center' style='font-size:0.8em'>{cient}</p>
    """, unsafe_allow_html=True)

    sol = planta.get("sunlight","Desconhecido")
    agua = planta.get("watering","Desconhecido")

    st.write(f"☀️ Sol: {sol}")
    st.write(f"💧 Água: {agua}")

    # JARDIM
    if st.button("⭐ Guardar no Jardim", key=f"fav{idx}"):
        if nome not in st.session_state.jardim:
            st.session_state.jardim.append(nome)
            st.success("Guardado no Jardim 🌿")

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
florestas = ["Amazónia","Congo","Taiga","Savana"]

paises = [
"Portugal","Espanha","França","Alemanha","Itália","Brasil","Estados Unidos",
"Canadá","México","Argentina","Chile","Peru","Colômbia","China","Japão",
"Índia","Austrália","África do Sul","Egipto","Marrocos","Nigéria","Quénia",
"Turquia","Rússia","Ucrânia","Polónia","Suécia","Noruega","Finlândia",
"Dinamarca","Grécia","Tailândia","Vietname","Indonésia","Filipinas",
"Coreia do Sul","Arábia Saudita","Irão","Paquistão"
]

# ----------------------
# SIDEBAR
# ----------------------
with st.sidebar:
    st.title("🌿 Plants World ULTRA PRO")

    menu = ["🌍 Mapa","🌲 Florestas","🏳️ Países","🔬 Laboratório","⭐ Jardim"]
    aba = st.radio("Navegação", menu)

# ----------------------
# MAPA
# ----------------------
if aba == "🌍 Mapa":
    st.map()

# ----------------------
# FLORESTAS
# ----------------------
elif aba == "🌲 Florestas":
    sel = st.selectbox("Floresta:", florestas)
    grid(get_plantas(sel))

# ----------------------
# PAÍSES
# ----------------------
elif aba == "🏳️ Países":
    sel = st.selectbox("País:", paises)
    grid(get_plantas(sel))

# ----------------------
# LAB
# ----------------------
elif aba == "🔬 Laboratório":
    q = st.text_input("Pesquisar planta:")
    if q:
        grid(get_plantas(q))

# ----------------------
# JARDIM
# ----------------------
elif aba == "⭐ Jardim":
    st.title("🌿 O Teu Jardim")
    for p in st.session_state.jardim:
        st.markdown(f"- 🌱 {p}")
