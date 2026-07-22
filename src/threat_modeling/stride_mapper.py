import os
import vertexai
from vertexai.generative_models import GenerativeModel
from dotenv import load_dotenv

# Garanta que as variáveis do .env sejam carregadas no escopo do arquivo
load_dotenv()


def inicializar_gemini():
    """
    Inicializa o Vertex AI com diagnóstico cirúrgico de arquivos para o Windows.
    """
    project_id = os.getenv("GCP_PROJECT_ID")
    location = os.getenv("GCP_LOCATION", "us-central1")
    cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    if not project_id:
        raise ValueError("[ERRO] A variável GCP_PROJECT_ID não foi encontrada no seu arquivo .env")

    if cred_path:
        cred_path = cred_path.strip('"').strip("'")

        # Calcula a raiz do projeto estritamente a partir da localização deste arquivo
        caminho_deste_script = os.path.abspath(__file__)
        raiz_projeto = os.path.dirname(os.path.dirname(os.path.dirname(caminho_deste_script)))

        if not os.path.isabs(cred_path):
            cred_path_absoluto = os.path.join(raiz_projeto, cred_path)

            if not os.path.exists(cred_path_absoluto):
                cred_path_absoluto = os.path.abspath(os.path.join(os.getcwd(), cred_path))

            cred_path = cred_path_absoluto

        # 🔍 DIAGNÓSTICO: Se o arquivo não existe, vamos listar o que tem na pasta
        if not os.path.exists(cred_path):
            try:
                arquivos_visiveis = os.listdir(raiz_projeto)
            except Exception:
                arquivos_visiveis = os.listdir(os.getcwd())

            raise FileNotFoundError(
                f"\n\n[ERRO CRÍTICO] Arquivo de credenciais NÃO encontrado!\n"
                f"O sistema buscou exatamente por: {cred_path}\n\n"
                f"📂 Arquivos que o Python REALMENTE está vendo na raiz do projeto:\n"
                f"{arquivos_visiveis}\n\n"
                f"Compare o nome do seu arquivo com a lista acima para ver se há extensões ocultas (como .txt) ou erros de digitação."
            )

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred_path

    vertexai.init(project=project_id, location=location)


def gerar_analise_stride_gemini(componentes_detectados: list) -> str:
    """Envia a lista de componentes detectados para o Gemini 2.5 Pro gerar o relatório de ameaças"""
    try:
        inicializar_gemini()

        model = GenerativeModel("gemini-2.5-pro")

        prompt = f"""
        Você é um Engenheiro de Segurança de Sistemas Sênior especialista na metodologia STRIDE.
        A nossa IA de Visão Computacional analisou um diagrama de arquitetura e detectou os seguintes componentes:
        {", ".join(componentes_detectados)}

        Com base nessa lista, gere um Relatório de Modelagem de Ameaças detalhado em formato Markdown.
        Para cada componente, identifique as ameaças aplicáveis do STRIDE e sugira contramedidas específicas e acionáveis.
        Seja técnico, direto e profissional.
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Erro ao chamar o fallback do Gemini via Vertex AI: {str(e)}"