import streamlit as st
import json
from typing import Dict, List, Optional, Tuple
import os
import json
import PyPDF2
import openai
import requests
import io
import google.generativeai as genai 

st.markdown("<h2 style='text-align: center; color: black;'>📐Gerador de Questões de Geometria Plana</h2>", unsafe_allow_html=True)
st.write("---")
st.subheader("ℹ️ Sobre o Aplicativo")

st.write("""
Este aplicativo gera questões de Geometria personalizadas para estudantes do ensino médio.
""")

col1, col2 = st.columns(2)

with col1:
    st.write("""
    **Recursos:**
    - 4 tópicos principais de Geometria
    - 3 níveis de dificuldade
    - Escolha entre Gemini e OpenAI
    - Soluções detalhadas passo a passo
    """)

with col2:
    st.write("""
    **Tópicos disponíveis:**
    - Ângulos e Relações Métricas
    - Congruência de Triângulos  
    - Propriedades Métricas dos Triângulos
    - Quadriláteros e Polígonos Especiais
    """)

col3, col4 = st.columns(2)

with col3:
    st.subheader("🎯 Dicas de Estudo:")
    st.info("""
    **📈 Progressão Recomendada:**
    - **Fácil:** Fixar conceitos básicos
    - **Intermediário:** Aplicar teoremas
    - **Difícil:** Resolver casos complexos
    """)
        
with col4:
    st.subheader("🤖 Escolha do LLM:")
    st.info("""
    - **Gemini:** Melhor para problemas complexos
    - **OpenAI:** Mais rápido para questões gerais
    """)

col5, col6, col7 = st.columns([1,4,1])

# Define your options
options = [
    "Modelo 1 - Chat GPT", 
    "Modelo 2 - Claude"
]

# Create a container for the buttons
st.markdown("<h3 style='text-align: center; color: black;'>Selecione uma opção:</h3>", unsafe_allow_html=True)

# Initialize session state variables if they don't exist
if 'selected_option' not in st.session_state:
    st.session_state.selected_option = None

# Define button click handlers for each option
def select_option(option):
    st.session_state.selected_option = option

# Define custom CSS for button styling
st.markdown("""
<style>
    /* Default button style (light gray) */
    .stButton > button {
        background-color: #f0f2f6 !important;
        color: #31333F !important;
        border-color: #d2d6dd !important;
        width: 100%;
    }
    
    /* Selected button style (red) */
    .selected-button {
        background-color: #FF4B4B !important;
        color: white !important;
        border-color: #FF0000 !important;
        width: 100%;
        padding: 0.5rem;
        font-weight: 400;
        border-radius: 0.25rem;
        cursor: default;
        text-align: center;
        margin-bottom: 0.75rem;
    }
</style>
""", unsafe_allow_html=True)

# Create two rows of columns for the buttons
col1, col2, col3 = st.columns([3, 1, 3])

# Row 1
with col1:
    if st.session_state.selected_option == options[0]:
        # Display selected (red) button
        st.markdown(
            f"""
            <div data-testid="stButton">
                <button class="selected-button">
                    {options[0]}
                </button>
            </div>
            """, 
            unsafe_allow_html=True
        )
    else:
        # Display default (gray) button
        st.button(options[0], key="btn1", use_container_width=True, on_click=select_option, args=(options[0],))

with col3:
    if st.session_state.selected_option == options[1]:
        # Display selected (red) button
        st.markdown(
            f"""
            <div data-testid="stButton">
                <button class="selected-button">
                    {options[1]}
                </button>
            </div>
            """, 
            unsafe_allow_html=True
        )
    else:
        # Display default (gray) button
        st.button(options[1], key="btn3", use_container_width=True, on_click=select_option, args=(options[1],))

st.write("---")

if st.session_state.selected_option == "Modelo 1 - Chat GPT":
    
    # Custom CSS for better formatting
    st.markdown("""
    <style>
        .main {
            padding: 2rem;
        }
        .stAlert {
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 5px solid #ff4b4b;
        }
        .info-box {
            background-color: #e6f3ff;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 5px solid #4B8BF5;
            margin-bottom: 1rem;
        }
        h1, h2, h3 {
            color: #1E3A8A;
        }
        .katex {
            font-size: 1.1em;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.write("---")


    # ========== CONFIGURAÇÃO DE CHAVES ==========
    # Carrega a chave diretamente do Streamlit Secrets
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    #if not api_key:
    #    raise ValueError("🛑 OPENAI_API_KEY não encontrada. Verifique o .env ou as variáveis de ambiente.")

    # Cria seu client

    #client = OpenAI(api_key=api_key)

    # ========== CARREGAMENTO E CACHE DE CONTEÚDO ==========
    # Função para carregar PDF do GitHub
    def load_pdf_from_github(url: str) -> str:
        """Carrega e extrai texto de um PDF do GitHub"""
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            pdf_file = io.BytesIO(response.content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        except Exception as e:
            st.error(f"Erro ao carregar PDF: {e}")
            return ""
    
    @st.cache_data
    def load_all_topics() -> Dict[str, str]:
        """Carrega todos os tópicos dos PDFs do GitHub"""
        base = "https://github.com/JAmerico1898/geometria/raw/999ddb566bc2d6682231419750c0914e4b983b91"
        files = {
            "Ângulos e Relações Métricas": f"{base}/1.%C3%82ngulos%20e%20Rela%C3%A7%C3%B5es%20M%C3%A9tricas.pdf",
            "Congruência de Triângulos": f"{base}/2.Congru%C3%AAncia%20de%20Tri%C3%A2ngulos.pdf",
            "Propriedades Métricas dos Triângulos": f"{base}/3.Propriedades%20M%C3%A9tricas%20dos%20Tri%C3%A2ngulos.pdf",
            "Quadriláteros e Polígonos Especiais": f"{base}/4.Quadril%C3%A1teros%20e%20Pol%C3%ADgonos%20Especiais.pdf",
        }
 
       
        topics_content = {}
        for topic, url in files.items():
            with st.spinner(f"Carregando {topic}..."):
                content = load_pdf_from_github(url)
                if content:
                    topics_content[topic] = content
                else:
                    # Fallback para conteúdo estático se falhar
                    topics_content[topic] = DOCUMENTOS_CONTEXTO.get(topic, "Conteúdo não disponível")
        
        return topics_content

    # ========== FUNÇÃO DE GERAÇÃO DE QUESTÕES ==========
    def generate_questions(context: str, n: int, difficulty: str, topic: str, model: str) -> List[Dict]:
        system_msg = {
            "role": "system",
            "content": (
                "Você é um gerador de questões de Geometria Plana para alunos do ensino médio. "
                "Utilize apenas o contexto fornecido, sem recorrer a outros materiais. "
                "Para cada questão, produza um JSON com as chaves:"
                " 'enunciado', 'figure_prompt' (caso desenhe figura), 'resposta' (passo a passo)."
            )
        }
        user_msg = {
            "role": "user",
            "content": (
                f"Contexto:\n{context}\n"
                f"Gere {n} questões sobre '{topic}', nível de dificuldade '{difficulty}'. "
                "Retorne somente um array JSON válido de objetos."
            )
        }
        resp = openai.chat.completions.create(
            model="gpt-4",
            messages=[system_msg, user_msg],
            temperature=0.7,
            max_tokens=1500,
        )
        content = resp.choices[0].message.content
        try:
            questions = json.loads(content)
        except Exception:
            st.error("Falha ao interpretar a resposta do LLM.\n" + content)
            return []
        return questions


    # Carregar tópicos
    topics = load_all_topics()
    # Sidebar de parâmetros
    st.sidebar.header("Configurações")
    selected_topic = st.sidebar.selectbox("Escolha o tópico:", options=list(topics.keys()))
    num_questions = st.sidebar.slider("Número de questões:", 1, 5, 3)
    difficulty = st.sidebar.radio("Grau de dificuldade:", ["Fácil", "Intermediário", "Difícil"])
    model = st.sidebar.selectbox(
        "Modelo LLM:", ["gpt-4", "gpt-3.5-turbo"])

    if st.sidebar.button("Gerar questões"):
        with st.spinner("Gerando questões..."):
            ctx = topics[selected_topic]
            qs = generate_questions(ctx, num_questions, difficulty, selected_topic, model)
            if not qs:
                st.stop()

        # Exibição das questões
        for i, q in enumerate(qs, start=1):
            st.markdown(f"**Questão {i}:** {q.get('enunciado','')}")
            # Gabarito oculto
            with st.expander("Mostrar gabarito e passo a passo"):
                st.write(q.get('resposta',''))
    
  
    

elif st.session_state.selected_option == "Modelo 2 - Claude":
    
    # Custom CSS for better formatting
    st.markdown("""
    <style>
        .main {
            padding: 2rem;
        }
        .stAlert {
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 5px solid #ff4b4b;
        }
        .info-box {
            background-color: #e6f3ff;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 5px solid #4B8BF5;
            margin-bottom: 1rem;
        }
        h1, h2, h3 {
            color: #1E3A8A;
        }
        .katex {
            font-size: 1.1em;
        }
    </style>
    """, unsafe_allow_html=True)


    # Tentativa de importar bibliotecas de LLM
    try:
        import google.generativeai as genai
        GEMINI_AVAILABLE = True
    except ImportError:
        GEMINI_AVAILABLE = False

    try:
        import openai
        OPENAI_AVAILABLE = True
    except ImportError:
        OPENAI_AVAILABLE = False


    # Configuração dos LLMs
    @st.cache_resource
    def configure_llms() -> Tuple[Optional[object], Optional[object], Dict[str, bool]]:
        """Configura os LLMs disponíveis e retorna os modelos e status"""
        gemini_model = None
        openai_client = None
        llm_status = {"gemini": False, "openai": False}
        
        # Tentar configurar Gemini
        if GEMINI_AVAILABLE:
            try:
                gemini_api_key = st.secrets.get("GEMINI_API_KEY")
                if gemini_api_key:
                    genai.configure(api_key=gemini_api_key)
                    gemini_model = genai.GenerativeModel('gemini-2.5-pro')
                    llm_status["gemini"] = True
            except Exception as e:
                st.warning(f"⚠️ Erro ao configurar Gemini: {e}")
        
        # Tentar configurar OpenAI
        if OPENAI_AVAILABLE:
            try:
                openai_api_key = st.secrets.get("OPENAI_API_KEY")
                if openai_api_key:
                    openai_client = openai.OpenAI(api_key=openai_api_key)
                    llm_status["openai"] = True
            except Exception as e:
                st.warning(f"⚠️ Erro ao configurar OpenAI: {e}")
        
        # Verificar se pelo menos um LLM está disponível
        if not any(llm_status.values()):
            st.error("❌ Nenhum LLM configurado. Verifique suas credenciais em st.secrets.")
            st.info("""
            Configure pelo menos uma das opções no arquivo `.streamlit/secrets.toml`:
            - GEMINI_API_KEY = "sua_chave_do_gemini"
            - OPENAI_API_KEY = "sua_chave_do_openai"
            """)
            st.stop()
        
        return gemini_model, openai_client, llm_status

    gemini_model, openai_client, llm_status = configure_llms()


    # ========== CARREGAMENTO E CACHE DE CONTEÚDO ==========
    # Função para carregar PDF do GitHub
    def load_pdf_from_github(url: str) -> str:
        """Carrega e extrai texto de um PDF do GitHub"""
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            pdf_file = io.BytesIO(response.content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        except Exception as e:
            st.error(f"Erro ao carregar PDF: {e}")
            return ""
    
    @st.cache_data
    def load_all_topics() -> Dict[str, str]:
        """Carrega todos os tópicos dos PDFs do GitHub"""
        base = "https://github.com/JAmerico1898/geometria/raw/1f64238760bea9594b7ac886266e8abf8e7a6836"
        files = {
            "Ângulos e Relações Métricas": f"{base}/1.%C3%82ngulos%20e%20Rela%C3%A7%C3%B5es%20M%C3%A9tricas.pdf",
            "Congruência de Triângulos": f"{base}/2.Congru%C3%AAncia%20de%20Tri%C3%A2ngulos.pdf",
            "Propriedades Métricas dos Triângulos": f"{base}/3.Propriedades%20M%C3%A9tricas%20dos%20Tri%C3%A2ngulos.pdf",
            "Quadriláteros e Polígonos Especiais": f"{base}/4.Quadril%C3%A1teros%20e%20Pol%C3%ADgonos%20Especiais.pdf",
        }
        
        topics_content = {}
        for topic, url in files.items():
            with st.spinner(f"Carregando {topic}..."):
                content = load_pdf_from_github(url)
                if content:
                    topics_content[topic] = content
                else:
                    # Fallback para conteúdo estático se falhar
                    topics_content[topic] = DOCUMENTOS_CONTEXTO.get(topic, "Conteúdo não disponível")
        
        return topics_content

    # Carregar conteúdo dos PDFs
    try:
        DOCUMENTOS_CONTEXTO = load_all_topics()
        st.success("✅ PDFs carregados do GitHub com sucesso!")
    except Exception as e:
        st.warning(f"⚠️ Erro ao carregar PDFs: {e}. Usando conteúdo estático.")
        # Fallback para conteúdo estático original


    # Conteúdo dos documentos (extraído dos PDFs fornecidos)
    DOCUMENTOS_CONTEXTO = {
        "Ângulos e Relações Métricas": """
        Tipos de Ângulos:
        - Nulo: 0°
        - Agudo: 0° < θ < 90°
        - Reto: 90°
        - Obtuso: 90° < θ < 180°
        - Raso: 180°
        - Côncavo/Reentrante: 180° < θ < 360°
        - Completo: 360°
        
        Bissetriz: semirreta que divide o ângulo em duas partes congruentes.
        Teorema da bissetriz interna: BD/DC = AB/AC
        
        Ângulos relacionados:
        - Opostos pelo vértice: sempre congruentes
        - Complementares: soma = 90°
        - Suplementares: soma = 180°
        
        Soma dos Ângulos Internos de Polígonos:
        - Fórmula geral: Σ Âng. Internos = (n-2) × 180°
        - Ângulos externos: Σ Âng. Externos = 360°
        - Ângulo interno regular: α = (n-2)180°/n
        - Ângulo externo regular: ε = 360°/n
        """,
        
        "Congruência de Triângulos": """
        Critérios de Congruência:
        - LLL/SSS: três lados correspondentes iguais
        - LAL/SAS: dois lados e ângulo entre eles
        - ALA/ASA: dois ângulos e lado entre eles
        - AAL/AAS: dois ângulos e lado não incluído
        - LLR/RHS: triângulo retângulo com hipotenusa e cateto
        
        Não são critérios válidos: SSA e AAA
        
        Construções clássicas com régua e compasso para cada critério.
        Aplicações: justificar construções geométricas, garantir igualdade de segmentos/ângulos.
        """,
        
        "Propriedades Métricas dos Triângulos": """
        Teorema de Pitágoras:
        - Enunciado: a² + b² = c²
        - Conversa: se a² + b² = c², então é retângulo
        - Números pitagóricos: (3,4,5), (5,12,13), (8,15,17)
        - Extensões: triângulo obtuso a² + b² < c²
        
        Teorema das Medianas:
        - ma² = (2b² + 2c² - a²)/4
        - Baricentro divide mediana na razão 2:1
        
        Pontos Notáveis:
        - Incentro (I): interseção das bissetrizes internas
        - Circuncentro (O): interseção das mediatrizes
        - Ortocentro (H): interseção das alturas
        - Baricentro (G): interseção das medianas
        - Reta de Euler: O, G, H são colineares
        """,
        
        "Quadriláteros e Polígonos Especiais": """
        Paralelogramos:
        - Lados opostos paralelos e congruentes
        - Ângulos opostos congruentes
        - Diagonais bissectam-se
        - Área: A = b×h ou |u⃗ × v⃗|
        
        Trapézios:
        - Pelo menos um par de lados paralelos
        - Área: A = (a+b)h/2
        - Segmento médio paralelo às bases
        
        Losangos:
        - Paralelogramo com todos os lados iguais
        - Diagonais perpendiculares e bissectam-se
        - Área: A = d₁×d₂/2
        
        Deltoides (Kites):
        - Dois pares de lados adjacentes congruentes
        - Uma diagonal é eixo de simetria
        - Área: A = d₁×d₂/2
        """
    }

    def gerar_questoes_gemini(topico: str, num_questoes: int, dificuldade: str, contexto: str) -> List[Dict]:
        """Gera questões usando o Gemini"""
        prompt = f"""
        Você é um professor experiente de Geometria. Com base no contexto fornecido sobre "{topico}", 
        crie {num_questoes} questão(ões) de nível {dificuldade}.
        
        CONTEXTO:
        {contexto}
        
        INSTRUÇÕES:
        - Nível fácil: conceitos básicos, cálculos simples
        - Nível intermediário: aplicação de teoremas, problemas de múltiplas etapas
        - Nível difícil: problemas complexos, demonstrações, casos especiais
        
        Para cada questão, forneça:
        1. Enunciado claro e completo (com todas as informações necessárias)
        2. Solução completa passo a passo
        3. Resposta final
        
        Responda APENAS no formato JSON válido:
        {{
            "questoes": [
                {{
                    "enunciado": "...",
                    "solucao_passo_a_passo": ["Passo 1: ...", "Passo 2: ..."],
                    "resposta_final": "..."
                }}
            ]
        }}
        """
        
        try:
            response = gemini_model.generate_content(prompt)
            texto_limpo = response.text.strip()
            if texto_limpo.startswith("```json"):
                texto_limpo = texto_limpo[7:]
            if texto_limpo.endswith("```"):
                texto_limpo = texto_limpo[:-3]
            
            questoes_data = json.loads(texto_limpo)
            return questoes_data["questoes"]
        except Exception as e:
            st.error(f"Erro ao gerar questões com Gemini: {e}")
            return []

    def gerar_questoes_openai(topico: str, num_questoes: int, dificuldade: str, contexto: str) -> List[Dict]:
        """Gera questões usando o OpenAI"""
        prompt = f"""
        Você é um professor experiente de Geometria. Com base no contexto fornecido sobre "{topico}", 
        crie {num_questoes} questão(ões) de nível {dificuldade}.
        
        CONTEXTO:
        {contexto}
        
        INSTRUÇÕES:
        - Nível fácil: conceitos básicos, cálculos simples
        - Nível intermediário: aplicação de teoremas, problemas de múltiplas etapas
        - Nível difícil: problemas complexos, demonstrações, casos especiais
        
        Para cada questão, forneça:
        1. Enunciado claro e completo (com todas as informações necessárias)
        2. Solução completa passo a passo
        3. Resposta final
        
        Responda APENAS no formato JSON válido:
        {{
            "questoes": [
                {{
                    "enunciado": "...",
                    "solucao_passo_a_passo": ["Passo 1: ...", "Passo 2: ..."],
                    "resposta_final": "..."
                }}
            ]
        }}
        """
        
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Você é um professor experiente de Geometria que sempre responde em formato JSON válido."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            texto_resposta = response.choices[0].message.content.strip()
            if texto_resposta.startswith("```json"):
                texto_resposta = texto_resposta[7:]
            if texto_resposta.endswith("```"):
                texto_resposta = texto_resposta[:-3]
            
            questoes_data = json.loads(texto_resposta)
            return questoes_data["questoes"]
        except Exception as e:
            st.error(f"Erro ao gerar questões com OpenAI: {e}")
            return []

    def gerar_questoes(topico: str, num_questoes: int, dificuldade: str, llm_escolhido: str) -> List[Dict]:
        """Gera questões usando o LLM escolhido pelo usuário"""
        contexto = DOCUMENTOS_CONTEXTO[topico]
        
        if llm_escolhido == "gemini" and llm_status["gemini"]:
            return gerar_questoes_gemini(topico, num_questoes, dificuldade, contexto)
        elif llm_escolhido == "openai" and llm_status["openai"]:
            return gerar_questoes_openai(topico, num_questoes, dificuldade, contexto)
        else:
            st.error(f"LLM {llm_escolhido} não está disponível ou configurado")
            return []

    # Interface principal
    #col1, col2 = st.columns([1, 2])

    # Informações adicionais
    with st.sidebar:
        
        st.subheader("🤖 Status dos LLMs")
        
        # Status do Gemini
        if llm_status["gemini"]:
            st.success("✅ **Google Gemini 2.5 Pro** - Disponível")
        else:
            st.error("❌ **Google Gemini** - Não configurado")
        
        # Status do OpenAI
        if llm_status["openai"]:
            st.success("✅ **OpenAI GPT-4o-mini** - Disponível")
        else:
            st.error("❌ **OpenAI** - Não configurado")
        
        st.subheader("⚙️ Configurações")
        
        # Seleção do LLM
        llms_disponiveis = []
        opcoes_llm = {}
        
        if llm_status["gemini"]:
            llms_disponiveis.append("Google Gemini 2.5 Pro")
            opcoes_llm["Google Gemini 2.5 Pro"] = "gemini"
        
        if llm_status["openai"]:
            llms_disponiveis.append("OpenAI GPT-4o-mini")
            opcoes_llm["OpenAI GPT-4o-mini"] = "openai"
        
        if llms_disponiveis:
            llm_selecionado = st.selectbox(
                "🤖 Escolha o LLM:",
                llms_disponiveis,
                index=0
            )
            llm_escolhido = opcoes_llm[llm_selecionado]
            
        else:
            st.error("Nenhum LLM disponível")
            st.stop()
        
        # Seleção do tópico
        topico = st.selectbox(
            "📚 Escolha o tópico:",
            list(DOCUMENTOS_CONTEXTO.keys()),
            index=0
        )
        
        # Número de questões
        num_questoes = st.slider(
            "📝 Número de questões:",
            min_value=1,
            max_value=5,
            value=2
        )
        
        # Dificuldade
        dificuldade = st.selectbox(
            "🎯 Grau de dificuldade:",
            ["Fácil", "Intermediário", "Difícil"],
            index=1
        )
        
        # Botão para gerar questões
        gerar = st.button("🚀 Gerar Questões", type="primary", use_container_width=True)

        st.markdown("---")

        # Estatísticas de uso (se houver questões geradas)
        if hasattr(st.session_state, 'questoes'):
            st.subheader("📊 Estatísticas da Sessão")
            total_questoes = len(st.session_state.questoes)
            llm_usado = st.session_state.get('llm_usado', 'N/A')
            
            col_stat1, col_stat2 = st.columns(2)
            with col_stat1:
                st.markdown(
                    f"""**Questões Geradas**  
                    <span style="font-size:1.25rem">{total_questoes}</span>""",
                    unsafe_allow_html=True
                )
            with col_stat2:
                st.markdown(
                    f"""**LLM Utilizado**  
                    <span style="font-size:1.25rem">
                    {llm_usado.split()[0] if llm_usado!='N/A' else 'N/A'}
                    </span>""",
                    unsafe_allow_html=True
                )

















                
    st.markdown(
        "<h3 style='text-align: center;'>📋 Questões Geradas</h3>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<h6 style='text-align: center;'>(Não esqueça de clicar na barra lateral)</h3>",
        unsafe_allow_html=True
    )
    
    if gerar:
        with st.spinner(f"Gerando questões com {llm_selecionado}..."):
            questoes = gerar_questoes(topico, num_questoes, dificuldade.lower(), llm_escolhido)
            
            if questoes:
                st.session_state.questoes = questoes
                st.session_state.llm_usado = llm_selecionado
                st.success(f"✅ {len(questoes)} questão(ões) gerada(s) com sucesso usando {llm_selecionado}!")
            else:
                st.error("❌ Erro ao gerar questões. Tente novamente.")

    # Exibir questões
    if hasattr(st.session_state, 'questoes') and st.session_state.questoes:
        st.markdown("---")
        
        # Mostrar informações sobre as questões geradas
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.info(f"🤖 **Gerado por:** {st.session_state.get('llm_usado', 'LLM')}")
        with col_info2:
            st.info(f"📊 **Total:** {len(st.session_state.questoes)} questão(ões)")
        
        for i, questao in enumerate(st.session_state.questoes, 1):
            st.subheader(f"📝 Questão {i}")
            st.write(questao["enunciado"])
            
            # Gabarito expansível
            with st.expander(f"📖 Gabarito - Questão {i}"):
                st.write("**Solução passo a passo:**")
                for j, passo in enumerate(questao["solucao_passo_a_passo"], 1):
                    st.write(f"**Passo {j}:** {passo}")
                
                st.write("**Resposta final:**")
                st.success(questao["resposta_final"])
            
            st.markdown("---")


    # Footer
    st.markdown("---")
    llm_usado = st.session_state.get('llm_usado', 'LLM')
    st.markdown(
        f"<div style='text-align: center; color: gray;'>"
        f"📐 Gerador de Questões de Geometria Plana<br>"
        f"Desenvolvido com Streamlit<br>"
        f"Última geração: {llm_usado}"
        "</div>",
        unsafe_allow_html=True
    )
