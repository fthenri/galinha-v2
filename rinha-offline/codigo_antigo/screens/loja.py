import flet as ft
import time
from logic.loja_logica import atualizar_loja_diaria, abrir_lootbox
from data.galos_db import GALOS_DB
from logic.galo import Galo

def criar_tela_loja(jogador, page):
    atualizar_loja_diaria(jogador)
    
    def formatar_tempo(segundos):
        h = int(segundos // 3600)
        m = int((segundos % 3600) // 60)
        return f"{h}h {m}m"

    # Variáveis de interface que serão atualizadas dinamicamente
    texto_tempo = ft.Text("", size=14, color=ft.Colors.GREY_400)
    log_compras = ft.Text("", size=14, color=ft.Colors.GREEN_400)
    texto_moedas = ft.Text(size=18)
    texto_galocoins = ft.Text(size=18)
    coluna_diaria = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    coluna_lootboxes = ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=20)

    # Função responsável por desenhar e atualizar os itens e textos da loja
    def atualizar_ui():
        tempo_restante = max(0, jogador.loja_atualizacao - time.time())
        texto_tempo.value = f"Próxima atualização em: {formatar_tempo(tempo_restante)}"
        texto_moedas.value = f"🪙 Moedas: {jogador.moedas}"
        texto_galocoins.value = f"🐔 Galo Coins: {jogador.galo_coins}"
        
        # Recria os botões da loja diária
        coluna_diaria.controls.clear()
        for i, item in enumerate(jogador.loja_diaria):
            if item["comprado"]:
                coluna_diaria.controls.append(ft.Text(f"Esgotado", color=ft.Colors.RED_400))
            else:
                moeda_str = "Moedas" if item["moeda"] == "moedas" else "Galo Coins"
                btn = ft.TextButton(
                    f"Comprar {item['nome']} ({item['raridade']}) | {item['valor']} {moeda_str}",
                    on_click=lambda e, idx=i, val=item["valor"], m=item["moeda"]: comprar_diario(e, idx, val, m)
                )
                coluna_diaria.controls.append(btn)
        
        # Recria os botões das Lootboxes para atualizar o pity em tempo real
        coluna_lootboxes.controls = [
            ft.Column([
                ft.TextButton("Caixa Bronze\n400 Moedas", on_click=lambda e: comprar_lootbox(e, "Bronze", 400, "moedas")),
                ft.Text(f"Pity Épico: {jogador.pity_bronze}/15", size=12)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Column([
                ft.TextButton("Caixa Gold\n5000 Moedas", on_click=lambda e: comprar_lootbox(e, "Gold", 5000, "moedas")),
                ft.Text(f"Pity Lendário: {jogador.pity_gold}/30", size=12)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Column([
                ft.TextButton("Caixa Emerald\n5 Galo Coins", on_click=lambda e: comprar_lootbox(e, "Emerald", 5, "galo_coins")),
                ft.Text(f"Pity Mítico: {jogador.pity_emerald}/50", size=12)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        ]
        
        try:
            page.update()
        except Exception:
            pass

    def comprar_diario(e, index, preco, moeda):
        if moeda == "moedas" and jogador.moedas >= preco:
            jogador.moedas -= preco
        elif moeda == "galo_coins" and jogador.galo_coins >= preco:
            jogador.galo_coins -= preco
        else:
            log_compras.value = "Saldo insuficiente!"
            page.update()
            return
        
        jogador.loja_diaria[index]["comprado"] = True
        nome_galo = jogador.loja_diaria[index]["nome"]
        novo_galo = Galo(nome_galo, GALOS_DB[nome_galo]["hp_base"], GALOS_DB[nome_galo]["caminho_imagem"])
        jogador.adicionar_galo(novo_galo)
        jogador.salvar()
        
        log_compras.value = f"Você comprou {nome_galo}!"
        atualizar_ui()

    def comprar_lootbox(e, tipo, preco, moeda):
        if moeda == "moedas" and jogador.moedas >= preco:
            jogador.moedas -= preco
        elif moeda == "galo_coins" and jogador.galo_coins >= preco:
            jogador.galo_coins -= preco
        else:
            log_compras.value = "Saldo insuficiente!"
            page.update()
            return
        
        galo_ganho = abrir_lootbox(jogador, tipo)
        log_compras.value = f"Lootbox {tipo} aberta: Ganhou {galo_ganho.nome} ({GALOS_DB[galo_ganho.nome].get('raridade')})!"
        atualizar_ui()

    # Preenche a UI pela primeira vez ao abrir a aba
    atualizar_ui()

    return ft.Column([
        ft.Text("Loja", size=30, weight=ft.FontWeight.BOLD),
        ft.Row([texto_moedas, texto_galocoins], alignment=ft.MainAxisAlignment.CENTER, spacing=30),
        log_compras,
        ft.Divider(),
        ft.Text("Loja Diária", size=24),
        texto_tempo,
        coluna_diaria,
        ft.Divider(),
        ft.Text("Lootboxes", size=24),
        coluna_lootboxes
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO)