# database.py
import streamlit as st
from datetime import datetime

@st.cache_resource
def get_banco_de_dados():
    return {'armazens': {}}

db = get_banco_de_dados()

def inicializar_estados_sessao():
    if 'autenticado' not in st.session_state: st.session_state['autenticado'] = False
    if 'perfil' not in st.session_state: st.session_state['perfil'] = None 
    if 'usuario_login' not in st.session_state: st.session_state['usuario_login'] = None
    if 'nome_usuario' not in st.session_state: st.session_state['nome_usuario'] = None 
    if 'armazem_atual' not in st.session_state: st.session_state['armazem_atual'] = None
    if 'criando_armazem' not in st.session_state: st.session_state['criando_armazem'] = False

def registrar_log(nome_armazem, acao, detalhes):
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    db['armazens'][nome_armazem]['historico'].insert(0, {
        "Data/Hora": agora,
        "Usuário": st.session_state.get('nome_usuario', 'Sistema'),
        "Ação": acao,
        "Detalhes": detalhes
    })