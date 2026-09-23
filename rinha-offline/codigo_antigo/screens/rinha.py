import flet as ft
import asyncio
import random
from logic.galo import Galo
from data.galos_db import GALOS_DB
from logic.efeitos import BUFFS 

def criar_tela_rinha(jogador, page):
    if not jogador.galo_ativo:
        return ft.Text("Equipe um galo no perfil primeiro!")
        
    meu_galo = jogador.galo_ativo
    inimigo = Galo("Dummy", 100, "assets/galos/00_2.png")
    
    if meu_galo.nome in GALOS_DB:
        meu_galo.hp_max = GALOS_DB[meu_galo.nome]["hp_base"] + ((meu_galo.nivel - 1) * 12)
        meu_galo.hp_atual = meu_galo.hp_max

    texto_log = ft.Text("Procurando oponente...", size=14)
    
    texto_nome_meu = ft.Text(f"{jogador.nome} Level {meu_galo.nivel}", weight=ft.FontWeight.BOLD)
    texto_hp_meu = ft.Text(f"{meu_galo.hp_atual}/{meu_galo.hp_max}", size=12)
    barra_hp_meu = ft.ProgressBar(value=1.0, color=ft.Colors.GREEN, width=150)
    
    texto_nome_inimigo = ft.Text(f"{inimigo.nome} Level {inimigo.nivel}", weight=ft.FontWeight.BOLD)
    texto_hp_inimigo = ft.Text(f"{inimigo.hp_atual}/{inimigo.hp_max}", size=12)
    barra_hp_inimigo = ft.ProgressBar(value=1.0, color=ft.Colors.PURPLE, width=150)
    
    imagem_combate = ft.Image(src=meu_galo.caminho_imagem, height=200, fit="contain")

    seletor_vel = ft.Dropdown(
        label="Velocidade",
        options=[
            ft.dropdown.Option("1.0", "1x (Normal)"),
            ft.dropdown.Option("0.5", "2x (Rápido)"),
            ft.dropdown.Option("0.1", "10x (Flash)")
        ],
        value=jogador.vel_rinha, 
        width=150
    )
    
    seletor_dificuldade = ft.Dropdown(
        label="Dificuldade",
        options=[
            ft.dropdown.Option("Facil", "Fácil"),
            ft.dropdown.Option("Medio", "Médio"),
            ft.dropdown.Option("Dificil", "Difícil"),
            ft.dropdown.Option("Extremo", "Extremo"),
            ft.dropdown.Option("Insano", "Insano")
        ],
        value=jogador.dif_rinha, 
        width=150
    )
    
    auto_revive = ft.Switch(
        label="Auto-Revive", 
        value=False,
        label_position=ft.LabelPosition.LEFT
    )

    def on_click_reiniciar(e):
        arena.reiniciar_solicitado = True
        
    btn_reiniciar = ft.TextButton(
        "Treinar Novamente",
        on_click=on_click_reiniciar,
        visible=False,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.GREEN_700, 
            color=ft.Colors.WHITE
        )
    )

    arena = ft.Container(
        bgcolor=ft.Colors.BLACK_87,
        padding=15,
        border_radius=10,
        content=ft.Column([
            texto_log,
            ft.Divider(color=ft.Colors.GREY_800),
            ft.Row([
                ft.Column([
                    texto_nome_meu,
                    texto_hp_meu,
                    barra_hp_meu
                ]),
                ft.Column([
                    texto_nome_inimigo,
                    texto_hp_inimigo,
                    barra_hp_inimigo
                ], horizontal_alignment=ft.CrossAxisAlignment.END)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(height=10),
            ft.Row([
                imagem_combate
            ], alignment=ft.MainAxisAlignment.CENTER)
        ])
    )

    def atualizar_tela():
        texto_nome_meu.value = f"{jogador.nome} Level {meu_galo.nivel}"
        texto_hp_meu.value = f"{meu_galo.hp_atual}/{meu_galo.hp_max}"
        barra_hp_meu.value = meu_galo.hp_atual / meu_galo.hp_max
        
        texto_nome_inimigo.value = f"{inimigo.nome} Level {inimigo.nivel}"
        texto_hp_inimigo.value = f"{inimigo.hp_atual}/{inimigo.hp_max}"
        barra_hp_inimigo.value = inimigo.hp_atual / inimigo.hp_max
        
        try:
            page.update()
        except Exception:
            pass

    async def loop_batalha():
        def arena_ativa():
            try:
                return arena.page is not None
            except RuntimeError:
                return False

        pesos_raridade = {
             "Common": 1, "Rare": 2, "Epic": 3,
             "Legendary": 4, "Mythic": 5, "Divine": 6
        }
        
        while arena_ativa():
            jogador.vel_rinha = seletor_vel.value
            jogador.dif_rinha = seletor_dificuldade.value
            
            dificuldade = seletor_dificuldade.value
            nivel_base = meu_galo.nivel
            
            raridade_jogador = GALOS_DB.get(meu_galo.nome, {}).get("raridade", "Common")
            peso_jogador = pesos_raridade.get(raridade_jogador, 1)

            galos_permitidos = []
            for nome, dados in GALOS_DB.items():
                peso_inim = pesos_raridade.get(dados.get("raridade", "Common"), 1)
                if dificuldade == "Facil" and peso_inim <= 5: 
                    galos_permitidos.append(nome)
                elif dificuldade == "Medio" and peso_inim >= 2: 
                    galos_permitidos.append(nome)
                elif dificuldade == "Dificil" and peso_inim >= 3: 
                    galos_permitidos.append(nome)
                elif dificuldade == "Extremo" and peso_inim >= 4: 
                    galos_permitidos.append(nome)
                elif dificuldade == "Insano" and peso_inim >= 5: 
                    galos_permitidos.append(nome)
            
            if not galos_permitidos: 
                galos_permitidos = list(GALOS_DB.keys())
                
            nome_sorteado = random.choice(galos_permitidos) 
            dados_inimigo = GALOS_DB[nome_sorteado]
            peso_inimigo = pesos_raridade.get(dados_inimigo.get("raridade", "Common"), 1)
            
            if dificuldade == "Facil":
                nivel_inimigo = max(1, nivel_base - 1)
                if peso_inimigo > peso_jogador: 
                    nivel_inimigo = max(1, nivel_inimigo - (peso_inimigo - peso_jogador))
                mult_xp = 1.0
                bonus_xp = 0
            elif dificuldade == "Medio":
                nivel_inimigo = nivel_base
                mult_xp = 1.30
                bonus_xp = 1
            elif dificuldade == "Dificil":
                nivel_inimigo = int(nivel_base * 1.40)
                mult_xp = 1.60
                bonus_xp = 2
            elif dificuldade == "Extremo":
                nivel_inimigo = nivel_base * 2
                mult_xp = 1.80
                bonus_xp = 5
            elif dificuldade == "Insano":
                nivel_inimigo = nivel_base * 3
                mult_xp = 2.65
                bonus_xp = 8
            else:
                nivel_inimigo = nivel_base
                mult_xp = 1.0
                bonus_xp = 0
            
            inimigo.nome = nome_sorteado
            inimigo.tipo = dados_inimigo["tipo"]
            inimigo.nivel = nivel_inimigo
            inimigo.hp_max = dados_inimigo["hp_base"] + ((nivel_inimigo - 1) * 12) 
            inimigo.hp_atual = inimigo.hp_max
            inimigo.caminho_imagem = dados_inimigo["caminho_imagem"]
            
            inimigo.equipar_skills_bot() 
            meu_galo.hp_atual = meu_galo.hp_max
            
            meu_galo.efeitos = {}
            inimigo.efeitos = {}
            
            historico_log = []
            def adicionar_log(msg):
                historico_log.append(msg)
                if len(historico_log) > 2:
                    historico_log.pop(0)
                texto_log.value = "\n".join(historico_log)
            
            adicionar_log(f"Um {inimigo.nome} Lvl {inimigo.nivel} apareceu!")
            atualizar_tela()
            
            vel = float(seletor_vel.value)
            await asyncio.sleep(vel)
            
            turno_jogador = True
            
            while meu_galo.hp_atual > 0 and inimigo.hp_atual > 0:
                if not arena_ativa(): 
                    return 
                
                jogador.vel_rinha = seletor_vel.value
                jogador.dif_rinha = seletor_dificuldade.value
                vel = float(seletor_vel.value)
                
                atacante = meu_galo if turno_jogador else inimigo
                defensor = inimigo if turno_jogador else meu_galo
                nome_atacante = jogador.nome if turno_jogador else inimigo.nome
                
                imagem_combate.src = atacante.caminho_imagem
                imagem_combate.scale = ft.Scale(scale_x=1 if turno_jogador else -1, scale_y=1)

                mensagens_efeito, pode_atacar = atacante.processar_efeitos_inicio_turno()
                if mensagens_efeito:
                    for msg in mensagens_efeito:
                        adicionar_log(msg)
                    atualizar_tela()
                    await asyncio.sleep(vel / 2)

                if atacante.hp_atual <= 0:
                    break

                if pode_atacar:
                    nome_skill, dano_ataque, efeito = atacante.atacar()
                    
                    foi_refletido = defensor.efeitos.get("Reflection", 0) > 0
                    if foi_refletido:
                        defensor.efeitos["Reflection"] -= 1
                        if defensor.efeitos["Reflection"] <= 0:
                            del defensor.efeitos["Reflection"]
                        
                        alvo_dano = atacante
                        tinha_escudo = alvo_dano.efeitos.get("Shield", 0) > 0
                        dano_real = alvo_dano.sofrer_dano(dano_ataque)
                        
                        msg_ataque = f"{defensor.nome} refletiu o ataque! {nome_atacante} sofreu {dano_real} de dano"
                    else:
                        alvo_dano = defensor
                        tinha_escudo = alvo_dano.efeitos.get("Shield", 0) > 0
                        dano_real = alvo_dano.sofrer_dano(dano_ataque)
                        
                        msg_ataque = f"{nome_atacante} usou {nome_skill} causando {dano_real} de dano"

                    if tinha_escudo:
                        msg_ataque += " (Bloqueado)"
                    
                    if efeito:
                        alvo_efeito = atacante if efeito["nome"] in BUFFS else alvo_dano 
                        aplicou = alvo_efeito.aplicar_efeito(efeito)
                        
                        if aplicou:
                            acao = "ativou" if alvo_efeito == atacante else "aplicou"
                            msg_ataque += f" e {acao} {efeito['nome']}!"
                            
                        if aplicou and efeito["nome"] in ["Life Steal", "Trade Blood For Food"]:
                            atacante.hp_atual = min(atacante.hp_max, atacante.hp_atual + dano_real)
                            msg_ataque += f" roubando {dano_real} HP!"
                    
                    adicionar_log(msg_ataque)

                atualizar_tela()
                await asyncio.sleep(vel)
                turno_jogador = not turno_jogador

            if arena_ativa(): 
                if meu_galo.hp_atual > 0:
                    xp_base = 34
                    xp_ganho = int((xp_base * mult_xp) + bonus_xp)
                    moedas_ganhas = 6
                    
                    meu_galo.ganhar_xp(xp_ganho)
                    jogador.moedas += moedas_ganhas
                    jogador.salvar()

                    texto_log.value = f"{jogador.nome} venceu!\n+{moedas_ganhas} Moedas | +{xp_ganho} XP\nProcurando próximo..."
                    atualizar_tela()
                    await asyncio.sleep(float(seletor_vel.value) * 2) 
                else:
                    if auto_revive.value:
                        texto_log.value = f"O teu galo foi derrotado...\nAuto-Revive ativado! Curando e procurando próximo..."
                        atualizar_tela()
                        await asyncio.sleep(float(seletor_vel.value) * 2)
                        continue
                        
                    texto_log.value = f"O teu galo foi derrotado... Treino encerrado."
                    btn_reiniciar.visible = True
                    atualizar_tela()
                    
                    reiniciar_agora = False
                    
                    # --- NOVO: LOOP DE ESPERA (IDLE LOOP) ---
                    # Mantém a thread viva sincronizando os seletores até o usuário sair da aba ou clicar em reiniciar
                    while arena_ativa():
                        jogador.vel_rinha = seletor_vel.value
                        jogador.dif_rinha = seletor_dificuldade.value
                        
                        if getattr(arena, "reiniciar_solicitado", False):
                            arena.reiniciar_solicitado = False
                            reiniciar_agora = True
                            break
                            
                        await asyncio.sleep(0.5) 
                    # ----------------------------------------
                    
                    btn_reiniciar.visible = False
                    
                    if reiniciar_agora:
                        texto_log.value = "Reiniciando treinamento..."
                        atualizar_tela()
                        await asyncio.sleep(1)
                        continue
                    else:
                        break

    page.run_task(loop_batalha)

    return ft.Column([
        ft.Text("Treinamento", size=30, weight=ft.FontWeight.BOLD),
        ft.Row([seletor_vel, seletor_dificuldade, auto_revive], alignment=ft.MainAxisAlignment.CENTER, wrap=True),
        arena,
        ft.Container(height=10),
        btn_reiniciar
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO)