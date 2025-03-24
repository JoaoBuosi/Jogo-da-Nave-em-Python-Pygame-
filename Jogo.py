import pygame
import sys
import random
import math

pygame.init()

# Configurações de Tela
LARGURA = 800
ALTURA = 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo da Nave")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)

# Carregar imagens
try:
    nave_img = pygame.image.load("nave.png")
    nave_img = pygame.transform.scale(nave_img, (80, 80))
    inimigo_img = pygame.image.load("inimigo.png")
    inimigo_img = pygame.transform.scale(inimigo_img, (80, 80))
    coracao_img = pygame.image.load("coracao.png")
    coracao_img = pygame.transform.scale(coracao_img, (30, 30))
    caveira_img = pygame.image.load("caveira.png")
    caveira_img = pygame.transform.scale(caveira_img, (30, 30))
    tela_inicial_img = pygame.image.load("tela_inicial.png")  # Imagem da tela inicial
    tela_inicial_img = pygame.transform.scale(tela_inicial_img, (LARGURA, ALTURA))  # Ajustando o tamanho para a tela
except Exception as e:
    print(f"Erro ao carregar imagens: {e}")
    sys.exit()

# Funções de Tela
def exibir_texto(texto, cor, tamanho, x, y):
    fonte = pygame.font.Font(None, tamanho)
    texto_surface = fonte.render(texto, True, cor)
    TELA.blit(texto_surface, (x, y))

def mostrar_instrucoes():
    TELA.fill(PRETO)
    exibir_texto("Instruções do Jogo", BRANCO, 40, LARGURA // 3, ALTURA // 6)
    exibir_texto("1. Controle a nave com as setas direcionais.", BRANCO, 30, LARGURA // 4, ALTURA // 3)
    exibir_texto("2. Atire com a tecla 'E'.", BRANCO, 30, LARGURA // 4, ALTURA // 2.5)
    exibir_texto("3. Destrua os inimigos e evite as colisões.", BRANCO, 30, LARGURA // 4, ALTURA // 2)
    exibir_texto("4. A cada 15 inimigos mortos, você sobe de nível.", BRANCO, 30, LARGURA // 4, ALTURA // 1.7)
    exibir_texto("5. Você começa com 3 vidas.", BRANCO, 30, LARGURA // 4, ALTURA // 1.5)
    exibir_texto("Pressione qualquer tecla para voltar ao menu.", BRANCO, 30, LARGURA // 4, ALTURA // 1.2)
    pygame.display.update()

    aguardando = True
    while aguardando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                aguardando = False
                menu_inicial()

def menu_inicial():
    TELA.blit(tela_inicial_img, (0, 0))  # Exibindo a imagem de fundo da tela inicial
    exibir_texto("Jogo da Nave", BRANCO, 50, LARGURA // 3, ALTURA // 4)
    exibir_texto("1. Iniciar Jogo", BRANCO, 30, LARGURA // 3, ALTURA // 2)
    exibir_texto("2. Instruções", BRANCO, 30, LARGURA // 3, ALTURA // 1.8)
    exibir_texto("3. Sair", BRANCO, 30, LARGURA // 3, ALTURA // 1.6)
    pygame.display.update()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print(f"Mouse clicado em: ({mouse_x}, {mouse_y})")  # Debug
                if LARGURA // 3 < mouse_x < LARGURA // 3 + 200 and ALTURA // 2 < mouse_y < ALTURA // 2 + 40:
                    iniciar_jogo()
                if LARGURA // 3 < mouse_x < LARGURA // 3 + 200 and ALTURA // 1.8 < mouse_y < ALTURA // 1.8 + 40:
                    mostrar_instrucoes()
                if LARGURA // 3 < mouse_x < LARGURA // 3 + 200 and ALTURA // 1.6 < mouse_y < ALTURA // 1.6 + 40:
                    pygame.quit()
                    sys.exit()

def iniciar_jogo():
    print("Iniciando o jogo...")  # Debug
    # Variáveis do Jogo
    nave_x, nave_y = LARGURA // 2, ALTURA - 100
    velocidade_nave = 5
    tiros = []
    inimigos = []
    nivel = 1
    kills = 0
    vidas = 3
    jogo_ativo = True

    # Flags para movimentação contínua
    mov_esq, mov_dir, mov_cima, mov_baixo = False, False, False, False

    # Variáveis para a animação do coração pulsando
    coração_tamanho = 30
    pulsando = True

    # Loop principal do Jogo
    while jogo_ativo:
        TELA.fill(PRETO)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    mov_esq = True
                if evento.key == pygame.K_RIGHT:
                    mov_dir = True
                if evento.key == pygame.K_UP:
                    mov_cima = True
                if evento.key == pygame.K_DOWN:
                    mov_baixo = True
                if evento.key == pygame.K_e:  # Tecla 'E' para atirar
                    tiros.append([nave_x + 35, nave_y])
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT:
                    mov_esq = False
                if evento.key == pygame.K_RIGHT:
                    mov_dir = False
                if evento.key == pygame.K_UP:
                    mov_cima = False
                if evento.key == pygame.K_DOWN:
                    mov_baixo = False

        # Movimentação contínua da nave
        if mov_esq:
            nave_x -= velocidade_nave
        if mov_dir:
            nave_x += velocidade_nave
        if mov_cima:
            nave_y -= velocidade_nave
        if mov_baixo:
            nave_y += velocidade_nave

        # Verificar limites da tela para a nave
        if nave_x < 0:
            nave_x = 0
        if nave_x > LARGURA - 80:
            nave_x = LARGURA - 80
        if nave_y < 0:
            nave_y = 0
        if nave_y > ALTURA - 80:
            nave_y = ALTURA - 80

        # Adicionar inimigos de forma controlada
        if len(inimigos) < 5:  # Limita a quantidade de inimigos na tela
            inimigos.append([random.randint(0, LARGURA - 80), -80])

        # Movimentação dos inimigos
        for inimigo in inimigos[:]:
            inimigo[1] += 5
            if inimigo[1] > ALTURA:
                inimigos.remove(inimigo)

            # Verificar colisão com os tiros
            for tiro in tiros[:]:
                if (inimigo[0] < tiro[0] < inimigo[0] + 80 and
                        inimigo[1] < tiro[1] < inimigo[1] + 80):
                    inimigos.remove(inimigo)
                    tiros.remove(tiro)
                    kills += 1
                    break

            # Verificar colisão com a nave
            if (nave_x < inimigo[0] < nave_x + 80 and
                    nave_y < inimigo[1] < nave_y + 80):
                vidas -= 1
                inimigos.remove(inimigo)

        # Desenhar elementos na tela
        TELA.blit(nave_img, (nave_x, nave_y))

        for tiro in tiros[:]:
            tiro[1] -= 10  # Movimento do tiro para cima
            pygame.draw.rect(TELA, VERDE, (tiro[0], tiro[1], 5, 10))
            if tiro[1] < 0:  # Se o tiro sair da tela, remove ele
                tiros.remove(tiro)

        for inimigo in inimigos:
            TELA.blit(inimigo_img, (inimigo[0], inimigo[1]))

        # Animação do coração pulsando
        if pulsando:
            coração_tamanho += 2
            if coração_tamanho > 35:
                pulsando = False
        else:
            coração_tamanho -= 2
            if coração_tamanho < 25:
                pulsando = True
        
        # Exibir três corações no canto superior esquerdo, com animação pulsante
        for i in range(vidas):  # Exibir um coração para cada vida
            coracao_img_pulsando = pygame.transform.scale(coracao_img, (coração_tamanho, coração_tamanho))
            TELA.blit(coracao_img_pulsando, (10 + (i * 35), 10))

        # Exibir a contagem de kills com a imagem da caveira
        TELA.blit(caveira_img, (LARGURA - 180, 10))
        exibir_texto(f"{kills}", BRANCO, 30, LARGURA - 130, 10)

        # Exibir o nível
        if kills >= 15 * nivel:  # A cada 15 kills, sobe de nível
            nivel += 1
        exibir_texto(f"Nível {nivel}", BRANCO, 30, LARGURA // 2 - 50, 10)

        # Verificar fim de jogo
        if vidas <= 0:
            jogo_ativo = False
            game_over()

        pygame.display.update()
        pygame.time.Clock().tick(60)

def game_over():
    print("Game Over")  # Debug
    TELA.fill(PRETO)
    exibir_texto("Game Over", VERMELHO, 50, LARGURA // 3, ALTURA // 3)
    exibir_texto("Pressione R para voltar ao menu", BRANCO, 30, LARGURA // 4, ALTURA // 2)
    pygame.display.update()

    aguardando = True
    while aguardando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                aguardando = False
                menu_inicial()

# Iniciar menu inicial
menu_inicial()

