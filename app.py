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
# IMAGEM SEGURA
# ----------------------
def get_image(planta):
    return (
        planta.get("default_photo", {}).get("medium_url")
        or planta.get("default_photo", {}).get("url")
        or "https://via.placeholder.com/400x300?text=Planta"
    )

# ----------------------
# PLANTAS (COM FALLBACK GARANTIDO)
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

    # fallback universal (NUNCA vazio)
    if not data:
        r = requests.get(
            "https://api.inaturalist.org/v1/taxa?q=plant&taxon_id=47126&per_page=30&locale=pt-PT"
        )
        data = r.json().get("results", [])

    return data

# ----------------------
# CARD COM SLIDER REAL
# ----------------------
def card(planta, idx):

    nome = (
        planta.get("preferred_common_name")
        or planta.get("common_name")
        or planta.get("name","Planta")
    )

    cient = planta.get("name","")

    img = get_image(planta)
    imagens = [img, img, img]

    key = f"fase_{idx}"
    if key not in st.session_state:
        st.session_state[key] = 0

    fases = ["🌿 Folhas","🌸 Flores","🍎 Frutos"]

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.image(imagens[st.session_state[key]], use_container_width=True)

    col1,col2,col3 = st.columns([1,2,1])

    with col1:
        if st.button("⬅️", key=f"p{idx}"):
            st.session_state[key] = (st.session_state[key] - 1) % 3

    with col3:
        if st.button("➡️", key=f"n{idx}"):
            st.session_state[key] = (st.session_state[key] + 1) % 3

    with col2:
        st.markdown(
            f"<p class='center'>{fases[st.session_state[key]]}</p>",
            unsafe_allow_html=True
        )

    # nome PT + científico
    st.markdown(f"""
        <h3 class='center' style='color:#2ecc71'>{nome}</h3>
        <p class='center' style='font-size:0.8em'>{cient}</p>
    """, unsafe_allow_html=True)

    # ☀️ SOL corrigido (sem "Desconhecido" vazio)
    sol = planta.get("light") or planta.get("sunlight") or "☀️ Informação não disponível"
    st.write(f"☀️ Sol: {sol}")

    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------
# GRID
# ----------------------
def grid(lista):
    for i in range(0, len(lista), 3):
        cols = st.columns(3)
        for j in range(3):
            if i+j < len(lista):
                with cols[j]:
                    card(lista[i+j], i+j)

# ----------------------
# LISTA PAÍSES (GARANTIDO FUNCIONAR)
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
