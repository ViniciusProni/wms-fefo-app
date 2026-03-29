# telas.py
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Importando do nosso próprio sistema
from models import Lote, PosicaoPallet, gerar_nome_rua
from database import db, registrar_log
from styles import injetar_css_login
from ui_components import desenhar_bloco_visual, desenhar_visao_panoramica

USUARIOS_SISTEMA = {
    "admin": {"senha": "123", "perfil": "admin", "nome": "Administrador"},
    "operador": {"senha": "123", "perfil": "operador", "nome": "Operador de Empilhadeira"},
    "supervisao": {"senha": "123", "perfil": "supervisao", "nome": "Supervisão de Qualidade"},
    "expedição": {"senha": "123", "perfil": "expedicao", "nome": "Equipe de Expedição"}
}

def tela_login():
    injetar_css_login()
    
    col_esq, col_meio, col_dir = st.columns([1, 1.5, 1])
    
    with col_meio:
        with st.form("form_login", clear_on_submit=False):
            st.markdown("<h1 style='text-align: center; color: white; margin-bottom: 5px;'>WMS FEFO</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #aaa; margin-bottom: 30px;'>Gestão Inteligente de Validades</p>", unsafe_allow_html=True)
            
            st.markdown("<label style='color:white;'>Usuário</label>", unsafe_allow_html=True)
            usuario_input = st.text_input("Usuário", label_visibility="collapsed").lower().strip()
            
            st.markdown("<label style='color:white; margin-top:15px; display:block;'>Senha</label>", unsafe_allow_html=True)
            senha_input = st.text_input("Senha", type="password", label_visibility="collapsed").strip()
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.form_submit_button("ACESSAR SISTEMA", use_container_width=True):
                if usuario_input in USUARIOS_SISTEMA and USUARIOS_SISTEMA[usuario_input]["senha"] == senha_input:
                    st.session_state['autenticado'] = True
                    st.session_state['usuario_login'] = usuario_input 
                    st.session_state['perfil'] = USUARIOS_SISTEMA[usuario_input]["perfil"]
                    st.session_state['nome_usuario'] = USUARIOS_SISTEMA[usuario_input]["nome"]
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos!")

def tela_hub_armazens():
    st.title("🏢 Complexo Logístico - Hub Central")
    
    c_user, c_logout = st.columns([4, 1])
    c_user.write(f"Bem-vindo, **{st.session_state['nome_usuario']}** ({st.session_state['perfil'].upper()})")
    if c_logout.button("Sair (Logout)"):
        st.session_state.clear()
        st.rerun()
        
    st.markdown("---")

    if not db['armazens']:
        if st.session_state['perfil'] in ['admin', 'supervisao']:
            st.info("O complexo está vazio. Nenhum armazém foi configurado ainda.")
            if st.button("➕ Criar Primeiro Armazém", type="primary", use_container_width=True):
                st.session_state['criando_armazem'] = True
                st.rerun()
        else:
            st.warning("⏳ Aguardando Setup. A Supervisão ainda não criou nenhum armazém.")
            if st.button("🔄 Atualizar"): st.rerun()
    else:
        st.subheader("Selecione um Armazém para Acessar:")
        
        cols = st.columns(3)
        nomes_armazens = list(db['armazens'].keys())
        
        for idx, nome in enumerate(nomes_armazens):
            dados = db['armazens'][nome]
            col = cols[idx % 3]
            with col:
                st.markdown(f"""
                <div style='background-color: #1e1e1e; padding: 20px; border-radius: 10px; border: 1px solid #4fc3f7; text-align: center; margin-bottom: 10px;'>
                    <h3 style='margin: 0; color: #4fc3f7;'>{nome}</h3>
                    <p style='margin: 5px 0 0 0; color: #ccc;'>Ruas: {dados['qtd_ruas']} | Vagas/Rua: {dados['qtd_pallets']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # SE FOR ADMIN OU SUPERVISOR, MOSTRA O BOTÃO DE EXCLUIR JUNTO
                if st.session_state['perfil'] in ['admin', 'supervisao']:
                    c_entrar, c_excluir = st.columns([4, 1])
                    with c_entrar:
                        if st.button("Entrar ➔", key=f"btn_entrar_{nome}", use_container_width=True):
                            st.session_state['armazem_atual'] = nome
                            registrar_log(nome, "Acesso", "Entrou no painel do armazém.")
                            st.rerun()
                    with c_excluir:
                        if st.button("🗑️", key=f"btn_del_{nome}", use_container_width=True, help="Excluir Armazém"):
                            del db['armazens'][nome]
                            st.rerun()
                # SE FOR OPERADOR OU EXPEDIÇÃO, MOSTRA SÓ O BOTÃO DE ENTRAR
                else:
                    if st.button("Entrar ➔", key=f"btn_entrar_{nome}", use_container_width=True):
                        st.session_state['armazem_atual'] = nome
                        registrar_log(nome, "Acesso", "Entrou no painel do armazém.")
                        st.rerun()

        st.markdown("---")
        if st.session_state['perfil'] in ['admin', 'supervisao']:
            if st.button("➕ Adicionar Novo Armazém ao Complexo"):
                st.session_state['criando_armazem'] = True
                st.rerun()

def tela_configuracao():
    col_esq, col_meio, col_dir = st.columns([1, 2, 1])
    with col_meio:
        st.title("⚙️ Construir Novo Armazém")
        with st.form("form_setup"):
            nome_armazem = st.text_input("Nome do Armazém", placeholder="Digite o nome...")
            qtd_ruas = st.number_input("Quantidade de Ruas", min_value=1, value=5)
            qtd_pallets = st.number_input("Endereços por Rua", min_value=1, value=20)
            capacidade_slot = st.number_input("Capacidade de Pallets por Endereço", min_value=1, value=1)
            
            c_btn1, c_btn2 = st.columns(2)
            with c_btn1:
                if st.form_submit_button("🔨 Construir", type="primary", use_container_width=True):
                    if not nome_armazem.strip(): st.error("O armazém precisa de um nome!")
                    elif nome_armazem in db['armazens']: st.error("Já existe um armazém com este nome!")
                    else:
                        db['armazens'][nome_armazem] = {'qtd_ruas': qtd_ruas, 'qtd_pallets': qtd_pallets, 'capacidade_slot': capacidade_slot, 'nomes_ruas': {gerar_nome_rua(r): "Setor Geral" for r in range(qtd_ruas)}, 'matriz': {f"{gerar_nome_rua(r)}{p+1}": PosicaoPallet(f"{gerar_nome_rua(r)}{p+1}", capacidade_slot) for r in range(qtd_ruas) for p in range(qtd_pallets)}, 'historico': []}
                        st.session_state['criando_armazem'] = False
                        st.rerun()
            with c_btn2:
                if st.form_submit_button("❌ Cancelar", use_container_width=True):
                    st.session_state['criando_armazem'] = False
                    st.rerun()

def tela_dashboard():
    nome_arm_atual = st.session_state['armazem_atual']
    if nome_arm_atual not in db['armazens']:
        st.session_state['armazem_atual'] = None
        st.rerun()
        
    arm = db['armazens'][nome_arm_atual]
    
    # FORÇA A ATUALIZAÇÃO DE TODOS OS LEDS E RESERVAS AO CARREGAR A TELA
    data_atual = datetime.now()
    mes_atual, ano_atual = data_atual.month, data_atual.year
    for p in arm['matriz'].values():
        p.atualizar_led(mes_atual, ano_atual, data_atual)
    
    c_voltar, c_titulo, c_user = st.columns([1, 2.5, 1])
    with c_voltar:
        if st.button("⬅️ Voltar ao Hub", use_container_width=True):
            registrar_log(nome_arm_atual, "Saída", "Retornou ao Hub Central.")
            st.session_state['armazem_atual'] = None
            st.rerun()
    with c_titulo:
        st.title(f"📦 {nome_arm_atual}")
    with c_user:
        st.write(f"👤 **{st.session_state['nome_usuario']}**")
    
    total_posicoes = arm['qtd_ruas'] * arm['qtd_pallets'] * arm['capacidade_slot']
    pallets_armazenados = sum([len(p.lotes) for p in arm['matriz'].values()])
    
    totais = {"VERDE": 0, "AMARELO": 0, "VERMELHO": 0, "PRETO": 0, "BRANCO": 0, "ROXO": 0}
    for p in arm['matriz'].values(): totais[p.cor_led] += 1

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Seguros", totais["VERDE"])
    c2.metric("Atenção", totais["AMARELO"])
    c3.metric("Urgentes", totais["VERMELHO"])
    c4.metric("Descarte", totais["PRETO"])
    c5.metric("Reservas", totais["ROXO"])
    c6.metric("End. Livres", totais["BRANCO"])
    
    st.markdown("---")
    
    col_acoes, col_mapa = st.columns([1.3, 2.2])

    with col_acoes:
        aba_entrada, aba_mover, aba_edicao, aba_saida, aba_analise, aba_historico = st.tabs(["📥 Guardar", "↔️ Mover", "✏️ Editar", "📤 Despachar", "🧠 Análise", "📜 Log"])

        with aba_entrada:
            if st.session_state['perfil'] == 'expedicao': st.info("🔒 Recebimento bloqueado para Expedição.")
            else:
                with st.form("form_entrada", clear_on_submit=True):
                    posicao_alvo = st.text_input("Rua/Pallet (Ex: A1)").upper().strip()
                    produto = st.text_input("Nome do Produto")
                    lote_cod = st.text_input("Código do Lote")
                    c_mes, c_ano = st.columns(2)
                    mes_val = c_mes.number_input("Mês Validade", 1, 12, step=1)
                    ano_val = c_ano.number_input("Ano Validade", 2024, 2050, step=1)
                    qtd = st.number_input("Quantidade (Caixas/Unidades)", 1, step=1)
                    if st.form_submit_button("Alocar Pallet"):
                        if not posicao_alvo or not produto or not lote_cod: st.warning("Preencha todos os campos!")
                        elif posicao_alvo not in arm['matriz']: st.error("Posição não existe.")
                        else:
                            pos = arm['matriz'][posicao_alvo]
                            if pos.alocar_lote(Lote(produto, lote_cod, mes_val, ano_val, qtd), mes_atual, ano_atual): 
                                registrar_log(nome_arm_atual, "Entrada", f"Alocou '{produto}' em {posicao_alvo}.")
                                st.success("Alocado!"); st.rerun()
                            else: st.error("Posição CHEIA!")

        with aba_mover:
            if st.session_state['perfil'] == 'expedicao': st.info("🔒 Remanejamento bloqueado para Expedição.")
            else:
                pos_ocupadas = [k for k, v in arm['matriz'].items() if v.lotes]
                pos_livres = [k for k, v in arm['matriz'].items() if len(v.lotes) < v.capacidade]
                
                if not pos_ocupadas: st.info("Armazém vazio.")
                elif not pos_livres: st.warning("Armazém cheio!")
                else:
                    with st.form("form_mover"):
                        origem = st.selectbox("1. Origem:", pos_ocupadas)
                        pos_origem_obj = arm['matriz'][origem]
                        opcoes_lotes = [f"Pallet {i+1}: {l.produto_nome}" for i, l in enumerate(pos_origem_obj.lotes)]
                        idx_lote = opcoes_lotes.index(st.selectbox("2. Qual Pallet?", opcoes_lotes))
                        destino = st.selectbox("3. Destino:", pos_livres)
                        
                        if st.form_submit_button("🔄 Transferir"):
                            if origem == destino: st.error("Origem e destino iguais.")
                            else:
                                lote_movido = pos_origem_obj.lotes.pop(idx_lote)
                                arm['matriz'][destino].lotes.append(lote_movido)
                                pos_origem_obj.atualizar_led(mes_atual, ano_atual, data_atual)
                                arm['matriz'][destino].atualizar_led(mes_atual, ano_atual, data_atual)
                                registrar_log(nome_arm_atual, "Movimentação", f"Moveu '{lote_movido.produto_nome}' de {origem} para {destino}.")
                                st.success("Transferido!"); st.rerun()

        with aba_edicao:
            if st.session_state['perfil'] in ['operador', 'expedicao']: st.info("🔒 Edição restrita à Supervisão.")
            else:
                pos_ocupadas = [k for k, v in arm['matriz'].items() if v.lotes]
                if pos_ocupadas:
                    pos_editar = st.selectbox("1. Selecione o Endereço:", pos_ocupadas)
                    pos_obj = arm['matriz'][pos_editar]
                    opcoes_lotes = [f"Pallet {i+1}: {l.produto_nome}" for i, l in enumerate(pos_obj.lotes)]
                    lote_idx = opcoes_lotes.index(st.selectbox("2. Selecione o pallet:", opcoes_lotes))
                    lote_atual = pos_obj.lotes[lote_idx]
                    
                    with st.form("form_edicao"):
                        e_prod = st.text_input("Produto", value=lote_atual.produto_nome)
                        e_cod = st.text_input("Lote", value=lote_atual.codigo)
                        c_mes, c_ano = st.columns(2)
                        e_mes = c_mes.number_input("Mês", 1, 12, value=lote_atual.mes_validade)
                        e_ano = c_ano.number_input("Ano", 2024, 2050, value=lote_atual.ano_validade)
                        e_qtd = st.number_input("Quantidade", 1, value=lote_atual.quantidade)
                        if st.form_submit_button("Salvar Alterações"):
                            pos_obj.atualizar_lote(lote_idx, e_prod, e_cod, e_mes, e_ano, e_qtd, mes_atual, ano_atual)
                            registrar_log(nome_arm_atual, "Edição", f"Editou '{e_prod}' em {pos_editar}.")
                            st.success("Atualizado!"); st.rerun()

        with aba_saida:
            if st.session_state['perfil'] == 'operador': st.info("🔒 Expedição restrita.")
            else:
                pos_ocupadas = [k for k, v in arm['matriz'].items() if v.lotes]
                if not pos_ocupadas: st.info("Armazém vazio.")
                else:
                    pos_saida = st.selectbox("Endereço:", pos_ocupadas, key="s_sel")
                    pos_obj = arm['matriz'][pos_saida]
                    
                    opcoes_saida = [f"Pallet {i+1}: {l.produto_nome} (Qtd: {l.quantidade})" for i, l in enumerate(pos_obj.lotes)]
                    lote_out_idx = opcoes_saida.index(st.selectbox("Qual pallet?", opcoes_saida))
                    lote_selecionado = pos_obj.lotes[lote_out_idx]
                    meses_restantes = lote_selecionado.calcular_meses_restantes(mes_atual, ano_atual)

                    if meses_restantes <= 0:
                        if st.session_state['perfil'] in ['supervisao', 'admin']:
                            st.error("⚠️ MODO SUPERVISOR: Produto Vencido.")
                            if st.button("🔴 Confirmar Descarte", type="primary"):
                                pos_obj.remover_lote(lote_out_idx)
                                registrar_log(nome_arm_atual, "Descarte", f"Descartou '{lote_selecionado.produto_nome}' de {pos_saida}.")
                                st.rerun()
                        else:
                            st.error("⛔ PRODUTO VENCIDO. Expedição/Reserva Bloqueada.")
                    else:
                        acoes_possiveis = ["📦 Expedir Pallet Completo", "🤏 Retirada Parcial (Picking)"]
                        
                        if not lote_selecionado.reservado:
                            acoes_possiveis.append("🟣 Reservar Pallet (30 dias)")
                        else:
                            acoes_possiveis.append("❌ Cancelar Reserva")

                        tipo_saida = st.radio("Ação:", acoes_possiveis)

                        if tipo_saida == "📦 Expedir Pallet Completo":
                            if st.button("Confirmar Expedição", type="primary"):
                                pos_obj.remover_lote(lote_out_idx)
                                registrar_log(nome_arm_atual, "Expedição", f"Expediu '{lote_selecionado.produto_nome}' de {pos_saida}.")
                                st.rerun()
                                
                        elif tipo_saida == "🤏 Retirada Parcial (Picking)":
                            qtd_retirar = st.number_input(f"Quantidade (Máx: {lote_selecionado.quantidade})", min_value=1, max_value=lote_selecionado.quantidade, value=1)
                            if st.button("Confirmar Picking"):
                                if qtd_retirar == lote_selecionado.quantidade: pos_obj.remover_lote(lote_out_idx)
                                else: lote_selecionado.quantidade -= qtd_retirar
                                pos_obj.atualizar_led(mes_atual, ano_atual, data_atual)
                                registrar_log(nome_arm_atual, "Expedição Parcial", f"Retirou {qtd_retirar}x '{lote_selecionado.produto_nome}' de {pos_saida}.")
                                st.rerun()
                                
                        elif tipo_saida == "🟣 Reservar Pallet (30 dias)":
                            st.info("O pallet ficará bloqueado visualmente na cor ROXA por 30 dias. Após isso, a reserva cai automaticamente.")
                            if st.button("Confirmar Reserva", type="primary"):
                                lote_selecionado.reservado = True
                                lote_selecionado.data_reserva = data_atual
                                pos_obj.atualizar_led(mes_atual, ano_atual, data_atual)
                                registrar_log(nome_arm_atual, "Reserva", f"Reservou '{lote_selecionado.produto_nome}' em {pos_saida}.")
                                st.rerun()
                                
                        elif tipo_saida == "❌ Cancelar Reserva":
                            if st.button("Cancelar Reserva Agora"):
                                lote_selecionado.reservado = False
                                lote_selecionado.data_reserva = None
                                pos_obj.atualizar_led(mes_atual, ano_atual, data_atual)
                                registrar_log(nome_arm_atual, "Cancelamento Reserva", f"Cancelou reserva de '{lote_selecionado.produto_nome}' em {pos_saida}.")
                                st.rerun()

        with aba_analise:
            lista = [{"End": p.endereco, "Produto": l.produto_nome, "Qtd": l.quantidade, "Val.": f"{l.mes_validade:02d}/{l.ano_validade}", "Meses": l.calcular_meses_restantes(mes_atual, ano_atual), "Status": "⚫ Vencidos" if l.calcular_meses_restantes(mes_atual, ano_atual) <= 0 else ("🟣 Reservados" if l.reservado else ("🔴 Urgentes" if l.calcular_meses_restantes(mes_atual, ano_atual) == 1 else ("🟡 Atenção" if l.calcular_meses_restantes(mes_atual, ano_atual) <= 3 else "🟢 Seguros")))} for p in arm['matriz'].values() for l in p.lotes]
            filtro = st.selectbox("Filtrar Risco:", ["📋 Mostrar Todos", "⚫ Vencidos", "🟣 Reservados", "🔴 Urgentes", "🟡 Atenção", "🟢 Seguros"])
            if lista:
                df = pd.DataFrame(lista)
                if filtro != "📋 Mostrar Todos": df = df[df["Status"] == filtro]
                if not df.empty:
                    st.dataframe(df.sort_values(by="Meses").style.apply(lambda r: ['background-color: rgba(100,100,100,0.3);' if "Vencidos" in r['Status'] else ('background-color: rgba(211,47,47,0.3);' if "Urgentes" in r['Status'] else ('background-color: rgba(245,124,0,0.3);' if "Atenção" in r['Status'] else ('background-color: rgba(142,36,170,0.3);' if "Reservados" in r['Status'] else 'background-color: rgba(56,142,60,0.3);')))] * len(r), axis=1), use_container_width=True, hide_index=True)
                else: st.success("Vazio!")
            else: st.info("Armazém vazio.")

        with aba_historico:
            if st.session_state['perfil'] not in ['admin', 'supervisao']: st.error("🔒 Acesso Negado")
            elif not arm['historico']: st.info("Nenhuma atividade.")
            else: st.dataframe(pd.DataFrame(arm['historico']), use_container_width=True, hide_index=True)

    with col_mapa:
        modo_visao = st.radio("👁️ Alternar Layout:", ["🔎 Detalhado (Por Rua)", "🗺️ Panorâmico"], horizontal=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if modo_visao == "🔎 Detalhado (Por Rua)":
            rua_atual = st.selectbox("Selecione a Rua:", [gerar_nome_rua(r) for r in range(arm['qtd_ruas'])])
            grid_html = f"""<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 15px; margin-top: 15px;">"""
            for p in range(arm['qtd_pallets']): grid_html += desenhar_bloco_visual(arm['matriz'][f"{rua_atual}{p + 1}"], mes_atual, ano_atual)
            st.markdown(grid_html + "</div>", unsafe_allow_html=True)
        else:
            st.markdown(desenhar_visao_panoramica(arm['matriz'], arm['nomes_ruas'], arm['qtd_ruas'], arm['qtd_pallets'], mes_atual, ano_atual), unsafe_allow_html=True)