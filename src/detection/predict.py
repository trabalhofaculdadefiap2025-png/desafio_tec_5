import os
from inference_sdk import InferenceHTTPClient
from PIL import Image, ImageDraw
from dotenv import load_dotenv

load_dotenv()


def extrair_predicoes_recursivo(dados):
    """Busca a lista de predições dentro do JSON do Workflow de forma segura."""
    if isinstance(dados, dict):
        if "predictions" in dados and isinstance(dados["predictions"], list):
            return dados["predictions"]
        for valor in dados.values():
            resultado = extrair_predicoes_recursivo(valor)
            if resultado:
                return resultado
    elif isinstance(dados, list):
        for item in dados:
            resultado = extrair_predicoes_recursivo(item)
            if resultado:
                return resultado
    return []


def rodar_deteccao_yolo(caminho_imagem: str):
    """
    Envia a imagem para o endpoint Serverless do Roboflow via Inference SDK,
    desenha as caixas delimitadoras nos componentes e retorna a lista encontrada.
    """
    api_key = os.getenv("ROBOFLOW_API_KEY")
    if not api_key:
        print("[ERRO] ROBOFLOW_API_KEY não configurada no arquivo .env")
        return [], None

    try:
        # Inicializa o cliente HTTP oficial do Roboflow Serverless
        client = InferenceHTTPClient(
            api_url="https://serverless.roboflow.com",
            api_key=api_key
        )

        # Executa o workflow exatamente como configurado na sua conta
        resultado_api = client.run_workflow(
            workspace_name="alessandra23333-gmail-com",
            workflow_id="aws-icon-detector-improved-fmnjg",
            images={"image": caminho_imagem},
            use_cache=True
        )

        componentes_detectados = set()

        # Abre a imagem original para desenhar as marcações visuais
        imagem_pil = Image.open(caminho_imagem)
        canva_desenho = ImageDraw.Draw(imagem_pil)

        # Localiza as caixas de detecção no retorno do servidor
        predicoes = extrair_predicoes_recursivo(resultado_api)

        for pred in predicoes:
            # Captura a classe detectada (ex: aws-icon)
            classe_original = pred.get("class", "Componente AWS")
            componentes_detectados.add(classe_original)

            # Coordenadas centrais fornecidas pelo Roboflow
            x_centro = pred.get("x", 0)
            y_centro = pred.get("y", 0)
            largura = pred.get("width", 0)
            altura = pred.get("height", 0)

            # Converte o centro/tamanho para pontos de quinas (coordenadas de caixa)
            esquerda = x_centro - (largura / 2)
            topo = y_centro - (altura / 2)
            direita = x_centro + (largura / 2)
            inferior = y_centro + (altura / 2)

            # Desenha o quadrado vermelho ao redor do componente detectado
            canva_desenho.rectangle([esquerda, topo, direita, inferior], outline="red", width=3)

        # Salva o resultado final processado para exibição no Streamlit
        caminho_saida_anotada = "imagem_analisada.png"
        imagem_pil.save(caminho_saida_anotada)

        # Retorna a lista de componentes e o caminho do arquivo gerado
        return list(componentes_detectados), caminho_saida_anotada

    except Exception as e:
        print(f"[ERRO DE INFERÊNCIA]: {str(e)}")
        return [], None