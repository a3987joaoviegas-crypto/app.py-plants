import streamlit as st
import requests

st.set_page_config(page_title="🌿 Plants World", layout="wide")

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
    margin-bottom:15px;
    color:white;
}

.center{text-align:center;}
</style>
""", unsafe_allow_html=True)

# ----------------------
# DADOS CIDADES
# ----------------------
cidades_por_pais = {
    "Portugal": ["Lisboa","Porto","Coimbra","Faro"],
    "Espanha": ["Madrid","Barcelona","Valência","Sevilha"],
    "França": ["Paris","Lyon","Marselha","Nice"],
    "Brasil": ["São Paulo","Rio de Janeiro","Brasília","Salvador"],
    "Estados Unidos": ["New York","Los Angeles","Chicago","Miami"],
    "China": ["Pequim","Xangai","Shenzhen","Guangzhou"]
}

# ----------------------
# IMAGEM SEGURA
# ----------------------
def get_image(planta):
    try:
        photo = planta.get("default_photo")
        if photo and isinstance(photo, dict):
            return photo.get("medium_url") or photo.get("url")
    except:
        pass

    return "https://via.placeholder.com/400x300?text=Planta"

# ----------------------
# BUSCAR PLANTAS (SEMPRE FUNCIONA)
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
# FASES INTELIGENTES
# ----------------------
def get_fases(planta, img):

    fases = [
        ("🌱 Bebé (folhas)", img),
        ("🌸 Flor", img)
    ]

    nome = (planta.get("name","") + planta.get("common_name","")).lower()

    if any(x in nome for x in ["fruit","tree","apple","orange","banana","berry"]):
        fases.append(("🍎 Fruto", img))

    return fases

# ----------------------
# CARD
# ----------------------
def card(planta, idx):

    nome = (
        planta.get("preferred_common_name")
        or planta.get("common_name")
        or planta.get("name","Planta")
    )

    cient = planta.get("name","")

    img = get_image(planta)

    fases = get_fases(planta, img)

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
# PAÍSES
# ----------------------
paises = [
"Portugal","Espanha","França","Alemanha","Itália","Brasil","Estados Unidos",
"Canadá","México","Argentina","Chile","Peru","Colômbia","China","Japão",
"Índia","Austrália","África do Sul","Egipto","Marrocos","Nigéria","Quénia",
"Turquia","Rússia","Ucrânia","Polónia","Suécia","Noruega","Finlândia",
"Dinamarca","Grécia","Tailândia","Vietname","Indonésia","Filipinas",
"Coreia do Sul","Arábia Saudita","Irão","Paquistão"
]

florestas = ["Amazónia","Congo","Taiga","Savana"]

# ----------------------
# SIDEBAR
# ----------------------
with st.sidebar:
    st.title("🌿 Plants World")

    menu = ["🌍 Países","🌲 Florestas","🔬 Laboratório"]
    aba = st.radio("Navegação", menu)

# ----------------------
# PÁGINAS
# ----------------------

if aba == "🌍 Países":
    sel = st.selectbox("Escolhe país:", paises)

    st.subheader("🏙️ Cidades")
    st.write(" | ".join(cidades_por_pais.get(sel, ["Cidade principal","Capital"])))

    st.subheader("🌿 Plantas")
    grid(get_plantas(sel))

elif aba == "🌲 Florestas":
    sel = st.selectbox("Escolhe floresta:", florestas)
    grid(get_plantas(sel))

elif aba == "🔬 Laboratório":
    q = st.text_input("Pesquisar planta:")
    if q:
        grid(get_plantas(q))
    else:
        st.info("Escreve o nome de uma planta 🌿")
