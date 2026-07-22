import streamlit as st
from PIL import Image
from src.threat_modeling.stride_mapper import gerar_analise_stride_gemini

# Configuração da página do Streamlit
st.set_page_config(
    page_title="FIAP - Software Security Threat Modeler",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ IA para Modelagem de Ameaças Automática")
st.markdown("""
Esta aplicação utiliza Inteligência Artificial para interpretar diagramas de arquitetura, 
identificar componentes e gerar relatórios de ameaças baseados na metodologia **STRIDE**.
""")

st.sidebar.header("Configurações do MVP")

# 1. Upload do Diagrama de Arquitetura
uploaded_file = st.sidebar.file_uploader(
    "Selecione a imagem do diagrama de arquitetura",
    type=["png", "jpg", "jpeg"]
)

# 2. Seleção manual de componentes (Simulação provisória enquanto o YOLO não entra em ação)
st.sidebar.subheader("Detecção de Componentes")
componentes_disponiveis = [
    "Usuário (Client)",
    "API Gateway",
    "Servidor de Aplicação (Backend)",
    "Banco de Dados (Database)",
    "Load Balancer",
    "Firewall (WAF)"
]

componentes_selecionados = st.sidebar.multiselect(
    "Selecione os componentes para simular a detecção da IA:",
    options=componentes_disponiveis,
    default=["Usuário (Client)", "API Gateway", "Banco de Dados (Database)"]
)

# Layout principal dividido em duas colunas
col1, col2 = st.columns([1, 1])

with col1:
    st.header("🖼️ Diagrama de Arquitetura")
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Diagrama enviado para análise", use_column_width=True)
    else:
        st.info("Aguardando o upload de uma imagem de arquitetura para exibição.")

with col2:
    st.header("📋 Relatório de Ameaças STRIDE")

    # Botão para disparar a análise do Gemini
    if st.button("Gerar Relatório de Segurança 🚀"):
        if not componentes_selecionados:
            st.warning("Por favor, selecione ao menos um componente na barra lateral para analisar.")
        else:
            with st.spinner("O Gemini 2.5 Pro está analisando os componentes e mapeando as ameaças..."):
                # Dispara a chamada para a nossa função na pasta src/
                relatorio_final = gerar_analise_stride_gemini(componentes_selecionados)

                # Exibe o resultado formatado em Markdown na tela
                st.markdown(relatorio_final)