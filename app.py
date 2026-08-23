from datetime import datetime
import urllib.parse
import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="ThalitaGourm - Confeitaria Premium",
    page_icon="🍰",
    layout="wide",
)

# --- CSS PERSONALIZADO (Estilo Confeitaria Premium & Correção de Cores) ---
st.markdown(
    """
    <style>
    /* Fundo geral da página em tom elegante */
    .stApp {
        background-color: #c89c7d;
        color: rgb(200, 156, 125);
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* Estilização dos títulos principais - Cor mais viva e destacada */
    h1, h2, h3 {
        color: #FF1493 !important;
        font-family: 'Georgia', serif;
        font-weight: bold;
    }
    
    /* Textos normais e descrições visíveis */
    p, span, label, .stMarkdown {
        color: #222222 !important;
    }
    
    /* Caixas de input, texto e seletores com fundo e letras escuras */
    input, textarea {
        color: #222222 !important;
        background-color: #c89c7d !important;
    }
    
    /* Cor do texto dentro dos menus de seleção (selectbox) */
    div[data-baseweb="select"] * {
        color: #FFFFFF !important;
    }
    
    /* Fundo das caixas de input e selectbox */
    div.stNumberInput, div.stTextInput, div.stSelectbox {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 5px;
        border-radius: 10px;
    }
    
    /* Botão principal de finalizar pedido */
    .stButton>button {
        background: linear-gradient(135deg, #FF69B4 0%, #D23669 100%);
        color: white;
        border-radius: 25px;
        font-weight: bold;
        border: none;
        padding: 10px 20px;
        box-shadow: 0px 4px 10px rgba(210, 54, 105, 0.3);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #D23669 0%, #FF1493 100%);
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- LAYOUT EM DUAS COLUNAS (Conteúdo principal à esquerda, Foto da Dona à direita) ---
col_principal, col_lateral = st.columns([2.5, 1])

with col_lateral:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### 👩‍🍳 Feito com Amor")
    st.write(
        "Olá! Sou a **Thalita**, criadora de cada sabor irresistível que você"
        " vai provar hoje. Peça o seu e sinta o carinho em cada fatia!"
    )
    try:
        st.image(
            "dona_thalita.jpg",
            use_container_width=True,
        )
    except:
        st.info(
            "💡 Dica: Coloque uma foto sua chamada 'dona_thalita.jpg' na pasta do"
            " projeto."
        )

with col_principal:
    st.title("🍰 ThalitaGourmet")
    st.markdown(
        "*Doce, artesanal e feito para você!*"
    )
    st.markdown("---")

    # 1. Coleta de dados do cliente
    st.subheader("1. Seus Dados para Entrega")
    nome_cliente = st.text_input("Nome Completo:")
    telefone_cliente = st.text_input("Telefone com DDD:")
    endereco = st.text_input("Endereço de Entrega (Rua, Número):")

    bairro_selecao = st.selectbox(
        "Bairro de Entrega:",
        [
            "Colinas do Sul (Frete Grátis)",
            "Planalto da Boa Esperança (Frete Grátis)",
            "Novo milênio (Frete Grátis)",
            "Outros (R$ 5,00 ou FRETE GRÁTIS a partir de 3 fatias)",
        ],
    )

    # Condicional: se escolher "Outros", abre o input para digitar o bairro
    if bairro_selecao.startswith("Outros"):
        bairro_outro = st.text_input("Digite o nome do seu bairro:")
        bairro_final = (
            bairro_outro if bairro_outro else "Outros (Não especificado)"
        )
    else:
        bairro_final = bairro_selecao.replace(" (Frete Grátis)", "")

    # 2. Cardápio com Fotos
    st.subheader("2. Cardápio de Fatias")
    cardapio = {
        "Fatia de prestígio": {
            "preco": 10.00,
            "img": "fatia_prestigio.jpg",
            "desc": "Massa molhadinha com recheio cremoso de coco e cobertura especial, 200G."
        },
        "Fatia de dois amores": {
            "preco": 12.00,
            "img": "fatia_dois_amores.jpg",
            "desc": "A perfeita combinação de brigadeiro branco cremoso e brigadeiro tradicional, 200G."
        },
        "Fatia de ninho com nutella": {
            "preco": 15.00,
            "img": "fatia_ninho.jpg",
            "desc": "Leite Ninho cremoso finalizado com generosas camadas de Nutella original, 200G."
        },
    }

    carrinho = []

    for item, dados in cardapio.items():
        st.markdown("---")  
        col_img, col_info, col_qtd = st.columns([1, 2, 1])

        with col_img:
            try:
                st.image(dados["img"], use_container_width=True)
                st.caption("*Imagem ilustrativa")
            except Exception:
                st.write("Imagem indisponível")

        with col_info:
            st.markdown(f"### {item}")
            st.write(dados["desc"])
            st.markdown(f"**Preço: R$ {dados['preco']:.2f}**")

        with col_qtd:
            st.markdown("<br>", unsafe_allow_html=True)
            qtd = st.number_input(
                f"Qtd", min_value=0, max_value=20, value=0, step=1, key=item
            )

        if qtd > 0:
            carrinho.append(
                {
                    "item": item,
                    "quantidade": qtd,
                    "preco_unitario": dados["preco"],
                    "subtotal": dados["preco"] * qtd,
                }
            )

    st.markdown("---")

    # 3. Forma de Pagamento
    st.subheader("3. Forma de Pagamento")
    forma_pagamento = st.selectbox(
        "Selecione a forma de pagamento:", ["PIX", "Dinheiro", "Cartão (+R$ 2,00)"]
    )

    # 4. Finalização e Relatório
    st.subheader("4. Resumo do Pedido")

    if st.button(
        "✨ Finalizar Pedido e Enviar para o WhatsApp", type="primary"
    ):
        if not nome_cliente or not telefone_cliente or not endereco:
            st.error("Por favor, preencha todos os seus dados pessoais!")
        elif bairro_selecao.startswith("Outros") and not bairro_outro:
            st.error("Por favor, digite o nome do seu bairro no campo indicado!")
        elif not carrinho:
            st.error("Seu carrinho está vazio! Escolha ao menos um produto.")
        else:
            # Conta a quantidade total de fatias no carrinho
            total_fatias = sum(item["quantidade"] for item in carrinho)

            # Regra de Frete para "Outros": R$ 5,00 se pedir até 2 fatias, Grátis se pedir 3 ou mais
            if bairro_selecao.startswith("Outros"):
                if total_fatias >= 3:
                    taxa_entrega = 0.0
                else:
                    taxa_entrega = 5.0
            else:
                taxa_entrega = 0.0  # Bairros da lista principal têm frete grátis

            acrescimo_cartao = 2.0 if forma_pagamento == "Cartão (+R$ 2,00)" else 0.0

            subtotal_produtos = sum(item["subtotal"] for item in carrinho)
            valor_total = subtotal_produtos + taxa_entrega + acrescimo_cartao
            data_hora_pedido = datetime.now().strftime("%d/%m/%Y às %H:%M")

            # Montagem do relatório
            relatorio = f"*NOVO PEDIDO - ThalitaGourm*\n"
            relatorio += (
                f"----------------------------------------\n*Data/Hora:* {data_hora_pedido}\n\n"
            )
            relatorio += (
                f"*CLIENTE:*\n- Nome: {nome_cliente}\n- Tel:"
                f" {telefone_cliente}\n- End: {endereco}\n- Bairro:"
                f" {bairro_final}\n\n"
            )
            relatorio += "*ITENS DO PEDIDO:*\n"

            for item in carrinho:
                relatorio += (
                    f"- {item['quantidade']}x {item['item']} (R$"
                    f" {item['preco_unitario']:.2f} un) = R$ {item['subtotal']:.2f}\n"
                )

            if taxa_entrega == 0.0 and bairro_selecao.startswith("Outros") and total_fatias >= 3:
                relatorio += f"\n*Taxa de Entrega:* R$ 0,00 (Promoção 3+ fatias grátis! 🎉)"
            else:
                relatorio += f"\n*Taxa de Entrega:* R$ {taxa_entrega:.2f}"

            if acrescimo_cartao > 0:
                relatorio += f"\n*Taxa do Cartão:* R$ {acrescimo_cartao:.2f}"

            relatorio += f"\n\n*VALOR TOTAL:* R$ {valor_total:.2f}"
            relatorio += f"\n*Forma de Pagamento:* {forma_pagamento}"
            relatorio += (
                "\n----------------------------------------\nStatus: Pedido Realizado"
                " via Site!"
            )

            st.success("Pedido gerado com sucesso!")
            st.text_area("Confirmação do Pedido:", relatorio, height=250)

            # Link WhatsApp
            whatsapp_confeitaria = "5583987356722"
            mensagem_codificada = urllib.parse.quote(relatorio)
            link_whatsapp = (
                f"https://wa.me/{whatsapp_confeitaria}?text={mensagem_codificada}"
            )

            st.markdown(
                f"""
                <a href="{link_whatsapp}" target="_blank">
                    <button style="background-color:#25D366;color:white;padding:14px 20px;border:none;border-radius:25px;font-size:16px;font-weight:bold;cursor:pointer;width:100%;box-shadow: 0px 4px 12px rgba(37, 211, 102, 0.4);">
                        📲 Enviar Pedido no WhatsApp Agora
                    </button>
                </a>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("<br>", unsafe_allow_html=True)

            # Botão para refazer o pedido
            if st.button("🔄 Fazer Outro Pedido"):
                st.rerun()
