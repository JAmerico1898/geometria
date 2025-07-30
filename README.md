# 📐 Gerador de Questões de Geometria

Um aplicativo Streamlit inteligente que gera questões personalizadas de Geometria para estudantes do ensino médio, utilizando inteligência artificial (Gemini ou OpenAI) para criar exercícios contextualizados e soluções detalhadas.

## 🎯 Funcionalidades

- **🤖 Duplo Suporte de IA**: Escolha entre Google Gemini ou OpenAI
- **📚 4 Tópicos Fundamentais**: Conteúdo completo baseado em material didático
- **🎚️ 3 Níveis de Dificuldade**: Fácil, Intermediário e Difícil
- **📝 Questões Variadas**: De 1 a 5 questões por sessão
- **📖 Gabaritos Expandíveis**: Soluções passo a passo ocultas
- **🎨 Interface Intuitiva**: Design limpo e focado no aprendizado

## 📋 Tópicos Disponíveis

### 1. Ângulos e Relações Métricas
- Tipos de ângulos (agudo, obtuso, reto, etc.)
- Bissetrizes e suas propriedades
- Ângulos complementares e suplementares
- Soma de ângulos internos e externos de polígonos

### 2. Congruência de Triângulos
- Critérios de congruência (LLL, LAL, ALA, AAL, LLR)
- Construções clássicas com régua e compasso
- Aplicações práticas e demonstrações

### 3. Propriedades Métricas dos Triângulos
- Teorema de Pitágoras e extensões
- Teorema das Medianas
- Pontos notáveis (baricentro, incentro, circuncentro, ortocentro)
- Reta de Euler

### 4. Quadriláteros e Polígonos Especiais
- Paralelogramos e suas propriedades
- Trapézios e suas características
- Losangos e deltoides
- Fórmulas de área e perímetro

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.8 ou superior
- Conta no Google AI (Gemini) ou OpenAI
- Chaves de API válidas

### 1. Clone o Repositório
```bash
git clone <url-do-repositorio>
cd gerador-questoes-geometria
```

### 2. Instale as Dependências
```bash
pip install -r requirements.txt
```

### 3. Configure as Credenciais
Crie o arquivo `.streamlit/secrets.toml` na raiz do projeto:

```toml
# Configure pelo menos uma das opções:

# Google Gemini (recomendado para matemática)
GEMINI_API_KEY = "sua_chave_api_do_gemini_aqui"

# OpenAI (alternativa eficiente)
OPENAI_API_KEY = "sua_chave_api_do_openai_aqui"
```

### 4. Execute o Aplicativo
```bash
streamlit run app.py
```

O aplicativo estará disponível em `http://localhost:8501`

## 🔑 Obtendo Chaves de API

### Google Gemini
1. Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Faça login com sua conta Google
3. Clique em "Create API Key"
4. Copie a chave gerada

### OpenAI
1. Acesse [OpenAI Platform](https://platform.openai.com/api-keys)
2. Faça login em sua conta
3. Clique em "Create new secret key"
4. Copie a chave gerada

## 🎮 Como Usar

1. **Escolha o LLM**: Selecione entre Gemini ou OpenAI
2. **Selecione o Tópico**: Escolha um dos 4 tópicos disponíveis
3. **Configure Parâmetros**: 
   - Número de questões (1-5)
   - Nível de dificuldade (Fácil/Intermediário/Difícil)
4. **Gere as Questões**: Clique em "🚀 Gerar Questões"
5. **Estude**: Tente resolver e depois confira o gabarito

## 📊 Estrutura do Projeto

```
gerador-questoes-geometria/
├── app.py                 # Aplicativo principal
├── requirements.txt       # Dependências
├── README.md             # Este arquivo
├── .streamlit/
│   └── secrets.toml      # Credenciais (criar manualmente)
└── docs/                 # Documentação adicional
```

## 🎓 Níveis de Dificuldade

### 🟢 Fácil
- Conceitos básicos e definições
- Cálculos simples e diretos
- Aplicação de fórmulas fundamentais

### 🟡 Intermediário
- Aplicação de teoremas
- Problemas de múltiplas etapas
- Combinação de conceitos

### 🔴 Difícil
- Problemas complexos e demonstrações
- Casos especiais e exceções
- Análise crítica e síntese

## 🤖 Comparação dos LLMs

| Característica | Google Gemini | OpenAI GPT-4o-mini |
|---|---|---|
| **Matemática** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Velocidade** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Custo** | Gratuito (cota) | Pago por uso |
| **Complexidade** | Problemas avançados | Questões gerais |
| **Recomendação** | Geometria complexa | Uso frequente |

## 🛠️ Desenvolvimento

### Tecnologias Utilizadas
- **Frontend**: Streamlit
- **IA**: Google Gemini API / OpenAI API
- **Linguagem**: Python 3.8+

### Contribuindo
1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📈 Roadmap

- [ ] **Exportação de Questões**: PDF, Word, LaTeX
- [ ] **Banco de Questões**: Salvar questões favoritas
- [ ] **Estatísticas de Desempenho**: Acompanhar progresso
- [ ] **Modo Professor**: Criar turmas e acompanhar alunos
- [ ] **Figuras Geométricas**: Opção de incluir diagramas
- [ ] **Outros Assuntos**: Álgebra, Trigonometria, etc.

## ❓ FAQ

### **P: Posso usar apenas uma das APIs?**
R: Sim! Configure apenas a API que preferir no `secrets.toml`.

### **P: As questões são sempre diferentes?**
R: Sim, a IA gera questões únicas a cada execução.

### **P: Há limite de questões por dia?**
R: Depende dos limites da API escolhida (Gemini tem cota gratuita, OpenAI é pago por uso).

### **P: Posso usar offline?**
R: Não, o aplicativo precisa de conexão com internet para acessar as APIs.

### **P: Como relatar bugs?**
R: Abra uma issue no repositório do projeto.

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- Material didático baseado em conteúdo de Geometria para ensino médio
- Comunidade Streamlit pela excelente framework
- Google e OpenAI pelas APIs de IA

## 📞 Suporte

- **Issues**: [GitHub Issues](link-para-issues)
- **Documentação**: [Wiki do Projeto](link-para-wiki)
- **Contato**: [email-do-desenvolvedor]

---

**Desenvolvido com ❤️ para estudantes de Geometria**

*Transformando o aprendizado de matemática com inteligência artificial*
