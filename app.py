import streamlit as st

# 🔐 password admin
ADMIN_PASSWORD = "lucasplant6354"

# ---------------- DADOS ---------------- #

if "videos" not in st.session_state:
    st.session_state.videos = [
        "Como regar plantas corretamente",
        "Como plantar uma semente"
    ]

info_nova = [
    "As plantas precisam de luz solar ☀️",
    "Regar demasiado pode matar a planta 💧"
]

avisos = [
    "Não partilhar passwords 🔒",
    "Cuidado com plantas tóxicas ⚠️"
]

# ---------------- UI TOPO ---------------- #

st.markdown(
    "<h1 style='text-align:center;'>🍃 Plant Videos</h1>",
    unsafe_allow_html=True
)

st.markdown("---")

# ---------------- SIDEBAR ---------------- #

menu = st.sidebar.selectbox(
    "🌿 Menu",
    ["🎥 Vídeos", "🆕 Informação", "⚠️ Avisos"]
)

# ---------------- VÍDEOS ---------------- #

if menu == "🎥 Vídeos":
    st.subheader("🎥 Vídeos")

    for v in st.session_state.videos:
        st.write("▶", v)

    st.markdown("---")

    st.subheader("➕ Adicionar vídeo (admin)")

    password = st.text_input("Password", type="password")

    if password == ADMIN_PASSWORD:
        novo_video = st.text_input("Nome do vídeo")

        if st.button("Adicionar vídeo"):
            if novo_video:
                st.session_state.videos.append(novo_video)
                st.success("Vídeo adicionado com sucesso! 🌱")

    elif password:
        st.error("Password incorreta!")

# ---------------- INFO ---------------- #

elif menu == "🆕 Informação":
    st.subheader("🆕 Informação nova")

    for i in info_nova:
        st.write("🌱", i)

# ---------------- AVISOS ---------------- #

elif menu == "⚠️ Avisos":
    st.subheader("⚠️ Avisos")

    for a in avisos:
        st.write("❗", a)

# ---------------- FOOTER ---------------- #

st.markdown("---")
st.caption("🌿 Plant Videos App - feito por ti")
