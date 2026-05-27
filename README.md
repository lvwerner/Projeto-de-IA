📦 FastLog - Sistema Integrado de Logística (RAG + Voz + BI)
Projeto desenvolvido como requisito do Seminário de Inteligência Artificial para solucionar o problema de alto volume de atendimento em consultas de status de entregas. O FastLog atua como uma "Torre de Controle" gerencial e um "Assistente de Atendimento" autônomo, cumprindo integralmente o fluxo exigido: Áudio → Texto → RAG → Áudio.

✨ Principais Funcionalidades e Arquitetura
O sistema foi arquitetado simulando um ambiente real de produção, separando as visões do cliente e do gestor usando o menu lateral (Sidebar) e a memória de sessão (session_state):

👤 1. Portal do Cliente (Frontend)
Atendimento Multimodal: Suporte para entrada de consultas via gravação de áudio (transcrição via Whisper) ou texto.

Respostas em Voz (TTS): A IA gera respostas em áudio dinamicamente, permitindo que o sistema converse com o usuário. Inclui opção de download em formato .mp3.

Assistente RAG Seguro: Chatbot integrado (Llama 3) que lê os dados operacionais da empresa em tempo real, eliminando totalmente o risco de alucinações (a IA só responde sobre pacotes que realmente existem na base).

🏢 2. Torre de Controle (Backoffice)
Business Intelligence (BI): Gráficos de distribuição e métricas de desempenho (Entregues, Atrasadas, Total) que reagem instantaneamente.

Edição ao Vivo: Interface de planilha interativa (st.data_editor) para atualizar ou adicionar status logísticos. O assistente de voz do cliente aprende a nova informação no mesmo segundo.

Gerenciamento de Base: Opção de "Limpar Tabela" para zerar o banco de dados e iniciar novos expedientes logísticos, salvando as alterações diretamente no arquivo .csv.

🛠️ Tecnologias Utilizadas
Linguagem: Python 3.10+

Interface e painel de controle: Streamlit

Processamento de Dados: Pandas

Manipulação de Áudio: gTTS (Google Text-to-Speech)

Inteligência Artificial: Groq Cloud API

Transcrição de Voz: whisper-large-v3

Raciocínio RAG: llama-3.3-70b-versatile

🚀 Guia de Instalação (Ambiente Virtual)
Para evitar erros de permissão de administrador ou conflitos de bibliotecas no Windows (comum em redes acadêmicas e corporativas), este projeto deve ser executado utilizando um Ambiente Virtual (venv).

1. Configurando a Chave de API
Abra o arquivo fastlog_texto.py.

Substitua a string "SUA_CHAVE_GSK_AQUI" na variável API_KEY pela sua chave gerada na Groq.

2. Configuração do Ambiente e Dependências
Abra o terminal (PowerShell ou CMD) dentro da pasta do projeto e execute os comandos abaixo na ordem:

A) Criar o ambiente virtual:
PowerShell

python -m venv venv

B) Ativar o ambiente virtual:
PowerShell

.\venv\Scripts\activate

(Confirme se a palavra (venv) apareceu no início da linha do seu terminal).

C) Instale as bibliotecas:
PowerShell

pip install streamlit pandas requests gTTS

3. Executando o Sistema
Com o ambiente ativado, inicie a aplicação utilizando o prefixo seguro do Python:
PowerShell

python -m streamlit run fastlog_texto.py

A interface abrirá automaticamente no seu navegador padrão (http://localhost:8501).

💡 Guia de Demonstração para a Banca Avaliadora
Para demonstrar a eficácia do sistema durante a apresentação, siga este roteiro (O Efeito UAU):

1. Preparando o Terreno (Iniciando Zerado):

Entre na aba "🏢 Torre de Controle Logístico".

Clique no botão "🗑️ Limpar Tabela". Mostre que o sistema inicia o dia limpo.

Adicione um pacote novo direto na tabela (Ex: Código 123, Cliente Banca Avaliadora, Status Em trânsito, Local Universidade).

2. O Fluxo Completo (Áudio → RAG → Áudio):

Mude para a aba "👤 Área do Cliente".

Clique no microfone e pergunte: "Qual a situação do pacote 123?"

Mostre ao público o sistema transcrevendo a voz, cruzando com a tabela que você acabou de preencher e gerando a resposta falada.

3. Validação Anti-Alucinação:

Pergunte por um pacote que não está na tabela (Ex: "Onde está o pedido 999?").

O sistema pedirá desculpas e informará que não localizou, provando que a Inteligência Artificial está domada e conectada estritamente aos dados corporativos.