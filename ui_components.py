# ui_components.py
from datetime import timedelta
from models import gerar_nome_rua

def gerar_conteudo_tooltip(posicao_obj, cor_status, mes_atual, ano_atual):
    info = f"<div style='margin-bottom: 12px; width: 100%; border-bottom: 1px solid #444; padding-bottom: 8px;'><span style='font-size: 1.3em; font-weight: bold; color: #4fc3f7;'>Endereço: {posicao_obj.endereco}</span><br><span style='font-size: 1em; color: #aaa;'>Ocupação: {len(posicao_obj.lotes)} / {posicao_obj.capacidade} pallets</span></div>"
    if posicao_obj.lotes:
        info += "<div style='display: flex; flex-direction: column; gap: 10px; width: 100%;'>"
        for i, l in enumerate(posicao_obj.lotes):
            meses = l.calcular_meses_restantes(mes_atual, ano_atual)
            alerta = "⚠️" if meses <= 3 else "✅"
            if meses <= 0: alerta = "❌"
            if l.reservado: alerta = "🟣"
            cor_texto = "#ff5252" if meses <= 0 else ("#ffd54f" if meses <= 3 else "#a5d6a7")
            if l.reservado: cor_texto = "#ce93d8"
            
            txt_status = f"Vence em: {l.mes_validade:02d}/{l.ano_validade} ({meses} meses)"
            if l.reservado and l.data_reserva: 
                venc_reserva = l.data_reserva + timedelta(days=30)
                txt_status += f"<br>⏳ Reserva: {venc_reserva.strftime('%d/%m/%Y')}"
            
            info += f"<div style='background: rgba(255,255,255,0.08); padding: 10px; border-radius: 8px;'><strong style='font-size: 1.15em; color: white;'>{i+1}. {l.produto_nome} (Qtd: {l.quantidade})</strong><br><span style='font-size: 0.95em; color: #ccc;'>Lote: {l.codigo}</span><br><span style='font-size: 0.95em; color: {cor_texto};'>{alerta} {txt_status}</span></div>"
        info += f"</div><div style='margin-top: 12px; padding-top: 10px; border-top: 1px solid #444; width: 100%; text-align: center;'><span style='font-size: 1.1em; font-weight: bold; text-transform: uppercase;'>Status: {cor_status}</span></div>"
    else:
        info += f"<div style='padding: 20px 0; text-align: center; width: 100%;'><strong style='font-size: 1.3em; color: #a5d6a7;'>ESPAÇO LIVRE</strong></div>"
    return info.replace('\n', '')

def desenhar_bloco_visual(posicao_obj, mes_atual, ano_atual):
    cores = {"VERDE": {"bg": "#2e7d32", "text": "white", "status": "SEGURO"}, "AMARELO": {"bg": "#fbc02d", "text": "black", "status": "ATENÇÃO"}, "VERMELHO": {"bg": "#c62828", "text": "white", "status": "URGENTE"}, "PRETO": {"bg": "#212121", "text": "white", "status": "VENCIDO"}, "BRANCO": {"bg": "#f0f2f6", "text": "#31333F", "status": "LIVRE"}, "ROXO": {"bg": "#8e24aa", "text": "white", "status": "RESERVADO"} }
    cor = cores[posicao_obj.cor_led]
    nome_prod = posicao_obj.lotes[0].produto_nome if posicao_obj.lotes else "VAZIO"
    ocupacao = f"{len(posicao_obj.lotes)}/{posicao_obj.capacidade}" if posicao_obj.lotes else ""
    tooltip = gerar_conteudo_tooltip(posicao_obj, cor["status"], mes_atual, ano_atual)

    return f"""<div class="pallet-box" style="background-color: {cor['bg']}; color: {cor['text']}; padding: 30px 15px; border-radius: 12px; text-align: center; height: 180px; display: flex; flex-direction: column; justify-content: center; align-items: center;"><strong style="font-size: 2.2em; margin-bottom: 8px;">{posicao_obj.endereco}</strong><span style="font-size: 1.3em; font-weight: bold; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; width: 100%;">{nome_prod}</span><span style="font-size: 1.1em; opacity: 0.9;">{ocupacao}</span><div class="fefo-tooltip">{tooltip}</div></div>""".replace('\n', '')

def desenhar_visao_panoramica(armazem_matriz, nomes_ruas, qtd_ruas, qtd_pallets, mes_atual, ano_atual):
    cores = {"VERDE": "#2e7d32", "AMARELO": "#fbc02d", "VERMELHO": "#c62828", "PRETO": "#212121", "BRANCO": "#f0f2f6", "ROXO": "#8e24aa"}
    status_text = {"VERDE": "SEGURO", "AMARELO": "ATENÇÃO", "VERMELHO": "URGENTE", "PRETO": "VENCIDO", "BRANCO": "LIVRE", "ROXO": "RESERVADO"}
    
    html = '<div style="display: flex; gap: 30px; justify-content: center; flex-wrap: wrap; margin-top: 20px;">'
    for r in range(qtd_ruas):
        letra_rua = gerar_nome_rua(r)
        html += f"<div style='background-color: rgba(255,255,255,0.05); padding: 15px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);'><div style='text-align: center; margin-bottom: 15px;'><strong style='font-size: 1.3em; color: #4fc3f7;'>RUA {letra_rua}</strong><br><span style='font-size: 0.9em; color: #aaa;'>{nomes_ruas[letra_rua]}</span></div><div style='display: grid; grid-template-columns: 1fr 1fr; gap: 10px; background-color: #1e1e1e; padding: 15px; border-radius: 6px;'>"
        for p in range(qtd_pallets):
            pos_obj = armazem_matriz[f"{letra_rua}{p + 1}"]
            tooltip = gerar_conteudo_tooltip(pos_obj, status_text[pos_obj.cor_led], mes_atual, ano_atual)
            html += f"<div class='mini-pallet' style='background-color: {cores[pos_obj.cor_led]}; display: flex; justify-content: center; align-items: center; font-size: 1.2em; color: {'#000' if pos_obj.cor_led in ['AMARELO', 'BRANCO'] else '#fff'}; font-weight: bold;'>{p+1}<div class='fefo-tooltip'>{tooltip}</div></div>"
        html += '</div></div>'
    html += '</div>'
    return html.replace('\n', '')# ui_components.py
from datetime import timedelta
from models import gerar_nome_rua

def gerar_conteudo_tooltip(posicao_obj, cor_status, mes_atual, ano_atual):
    info = f"<div style='margin-bottom: 12px; width: 100%; border-bottom: 1px solid #444; padding-bottom: 8px;'><span style='font-size: 1.3em; font-weight: bold; color: #4fc3f7;'>Endereço: {posicao_obj.endereco}</span><br><span style='font-size: 1em; color: #aaa;'>Ocupação: {len(posicao_obj.lotes)} / {posicao_obj.capacidade} pallets</span></div>"
    if posicao_obj.lotes:
        info += "<div style='display: flex; flex-direction: column; gap: 10px; width: 100%;'>"
        for i, l in enumerate(posicao_obj.lotes):
            meses = l.calcular_meses_restantes(mes_atual, ano_atual)
            alerta = "⚠️" if meses <= 3 else "✅"
            if meses <= 0: alerta = "❌"
            if l.reservado: alerta = "🟣"
            cor_texto = "#ff5252" if meses <= 0 else ("#ffd54f" if meses <= 3 else "#a5d6a7")
            if l.reservado: cor_texto = "#ce93d8"
            
            txt_status = f"Vence em: {l.mes_validade:02d}/{l.ano_validade} ({meses} meses)"
            if l.reservado and l.data_reserva: 
                venc_reserva = l.data_reserva + timedelta(days=30)
                txt_status += f"<br>⏳ Reserva: {venc_reserva.strftime('%d/%m/%Y')}"
            
            info += f"<div style='background: rgba(255,255,255,0.08); padding: 10px; border-radius: 8px;'><strong style='font-size: 1.15em; color: white;'>{i+1}. {l.produto_nome} (Qtd: {l.quantidade})</strong><br><span style='font-size: 0.95em; color: #ccc;'>Lote: {l.codigo}</span><br><span style='font-size: 0.95em; color: {cor_texto};'>{alerta} {txt_status}</span></div>"
        info += f"</div><div style='margin-top: 12px; padding-top: 10px; border-top: 1px solid #444; width: 100%; text-align: center;'><span style='font-size: 1.1em; font-weight: bold; text-transform: uppercase;'>Status: {cor_status}</span></div>"
    else:
        info += f"<div style='padding: 20px 0; text-align: center; width: 100%;'><strong style='font-size: 1.3em; color: #a5d6a7;'>ESPAÇO LIVRE</strong></div>"
    return info.replace('\n', '')

def desenhar_bloco_visual(posicao_obj, mes_atual, ano_atual):
    cores = {"VERDE": {"bg": "#2e7d32", "text": "white", "status": "SEGURO"}, "AMARELO": {"bg": "#fbc02d", "text": "black", "status": "ATENÇÃO"}, "VERMELHO": {"bg": "#c62828", "text": "white", "status": "URGENTE"}, "PRETO": {"bg": "#212121", "text": "white", "status": "VENCIDO"}, "BRANCO": {"bg": "#f0f2f6", "text": "#31333F", "status": "LIVRE"}, "ROXO": {"bg": "#8e24aa", "text": "white", "status": "RESERVADO"} }
    cor = cores[posicao_obj.cor_led]
    nome_prod = posicao_obj.lotes[0].produto_nome if posicao_obj.lotes else "VAZIO"
    ocupacao = f"{len(posicao_obj.lotes)}/{posicao_obj.capacidade}" if posicao_obj.lotes else ""
    tooltip = gerar_conteudo_tooltip(posicao_obj, cor["status"], mes_atual, ano_atual)

    return f"""<div class="pallet-box" style="background-color: {cor['bg']}; color: {cor['text']}; padding: 30px 15px; border-radius: 12px; text-align: center; height: 180px; display: flex; flex-direction: column; justify-content: center; align-items: center;"><strong style="font-size: 2.2em; margin-bottom: 8px;">{posicao_obj.endereco}</strong><span style="font-size: 1.3em; font-weight: bold; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; width: 100%;">{nome_prod}</span><span style="font-size: 1.1em; opacity: 0.9;">{ocupacao}</span><div class="fefo-tooltip">{tooltip}</div></div>""".replace('\n', '')

def desenhar_visao_panoramica(armazem_matriz, nomes_ruas, qtd_ruas, qtd_pallets, mes_atual, ano_atual):
    cores = {"VERDE": "#2e7d32", "AMARELO": "#fbc02d", "VERMELHO": "#c62828", "PRETO": "#212121", "BRANCO": "#f0f2f6", "ROXO": "#8e24aa"}
    status_text = {"VERDE": "SEGURO", "AMARELO": "ATENÇÃO", "VERMELHO": "URGENTE", "PRETO": "VENCIDO", "BRANCO": "LIVRE", "ROXO": "RESERVADO"}
    
    html = '<div style="display: flex; gap: 30px; justify-content: center; flex-wrap: wrap; margin-top: 20px;">'
    for r in range(qtd_ruas):
        letra_rua = gerar_nome_rua(r)
        html += f"<div style='background-color: rgba(255,255,255,0.05); padding: 15px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);'><div style='text-align: center; margin-bottom: 15px;'><strong style='font-size: 1.3em; color: #4fc3f7;'>RUA {letra_rua}</strong><br><span style='font-size: 0.9em; color: #aaa;'>{nomes_ruas[letra_rua]}</span></div><div style='display: grid; grid-template-columns: 1fr 1fr; gap: 10px; background-color: #1e1e1e; padding: 15px; border-radius: 6px;'>"
        for p in range(qtd_pallets):
            pos_obj = armazem_matriz[f"{letra_rua}{p + 1}"]
            tooltip = gerar_conteudo_tooltip(pos_obj, status_text[pos_obj.cor_led], mes_atual, ano_atual)
            html += f"<div class='mini-pallet' style='background-color: {cores[pos_obj.cor_led]}; display: flex; justify-content: center; align-items: center; font-size: 1.2em; color: {'#000' if pos_obj.cor_led in ['AMARELO', 'BRANCO'] else '#fff'}; font-weight: bold;'>{p+1}<div class='fefo-tooltip'>{tooltip}</div></div>"
        html += '</div></div>'
    html += '</div>'
    return html.replace('\n', '')