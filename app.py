def card(planta, idx):
    nome = (planta.get('common_name') or planta.get('scientific_name','Planta')).title()
    cient = planta.get('scientific_name','Desconhecido')

    imagens = get_imgs(nome)

    sol = planta.get('sunlight','Desconhecido')
    agua = planta.get('watering','Desconhecido')

    st.markdown(f"""
    <div class="card">

        <div id="slider-{idx}">
            <img src="{imagens[0]}" class="img" id="img-{idx}">
            
            <div style="margin-top:5px;">
                <button onclick="prev{idx}()">⬅️</button>
                <button onclick="next{idx}()">➡️</button>
            </div>

            <p id="label-{idx}">🌿 Folhas</p>
        </div>

        <h4 style="color:#2ecc71;">{nome}</h4>
        <p style="font-size:0.8em; font-style:italic;">{cient}</p>

        <p>☀️ <b>Sol:</b> {sol}</p>
        <p>💧 <b>Água:</b> {agua}</p>

    </div>

    <script>
    var imgs{idx} = ["{imagens[0]}", "{imagens[1]}", "{imagens[2]}"];
    var labels{idx} = ["🌿 Folhas","🌸 Flores","🍎 Frutos"];
    var i{idx} = 0;

    function update{idx}() {{
        document.getElementById("img-{idx}").src = imgs{idx}[i{idx}];
        document.getElementById("label-{idx}").innerText = labels{idx}[i{idx}];
    }}

    function next{idx}() {{
        i{idx} = (i{idx} + 1) % imgs{idx}.length;
        update{idx}();
    }}

    function prev{idx}() {{
        i{idx} = (i{idx} - 1 + imgs{idx}.length) % imgs{idx}.length;
        update{idx}();
    }}
    </script>
    """, unsafe_allow_html=True)
