# app.py
import streamlit as st

# Importamos as nossas ferramentas dos outros arquivos
from database import inicializar_estados_sessao
from styles import injetar_animacao_global, injetar_css_global
from telas import tela_login, tela_hub_armazens, tela_configuracao, tela_dashboard

# ==========================================================
# BOOTSTRAP DA APLICAÇÃO (O INÍCIO DE TUDO)
# ==========================================================
st.set_page_config(page_title="WMS FEFO", layout="wide")

# 1. Aplica animação global de transição
injetar_animacao_global()

# 2. Prepara a memória da sessão
inicializar_estados_sessao()

# 3. Se logado, injeta o CSS dos botões e painéis
if st.session_state['autenticado']:
    injetar_css_global()

# 4. Roteador: Decide qual tela mostrar dependendo do momento do usuário
if not st.session_state['autenticado']: 
    tela_login()
elif st.session_state['criando_armazem']:
    tela_configuracao()
elif not st.session_state['armazem_atual']: 
    tela_hub_armazens()
else: 
    tela_dashboard()