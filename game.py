import pygame
import sys
import random

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
AMARELO = (255, 255, 0)

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
    fruta_img = pygame.image.load("fruta.png")  # Adicione a imagem da fruta
    fruta_img = pygame.transform.scale(fruta_img, (40, 40))  # Ajuste o tamanho da fruta
except Exception as e:
    print(f"Erro ao carregar imagens: {e}")
    sys.exit()

# Funções de Tela
def exibir_texto(texto, cor, tamanho, x, y):
    fonte = pygame.font.Font(None, tamanho)
    texto_surface = fonte.render(texto, True, cor)
    TELA.blit(texto_surface, (x, y))

# Função para mostrar instruções
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

# Função para o menu inicial
def menu_inicial():
    TELA.fill(PRETO)
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
                if LARGURA // 3 < mouse_x < LARGURA // 3 + 200 and ALTURA // 2 < mouse_y < ALTURA // 2 + 40:
                    iniciar_jogo()
                if LARGURA // 3 < mouse_x < LARGURA // 3 + 200 and ALTURA // 1.8 < mouse_y < ALTURA // 1.8 + 40:
                    mostrar_instrucoes()
                if LARGURA // 3 < mouse_x < LARGURA // 3 + 200 and ALTURA // 1.6 < mouse_y < ALTURA // 1.6 + 40:
                    pygame.quit()
                    sys.exit()

# Função para iniciar o jogo
def iniciar_jogo():
    nave_x, nave_y = LARGURA // 2, ALTURA - 100
    velocidade_nave = 5
    tiros = []
    inimigos = []
    frutas = []  # Lista para armazenar as frutas
    nivel = 1
    kills = 0
    vidas = 3
    jogo_ativo = True

    # Loop principal do Jogo
    while jogo_ativo:
        TELA.fill(PRETO)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    nave_x -= velocidade_nave
                if evento.key == pygame.K_RIGHT:
                    nave_x += velocidade_nave
                if evento.key == pygame.K_UP:
                    nave_y -= velocidade_nave
                if evento.key == pygame.K_DOWN:
                    nave_y += velocidade_nave
                if evento.key == pygame.K_e:  # Tecla 'E' para atirar
                    tiros.append([nave_x + 35, nave_y])

        # Verificar limites da tela para a nave
        if nave_x < 0:
            nave_x = 0
        if nave_x > LARGURA - 80:
            nave_x = LARGURA - 80
        if nave_y < 0:
            nave_y = 0
        if nave_y > ALTURA - 80:
            nave_y = ALTURA - 80

        # Movimentação dos tiros
        for tiro in tiros[:]:
            tiro[1] -= 10
            if tiro[1] < 0:
                tiros.remove(tiro)

        # Adicionar inimigos (simples exemplo)
        if len(inimigos) < 5:
            inimigos.append([random.randint(0, LARGURA - 80), -80])

        # Adicionar frutas com probabilidade baixa (10%)
        if random.random() < 0.01 and len(frutas) < 1:  # Apenas uma fruta pode aparecer de cada vez
            frutas.append([random.randint(0, LARGURA - 40), -40])

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

        # Movimentação das frutas
        for fruta in frutas[:]:
            fruta[1] += 5  # Velocidade da fruta
            if fruta[1] > ALTURA:
                frutas.remove(fruta)

            # Verificar colisão com a nave
            if (nave_x < fruta[0] < nave_x + 80 and
                    nave_y < fruta[1] < nave_y + 80):
                vidas += 1  # Cura 1 vida
                frutas.remove(fruta)

        # Desenhar elementos na tela
        TELA.blit(nave_img, (nave_x, nave_y))

        for tiro in tiros:
            pygame.draw.rect(TELA, VERDE, (tiro[0], tiro[1], 5, 10))

        for inimigo in inimigos:
            TELA.blit(inimigo_img, (inimigo[0], inimigo[1]))

        for fruta in frutas:
            TELA.blit(fruta_img, (fruta[0], fruta[1]))

        # Exibir informações
        exibir_texto(f"Vidas: {vidas}", BRANCO, 30, 10, 10)
        exibir_texto(f"Kills: {kills}", BRANCO, 30, 10, 50)
        exibir_texto(f"Nível {nivel}", BRANCO, 30, 10, 90)

        if kills >= 15:
            nivel = 2
        if kills >= 30:
            nivel = 3
        if kills >= 45:
            nivel = 4

        pygame.display.update()

        if vidas <= 0:
            jogo_ativo = False
            game_over()

        pygame.time.Clock().tick(60)

# Tela de Game Over
def game_over():
    TELA.fill(PRETO)
    exibir_texto("Game Over", VERMELHO, 50, LARGURA // 3, ALTURA // 3)
    exibir_texto("Pressione qualquer tecla para reiniciar", BRANCO, 30, LARGURA // 3, ALTURA // 2)
    pygame.display.update()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                iniciar_jogo()

menu_inicial()
