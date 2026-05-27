import streamlit as st
import pandas as pd
import requests
import os
import io
from gtts import gTTS

# ==========================================
# 1. CONFIGURAÇÃO DA TELA
# ==========================================
st.set_page_config(page_title="FastLog - Sistema Integrado", page_icon="📦", layout="wide")

# NUNCA DEIXE SUA CHAVE REAL AQUI AO ENVIAR PARA O GITHUB!
API_KEY = "COLOQUE_CHAVE_KEY_AQUI" 

# ==========================================
# 2. CARREGAMENTO DE DADOS E MEMÓRIA
# ==========================================
colunas_padrao = ['codigo_rastreio', 'cliente', 'status', 'local_atual', 'previsao_entrega', 'observacao']

if "dados_logistica" not in st.session_state:
    if os.path.exists("entregas.csv"):
        df = pd.read_csv("entregas.csv")
        if df.empty:
            df = pd.DataFrame(columns=colunas_padrao)
        st.session_state.dados_logistica = df
    else:
        st.session_state.dados_logistica = pd.DataFrame(columns=colunas_padrao)

# ==========================================
# 3. MOTORES DE IA E VOZ
# ==========================================
def transcrever_audio_groq(audio_bytes):
    url = "https://api.groq.com/openai/v1/audio/transcriptions"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    files = {"file": ("audio.wav", audio_bytes, "audio/wav")}
    data = {"model": "whisper-large-v3"}
    try:
        response = requests.post(url, headers=headers, files=files, data=data)
        return response.json().get('text', "Não consegui transcrever o áudio.")
    except Exception as e:
        return f"Erro na transcrição: {e}"

def chamar_groq(sistema_prompt, pergunta_usuario):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": sistema_prompt},
            {"role": "user", "content": pergunta_usuario}
        ],
        "temperature": 0 
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Erro na IA: {e}"

def gerar_audio_resposta(texto):
    try:
        tts = gTTS(text=texto, lang='pt')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp
    except Exception as e:
        return None

# ==========================================
# 4. MENU DE NAVEGAÇÃO (SIDEBAR)
# ==========================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/679/679821.png", width=80)
st.sidebar.title("FastLog Menu")
st.sidebar.markdown("---")

tela_selecionada = st.sidebar.radio(
    "Acessar como:",
    ["👤 Área do Cliente (Frontend)", "🏢 Torre de Controle Logístico"]
)

st.sidebar.markdown("---")
st.sidebar.caption("Projeto de IA - RAG Multimodal")

# ==========================================
# 5. TELA 1: ÁREA DO CLIENTE
# ==========================================
if tela_selecionada == "👤 Área do Cliente (Frontend)":
    st.title("👤 Portal de Atendimento FastLog")
    st.markdown("Bem-vindo! Consulte o status da sua entrega falando com nossa inteligência artificial.")
    
    st.markdown("---")
    
    col_chat, col_vazia = st.columns([2, 1])
    
    with col_chat:
        st.subheader("💬 Fale com o Assistente")
        audio_data = st.audio_input("🎤 Grave sua pergunta:")
        pergunta_texto = st.text_input("⌨️ Ou digite o código de rastreio/pergunta:")
        
        pergunta_final = None
        
        if audio_data:
            with st.spinner("Ouvindo..."):
                pergunta_final = transcrever_audio_groq(audio_data.getvalue())
                st.success(f"🗣️ **Você disse:** {pergunta_final}")
                
        elif pergunta_texto:
            pergunta_final = pergunta_texto

        if pergunta_final:
            with st.spinner("Buscando sua entrega..."):
                contexto_dados = st.session_state.dados_logistica.to_string(index=False)
                prompt_sistema = f"""
                Você é a inteligência artificial de atendimento ao cliente da FastLog. 
                Responda de forma extremamente educada, curta e natural, como um atendente humano em um Call Center.
                NÃO use formatação complexa (asteriscos, markdown, listas). Fale apenas o essencial para a leitura em voz alta.
                Base de dados de clientes:
                {contexto_dados}
                """
                
                resposta = chamar_groq(prompt_sistema, pergunta_final)
                st.info("🤖 **Resposta FastLog:**")
                st.write(resposta)
                
                with st.spinner("Gerando voz..."):
                    audio_resposta = gerar_audio_resposta(resposta)
                    if audio_resposta:
                        st.audio(audio_resposta, format="audio/mp3", autoplay=True)
                        st.download_button(
                            label="💾 Baixar Resposta em MP3",
                            data=audio_resposta,
                            file_name="resposta_fastlog.mp3",
                            mime="audio/mp3"
                        )

# ==========================================
# 6. TELA 2: PAINEL DA EMPRESA (GESTOR)
# ==========================================
elif tela_selecionada == "🏢 Torre de Controle Logístico":
    st.title("🏢 Torre de Controle Logístico")
    st.markdown("Visão gerencial de frota e adição/edição de status em tempo real.")
    
    st.markdown("---")
    
    df_atual = st.session_state.dados_logistica
    total_pedidos = len(df_atual)
    
    if not df_atual.empty and 'status' in df_atual.columns:
        pedidos_entregues = len(df_atual[df_atual['status'].astype(str).str.contains('Entregue', case=False, na=False)])
        pedidos_atrasados = len(df_atual[df_atual['status'].astype(str).str.contains('Atrasado', case=False, na=False)])
    else:
        pedidos_entregues = 0
        pedidos_atrasados = 0
    
    col_metrica1, col_metrica2, col_metrica3 = st.columns(3)
    with col_metrica1:
        st.metric(label="📦 Total de Pacotes", value=total_pedidos)
    with col_metrica2:
        st.metric(label="✅ Entregas Concluídas", value=pedidos_entregues)
    with col_metrica3:
        st.metric(label="🚨 Atrasos Críticos", value=pedidos_atrasados, delta="- Atenção", delta_color="inverse")
    
    st.markdown("---")
    
    col_tabela, col_grafico = st.columns([1.5, 1])
    
    with col_tabela:
        # --- BOTÃO MÁGICO PARA LIMPAR TUDO ---
        col_tit, col_btn = st.columns([2, 1])
        with col_tit:
            st.subheader("📝 Adição e Edição de Status")
        with col_btn:
            if st.button("🗑️ Limpar Tabela"):
                df_vazio = pd.DataFrame(columns=colunas_padrao)
                st.session_state.dados_logistica = df_vazio
                df_vazio.to_csv("entregas.csv", index=False)
                st.rerun()

        st.caption("Adicione dados na linha em branco abaixo. O assistente do cliente será atualizado automaticamente.")
        
        # O data_editor agora usa uma chave (key) para forçar a atualização visual quando resetado
        df_editado = st.data_editor(st.session_state.dados_logistica, num_rows="dynamic", use_container_width=True, key="tabela_editor")
        
        # Salva as edições na memória E no arquivo CSV para não perder ao reiniciar
        st.session_state.dados_logistica = df_editado
        df_editado.to_csv("entregas.csv", index=False)
        
    with col_grafico:
        st.subheader("📈 Distribuição Operacional")
        if not df_editado.empty and 'status' in df_editado.columns:
            st.bar_chart(df_editado['status'].value_counts(), color="#FF4B4B")
        else:
            st.info("Adicione dados na tabela para visualizar o gráfico.")