# 🛡️ ThreatMod AI - Automação de Modelagem de Ameaças (STRIDE)

> **Tech Challenge - Fase 5 | Pós-Tech FIAP**  
> *Plataforma inteligente de análise de riscos de arquitetura de nuvem utilizando Visão Computacional e Inteligência Artificial Generativa Multimodal.*

---

## 📌 Sobre o Projeto

O **ThreatMod AI** é uma solução voltada para ecossistemas **DevSecOps** que automatiza a identificação de componentes de infraestrutura em nuvem (AWS/Azure) a partir de diagramas de arquitetura e gera relatórios completos de modelagem de ameaças baseados no framework **STRIDE**.

A aplicação reduz o tempo de análise de segurança de dias para **poucos segundos**, combinando a detecção visual de ativos com o raciocínio analítico de IA para sugerir contramedidas técnicas acionáveis.

---

## 🧠 Arquitetura Híbrida de IA

A solução opera com uma **Arquitetura Composta de IA** em pipeline:

1. **Camada de Visão Computacional (YOLOv11 - Serverless):**
   * Processa o diagrama enviado e realiza a detecção dos ícones de infraestrutura.
   * Consumido via **Roboflow Inference SDK**, gerando as caixas delimitadoras (*bounding boxes*) na imagem.
2. **Camada Cognitiva de Segurança (Gemini 2.5 Pro - Vertex AI):**
   * Recebe o contexto visual e os ativos identificados.
   * Aplica a metodologia **STRIDE** (*Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege*).
3. **Frontend Reativo (Streamlit):**
   * Apresenta o diagrama anotado e o relatório técnico formatado em tempo real.

---

## 📂 Estrutura do Projeto

```text
tech_5/
├── .env.example                 # Modelo de variáveis de ambiente
├── .gitignore                   # Arquivos ignorados pelo Git
├── Dockerfile                   # Configuração de containerização da aplicação
├── app.py                       # Interface web e orquestrador Streamlit
├── requirements.txt             # Dependências do projeto Python
└── src/                         # Módulos do código-fonte
    ├── detection/
    │   └── predict.py           # Cliente da API Serverless do Roboflow (YOLOv11)
    ├── reporting/
    │   └── generator.py         # Integração com Google Cloud Vertex AI (Gemini 2.5 Pro)
    └── threat_modeling/         # Lógica do framework STRIDE