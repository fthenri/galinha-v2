import flet as ft

def criar_tela_perfil(jogador):
    main_col = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )
    
    def render():
        main_col.controls.clear()
        
        main_col.controls.append(ft.Container(height=10)) 
        main_col.controls.append(ft.Text(f"Perfil de {jogador.nome}", size=30, weight=ft.FontWeight.BOLD))
        main_col.controls.append(ft.Text(f"🪙 Moedas: {jogador.moedas} | 🐔 Galo Coins: {jogador.galo_coins}", size=18, color=ft.Colors.AMBER))
        main_col.controls.append(ft.Divider())
        main_col.controls.append(ft.Text("Seu Time (Galos):", size=24, weight=ft.FontWeight.BOLD))
        
        # Row com wrap=True para quebrar linha automaticamente (grelha responsiva)
        galos_list = ft.Row(
            wrap=True, 
            spacing=20, 
            run_spacing=20, # Espaçamento vertical entre as linhas quando quebram
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.START
        )
        
        for galo in jogador.galos:
            is_active = (jogador.galo_ativo == galo)
            
            if not galo.skills_equipadas or all(s is None for s in galo.skills_equipadas):
                galo.equipar_skills_bot()
                
            desbloqueadas = galo.obter_skills_desbloqueadas()
            desbloqueadas.sort(key=lambda x: x[0]) # Ordem crescente de nível
            
            qnt_vazios = sum(1 for s in galo.skills_equipadas if s is None)
            
            # Travar e resetar as skills se tiver menos de 6 desbloqueadas
            if len(desbloqueadas) < 6 or (qnt_vazios > 0 and len(desbloqueadas) >= 5):
                print(f"[DEBUG] Forcando equipar_bot no galo {galo.nome} | Lvl {galo.nivel} | Desbloqueadas: {len(desbloqueadas)} | Vazios: {qnt_vazios}")
                galo.equipar_skills_bot()
                jogador.salvar()
                
            # Botão de Equipar Galo
            def equipar(e):
                g = e.control.data
                jogador.galo_ativo = g
                jogador.salvar()
                render() 
                if main_col.page:
                    main_col.page.update()

            texto_btn = "Galo Ativo" if is_active else "Equipar Galo"
            btn_equipar = ft.TextButton(
                texto_btn,
                disabled=is_active,
                on_click=equipar,
                data=galo
            )
            
            skills_col = ft.Column(spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            dropdowns_ref = []
            
            for i in range(5):
                val = None
                if i < len(galo.skills_equipadas) and galo.skills_equipadas[i]:
                    val = galo.skills_equipadas[i]["nome"]
                
                # Lista de skills que já estão equipadas em OUTROS slots
                skills_em_outros_slots = [
                    s["nome"] for idx, s in enumerate(galo.skills_equipadas) 
                    if s is not None and idx != i
                ]
                    
                opcoes_dropdown = []
                for lvl, sk in desbloqueadas:
                    # Só adiciona se não estiver equipado em outro slot
                    if sk["nome"] not in skills_em_outros_slots:
                        opcoes_dropdown.append(
                            ft.dropdown.Option(
                                key=sk["nome"], 
                                text=f"[Nv.{lvl}] {sk['nome']} ({sk.get('min', 0)} - {sk.get('max', 0)})"
                            )
                        )

                dd = ft.Dropdown(
                    label=f"Slot {i+1}",
                    value=val,
                    options=opcoes_dropdown,
                    width=250,
                    dense=True,
                    disabled=len(desbloqueadas) < 6
                )
                dropdowns_ref.append(dd)
                skills_col.controls.append(dd)
                
            # --- NOVO: BOTAO PARA FORÇAR O SALVAMENTO E BOTAO RESET ---
            def salvar_skills_manual(e):
                g = e.control.data["galo"]
                dds = e.control.data["dropdowns"]
                print(f"\n[DEBUG] === SALVAR HABILIDADES CLICADO para {g.nome} ===")
                try:
                    novas_skills = [d.value for d in dds]
                    skills_validas = [s for s in novas_skills if s is not None]
                    
                    # Verificar duplicadas
                    if len(skills_validas) != len(set(skills_validas)):
                        print("[DEBUG] Duplicada detectada no salvamento manual!")
                        if main_col.page:
                            main_col.page.snack_bar = ft.SnackBar(ft.Text("Existem habilidades duplicadas! Remova a repetição antes de salvar.", color=ft.Colors.WHITE), bgcolor=ft.Colors.RED)
                            main_col.page.snack_bar.open = True
                            main_col.page.update()
                        return
                        
                    print(f"[DEBUG] Skills selecionadas válidas: {novas_skills}")
                    
                    # Atualizar backend
                    for idx, val in enumerate(novas_skills):
                        while len(g.skills_equipadas) <= idx:
                            g.skills_equipadas.append(None)
                            
                        if val is None:
                            g.skills_equipadas[idx] = None
                        else:
                            for lvl, sk in g.obter_skills_desbloqueadas():
                                if sk["nome"] == val:
                                    g.skills_equipadas[idx] = sk
                                    break
                                    
                    # Garantir tamanho 5
                    while len(g.skills_equipadas) < 5:
                        g.skills_equipadas.append(None)
                    if len(g.skills_equipadas) > 5:
                        g.skills_equipadas = g.skills_equipadas[:5]
                        
                    jogador.salvar()
                    print("[DEBUG] Skills salvas no backend com sucesso!")
                    
                    if main_col.page:
                        main_col.page.snack_bar = ft.SnackBar(ft.Text("Habilidades salvas com sucesso!", color=ft.Colors.WHITE), bgcolor=ft.Colors.GREEN)
                        main_col.page.snack_bar.open = True
                        
                        # Recarrega a UI para atualizar as listas (removendo opções agora equipadas)
                        render()
                        main_col.page.update()
                except Exception as ex:
                    import traceback
                    traceback.print_exc()
                    print(f"[DEBUG ERRO CRITICO] Erro ao salvar skills manual: {ex}")
                    
            def resetar_skills_manual(e):
                print(f"[DEBUG] Resetando UI para o galo {galo.nome}")
                render()
                if main_col.page:
                    main_col.page.update()
                    
            btn_salvar_skills = ft.TextButton(
                "Salvar Mudanças", 
                on_click=salvar_skills_manual, 
                data={"galo": galo, "dropdowns": dropdowns_ref},
                disabled=len(desbloqueadas) < 6
            )
            
            btn_resetar = ft.TextButton(
                "Desfazer",
                on_click=resetar_skills_manual,
                disabled=len(desbloqueadas) < 6
            )
            
            botoes_row = ft.Row(
                [btn_resetar, btn_salvar_skills],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20
            )
            
            skills_col.controls.append(ft.Container(height=5))
            skills_col.controls.append(botoes_row)
            # ---------------------------------------------
            
            # Altura fixa removida do Container interno para permitir que cresça consoante o conteúdo
            card = ft.Card(
                bgcolor=ft.Colors.BLUE_GREY_900 if is_active else ft.Colors.GREY_900,
                elevation=10 if is_active else 2,
                width=340,
                content=ft.Container(
                    padding=20,
                    width=340,
                    content=ft.Column([
                        ft.Image(src=galo.caminho_imagem, width=150, height=150),
                        ft.Text(f"{galo.nome}", weight=ft.FontWeight.BOLD, size=20),
                        ft.Text(f"Tipo: {galo.tipo} | Nível: {galo.nivel}", size=14),
                        ft.Text(f"HP: {galo.hp_max}", color=ft.Colors.RED_400, weight=ft.FontWeight.BOLD, size=16),
                        btn_equipar,
                        ft.Divider(color=ft.Colors.GREY_700),
                        ft.Text("HABILIDADES EQUIPADAS", weight=ft.FontWeight.BOLD, size=14),
                        skills_col
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                )
            )
            galos_list.controls.append(card)
            
        # Altura fixa removida para que o scroll vertical da página atue livremente
        main_col.controls.append(
            ft.Container(
                content=galos_list,
                padding=20
            )
        )
        
    render()
    
    return main_col