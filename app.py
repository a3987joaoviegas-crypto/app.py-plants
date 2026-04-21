import streamlit as st

# 🔐 password admin
ADMIN_PASSWORD = "lucasplant6354"

# ---------------- STATE ---------------- #

if "items" not in st.session_state:
    st.session_state.items = []

# ---------------- UI ---------------- #

st.markdown("<h1 style='text-align:center;'>🍃 Plant Videos</h1>", unsafe_allow_html=True)
st.markdown("---")

menu = st.sidebar.selectbox("🌿 Menu", ["📺 Conteúdo", "➕ Admin"])

# ---------------- CONTEÚDO ---------------- #

if menu == "📺 Conteúdo":
    st.subheader("📺 Conteúdo")

    if len(st.session_state.items) == 0:
        st.info("Ainda não há vídeos 🌱")

    for item in st.session_state.items:

        st.markdown(f"## 🌿 {item['title']}")

        # 🖼️ IMAGEM DO VÍDEO (thumbnail)
        if item["image"]:
            st.image(item["image"], use_container_width=True)

        # 🎬 VÍDEO COM ÁUDIO
        if item["video"]:
            st.video(item["video"])

        st.markdown("---")

# ---------------- ADMIN ---------------- #

elif menu == "➕ Admin":
    st.subheader("🔐 Admin")

    password = st.text_input("Password", type="password")

    if password == ADMIN_PASSWORD:

        st.success("Acesso autorizado ✔️")

        title = st.text_input("Título do vídeo")

        image_url = st.text_input("Imagem do vídeo (thumbnail) 🖼️")

        video_url = st.text_input("Link do vídeo (YouTube ou MP4) 🎬")

        if st.button("Adicionar vídeo"):
            if title:
                st.session_state.items.append({
                    "title": title,
                    "image": image_url,
                    "video": video_url
                })
                st.success("Vídeo adicionado 🌱")

    elif password:
        st.error("Password incorreta ❌")
