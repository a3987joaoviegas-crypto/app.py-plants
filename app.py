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
# JARDIM (FAVORITOS)
# ----------------------
if "jardim" not in st.session_state:
    st.session_state.jardim = []

# ----------------------
# IMAGENS POR FASE (SEGURO)
# ----------------------
def get_images(planta, nome):

    base = nome.replace(" ", "+") + "+plant"

    return {
        "leaf": f"https://source.unsplash.com/400x300/?{base},leaf",
        "flower": f"https://source.unsplash.com/400x300/?{base},flower",
        "fruit": f"https://source.unsplash.com/400x300/?{base},fruit"
    }

# ----------------------
# API PLANTAS (SEMPRE FUNCIONA)
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
# CARD PLANTA (SLIDER REAL)
# ----------------------
def card(planta, idx):

    nome = (
        planta.get("preferred_common_name")
        or planta.get("common_name")
        or planta.get("name","Planta")
    )

    cient = planta.get("name","")

    imgs = get_images(planta, nome)

    fases = [
        ("🌱 Folhas (bebé)", imgs["leaf"]),
        ("🌸 Flor", imgs["flower"]),
        ("🍎 Fruto", imgs["fruit"])
    ]

    key = f"fase_{idx}"
    if key not in st.session_state:
        st.session_state[key] = 0

    st.markdown('<div class="card">', unsafe_allow_html=True)

    # imagem fase atual
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
# LISTAS
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

    menu = ["🌍 Países","🌲 Florestas","🔬 Laboratório","⭐ Jardim"]
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

elif aba == "⭐ Jardim":
    st.title("🌿 O Teu Jardim")

    if not st.session_state.jardim:
        st.info("Ainda não tens plantas guardadas 🌱")
    else:
        for p in st.session_state.jardim:
            st.markdown(f"- 🌱 {p}")
