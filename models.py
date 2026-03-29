# models.py
from datetime import datetime, timedelta

class Lote:
    def __init__(self, produto_nome, codigo, mes_validade, ano_validade, quantidade):
        self.produto_nome = produto_nome
        self.codigo = codigo
        self.mes_validade = mes_validade
        self.ano_validade = ano_validade
        self.quantidade = quantidade
        self.reservado = False
        self.data_reserva = None

    def calcular_meses_restantes(self, mes_atual, ano_atual):
        return (self.ano_validade - ano_atual) * 12 + (self.mes_validade - mes_atual)

    def checar_validade_reserva(self, data_atual):
        if self.reservado and self.data_reserva:
            if (data_atual - self.data_reserva).days > 30:
                self.reservado = False
                self.data_reserva = None

class PosicaoPallet:
    def __init__(self, endereco, capacidade=1):
        self.endereco = endereco
        self.capacidade = capacidade
        self.lotes = []
        self.cor_led = "BRANCO"

    def alocar_lote(self, lote_novo, mes_atual, ano_atual):
        if len(self.lotes) < self.capacidade:
            self.lotes.append(lote_novo)
            self.atualizar_led(mes_atual, ano_atual, datetime.now())
            return True
        return False
        
    def remover_lote(self, index=0):
        if self.lotes:
            self.lotes.pop(index)
            data_agora = datetime.now()
            self.atualizar_led(data_agora.month, data_agora.year, data_agora)

    def atualizar_lote(self, index, novo_nome, novo_cod, novo_mes, novo_ano, nova_qtd, mes_atual, ano_atual):
        if 0 <= index < len(self.lotes):
            l = self.lotes[index]
            l.produto_nome, l.codigo, l.mes_validade, l.ano_validade, l.quantidade = novo_nome, novo_cod, novo_mes, novo_ano, nova_qtd
            self.atualizar_led(mes_atual, ano_atual, datetime.now())

    def atualizar_led(self, mes_atual, ano_atual, data_atual):
        if not self.lotes:
            self.cor_led = "BRANCO"
            return
        for l in self.lotes: l.checar_validade_reserva(data_atual)
        menor_meses = min([l.calcular_meses_restantes(mes_atual, ano_atual) for l in self.lotes])
        tem_reservado = any([l.reservado for l in self.lotes])
        
        if menor_meses <= 0: self.cor_led = "PRETO"
        elif tem_reservado: self.cor_led = "ROXO"
        elif menor_meses == 1: self.cor_led = "VERMELHO"
        elif menor_meses <= 3: self.cor_led = "AMARELO"
        else: self.cor_led = "VERDE"

def gerar_nome_rua(index):
    nome = ""
    dividendo = index + 1
    while dividendo > 0:
        modulo = (dividendo - 1) % 26
        nome = chr(65 + modulo) + nome
        dividendo = (dividendo - modulo) // 26
    return nome