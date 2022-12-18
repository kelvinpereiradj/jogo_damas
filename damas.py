
import sys
import random


class Pedra():
    def __init__(self, nome, pedra_dono_inicial):
        self.pedra_dono_inicial = pedra_dono_inicial
        self.pedra_dono = pedra_dono_inicial
        self.nome = nome
        self.pedra_ocupando_casa = "nao"

    def pedra_ocupar_casa(self, casa):
        self.pedra_ocupando_casa = casa
        casa.casa_se_ocupar(pedra = self)

    def pedra_se_mudar(self, casa_antiga, casa_nova):
        self.pedra_ocupar_casa(casa = casa_nova)
        casa_antiga.casa_se_desocupar()
        casa_nova.casa_se_ocupar(pedra = self)
    
    def __str__(self):
        return str(self.nome)

class Casa():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.nome = "nao"
        self.casa_ocupada = "nao" 

    def casa_se_desocupar(self):
        self.casa_ocupada = "nao"

    def casa_se_ocupar(self, pedra):
        self.casa_ocupada = pedra

    def casa_nomear(self):
        self.nome = str(self.x)+"_"+str(self.y)

    def __str__(self):
        return str(self.nome)

class Tabuleiro():
    def __init__(self, altura, largura):
        self.altura = altura
        self.largura = largura
        self.casas = []

    def casas_criar(self):
        for i in range(1, self.altura +1):
            for j in range(1, self.largura +1):
                casa = Casa(x = i, y = j)
                casa.casa_nomear()
                casa.casa_se_desocupar()
                self.casas.append(casa)


class Jogador():
    def __init__(self, nome, pedras_quantidade):
        self.nome = nome
        self.pedras_quantidade = pedras_quantidade
        self.pedras = []

    def pedras_criar(self):
        for i in range(1, self.pedras_quantidade +1):
            pedra = Pedra(nome = self.nome+"_"+str(i), pedra_dono_inicial = self)
            self.pedras.append(pedra)

    def pedra_posicionar(self, pedra, casa):
        pedra.pedra_ocupar_casa(casa)
    
    def jogador_vez(self, tabuleiro, adversario):
        print(self.nome)
        jogador_pedras_casas = list(i.pedra_ocupando_casa.nome for i in self.pedras)
        adversario_pedras_casas = list(i.pedra_ocupando_casa.nome for i in adversario.pedras)
        tabuleiro_casas = list(i.nome for i in tabuleiro.casas)
        tabuleiro_casas_vazias = list(i.nome for i in tabuleiro.casas if i.casa_ocupada == "nao")

        

        print("jogador_pedras_casas")
        print(list(zip( list(i.nome for i in self.pedras), jogador_pedras_casas)))
        print("adversario_pedras_casas")
        print(list(zip( list(i.nome for i in adversario.pedras), adversario_pedras_casas)))
        print("tabuleiro_casas")
        print(len(tabuleiro_casas))
        print(tabuleiro_casas)
        print("tabuleiro_casas_vazias")
        print(len(tabuleiro_casas_vazias))
        print(tabuleiro_casas_vazias)

        while True:
            jogar_da_casa = input("jogada da casa x_y: ")   
            if jogar_da_casa in jogador_pedras_casas:
                print(jogar_da_casa)
                break
            elif jogar_da_casa not in tabuleiro_casas:
                print("Casa não existe no tabuleiro!")
            elif jogar_da_casa in adversario_pedras_casas:
                print("Pedra do adversário!")
            elif jogar_da_casa in tabuleiro_casas_vazias:
                print("Casa vazia!")

        
        while True:
            jogar_para_casa = input("jogada para a casa x_y: ")
            if jogar_para_casa in jogador_pedras_casas:
                print("Casa ocupada por outra pedra sua!")
            elif jogar_para_casa not in tabuleiro_casas:
                print("Casa não existe no tabuleiro!")
            elif jogar_para_casa in adversario_pedras_casas:
                print("Casa ocupada por uma pedra do adversário!")
            elif jogar_para_casa in tabuleiro_casas_vazias:
                print(jogar_para_casa)
                break


        pedra_escolhida = list({i for i in self.pedras if i.pedra_ocupando_casa.nome==jogar_da_casa})[0]
        jogar_da_casa = list({i for i in tabuleiro.casas if i.nome==jogar_da_casa})[0]
        jogar_para_casa = list({i for i in tabuleiro.casas if i.nome==jogar_para_casa})[0] 

        self.jogador_pedra_mover(pedra=pedra_escolhida, jogar_da_casa=jogar_da_casa, jogar_para_casa=jogar_para_casa)

    def jogador_pedra_mover(self, pedra, jogar_da_casa, jogar_para_casa):
        pedra.pedra_se_mudar(casa_antiga=jogar_da_casa, casa_nova=jogar_para_casa)

    def __str__(self):
        return str(self.nome)

def jogadores_criar():
    jogadores = []
    a = 0
    while a<2:
        a += 1
        jogador = Jogador(nome = "jogador_"+str(a), pedras_quantidade = 16)
        jogador.pedras_criar()
        jogadores.append(jogador)
    return jogadores

def tabuleiro_criar():
    tabuleiro = Tabuleiro(altura=8, largura=8)
    tabuleiro.casas_criar()
    return tabuleiro


def pedras_posicionar(jogadores, tabuleiro):
    jogador_1 = jogadores[0]
    jogador_2 = jogadores[1]
    for i in range(len(jogador_1.pedras)):
        pedra = jogador_1.pedras[i]
        casa = tabuleiro.casas[i]
        jogador_1.pedra_posicionar(pedra=pedra, casa=casa)

    for i in range(len(jogador_2.pedras)):
        pedra = jogador_2.pedras[i]
        casa = tabuleiro.casas[len(tabuleiro.casas)-1-i]
        jogador_2.pedra_posicionar(pedra=pedra, casa=casa)

def jogo_carregar():
    jogadores = jogadores_criar()
    tabuleiro = tabuleiro_criar()
    pedras_posicionar(jogadores=jogadores, tabuleiro=tabuleiro)
    while True:
        vez = [[0,1],[1,0]]
        for i in vez:
            jogando = jogadores[i[0]]
            adversario = jogadores[i[1]]
            jogando.jogador_vez(tabuleiro = tabuleiro, adversario = adversario)
    """
    while True:
        for i in jogadores:
            i.escrever()
    
    for i in tabuleiro.casas:
        print(i.nome)
        print(i)
    for j in jogadores:
        for k in j.pedras:

            print(k.nome)
            print(k)
            print(k.pedra_dono)
            print(k.pedra_ocupando_casa)
    """
jogo_carregar()
