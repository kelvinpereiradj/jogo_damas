
import sys
import random


class Pedra():
    def __init__(self, nome, pedra_dono_inicial):
        self.pedra_dono_inicial = pedra_dono_inicial
        self.pedra_dono = pedra_dono_inicial
        self.nome = nome
        self.pedra_ocupando_casa = None

    def pedra_ocupar_casa(self, casa):
        self.pedra_ocupando_casa = casa
        casa.casa_se_ocupar(pedra = self)

    def pedra_se_mudar(self, casa_antiga, casa_nova):
        self.pedra_ocupar_casa(casa = casa_nova)
        casa_antiga.casa_se_desocupar()
        casa_nova.casa_se_ocupar(pedra = self)
    

class Casa():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.nome = None
        self.casa_ocupada = None 
        self.casa_ocupavel = None

    def casa_se_desocupar(self):
        self.casa_ocupada = None

    def casa_se_ocupar(self, pedra):
        self.casa_ocupada = pedra

    def casa_nomear(self):
        self.nome = str(self.x)+"_"+str(self.y)

class Tabuleiro():
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.casas = []
        self.casas_ocupaveis = None
        self.casas_nao_ocupaveis = None

    def casas_ocupaveis_vazias(self):
        aa = self.casas_vazias()
        a = list(i for i in aa if i.casa_ocupavel == True)
        return a

    def casas_ocupaveis_vazias_nomes(self):
        aa = self.casas_ocupaveis_vazias()
        a = list(i.nome for i in aa)
        return a

    def casas_nomes(self):
        return list(i.nome for i in self.casas)
    
    def casas_vazias(self):
        return list(i for i in self.casas if i.casa_ocupada == None)

    def casas_vazias_nomes(self):
        return list(i.nome for i in self.casas if i.casa_ocupada == None)

    def casas_criar(self):
        for altura in range(1, self.altura +1):
            for largura in range(1, self.largura +1):
                casa = Casa(x = largura, y = altura)
                casa.casa_nomear()
                casa.casa_se_desocupar()
                a = bool(largura%2)
                b = bool(altura%2)
                if a==b:
                    casa.casa_ocupavel = True
                else:
                    casa.casa_ocupavel = False
                self.casas.append(casa)
        self.casas_ocupaveis_criar()
        self.casas_nao_ocupaveis_criar()
        
    def casas_ocupaveis_criar(self,):   
        self.casas_ocupaveis = list(i for i in self.casas if i.casa_ocupavel == True )

    def casas_nao_ocupaveis_criar(self,):   
        self.casas_nao_ocupaveis = list(i for i in self.casas if i.casa_ocupavel == False)

class Jogador():
    def __init__(self, nome, pedras_quantidade, movimento_y):
        self.nome = nome
        self.pedras_quantidade = pedras_quantidade
        self.pedras = []
        self.movimento_y = movimento_y

    def pedras_criar(self):
        for i in range(1, self.pedras_quantidade +1):
            pedra = Pedra(nome = self.nome+"_"+str(i), pedra_dono_inicial = self)
            self.pedras.append(pedra)

    def pedra_posicionar(self, pedra, casa):
        pedra.pedra_ocupar_casa(casa)
    
    def jogador_pedras_casas_nomes(self):
        return list(i.pedra_ocupando_casa.nome for i in self.pedras)

    def jogador_vez(self, tabuleiro, adversario):
        print(self.nome)
        jogador_pedras_casas_nomes = self.jogador_pedras_casas_nomes()
        adversario_pedras_casas_nomes = adversario.jogador_pedras_casas_nomes()
        tabuleiro_casas_nomes = tabuleiro.casas_nomes()
        tabuleiro_casas_vazias_nomes = tabuleiro.casas_vazias_nomes() 
        tabuleiro_casas_ocupaveis_vazias_nomes = tabuleiro.casas_ocupaveis_vazias_nomes() 

        

        print("jogador: (pedra.nome em casa.nome)")
        print(len(jogador_pedras_casas_nomes))
        print(list(zip( list(i.nome for i in self.pedras), jogador_pedras_casas_nomes)))

        print("adversario (pedra.nome em casa.nome)")
        print(len(adversario_pedras_casas_nomes))
        print(list(zip( list(i.nome for i in adversario.pedras), adversario_pedras_casas_nomes)))

        print("tabuleiro_casas_nomes")
        print(len(tabuleiro_casas_nomes))
        print(tabuleiro_casas_nomes)

        print("tabuleiro_casas_vazias_nomes")
        print(len(tabuleiro_casas_vazias_nomes))
        print(tabuleiro_casas_vazias_nomes)

        print("tabuleiro_casas_ocupaveis_vazias_nomes")
        print(len(tabuleiro_casas_ocupaveis_vazias_nomes))
        print(tabuleiro_casas_ocupaveis_vazias_nomes)


        while True:
            jogar_da_casa_nome = input("jogada da casa x_y: ")  
            if jogar_da_casa_nome not in tabuleiro_casas_nomes:
                print("Casa não existe no tabuleiro!")
            elif jogar_da_casa_nome in adversario_pedras_casas_nomes:
                print("Pedra do adversário!")
            elif jogar_da_casa_nome in tabuleiro_casas_vazias_nomes:
                print("Casa vazia!") 
            elif jogar_da_casa_nome in jogador_pedras_casas_nomes:
                jogar_da_casa_executar = list({i for i in tabuleiro.casas if i.nome==jogar_da_casa_nome})[0]
                a, b, c = jogar_da_casa_executar.x + 1, jogar_da_casa_executar.x-1, jogar_da_casa_executar.y + self.movimento_y
                print(a, b, c)
                d = [f"{a}_{c}", f"{b}_{c}"]
                print(d)
                e = list(i for i in d if i in tabuleiro_casas_ocupaveis_vazias_nomes)
                print(e)
                if len(e)>0:
                    print(jogar_da_casa_nome)
                    break
                else:
                    print("Não é possível mover essa sua peça!")

        
        while True:
            jogar_para_casa_nome = input("jogada para a casa x_y: ")
            if jogar_para_casa_nome not in e:
                if jogar_para_casa_nome not in tabuleiro_casas_nomes:
                    print("Casa não existe no tabuleiro!")
                elif jogar_para_casa_nome in adversario_pedras_casas_nomes:
                    print("Casa ocupada por uma pedra do adversário!") 
                elif jogar_para_casa_nome in tabuleiro.casas_nao_ocupaveis:
                    print("Nenhuma pedra pode ficar nessa casa!")
            else:
                print(jogar_para_casa_nome)
                break


        pedra_escolhida_executar = list({i for i in self.pedras if i.pedra_ocupando_casa.nome==jogar_da_casa_nome})[0]
        jogar_para_casa_executar = list({i for i in tabuleiro.casas if i.nome==jogar_para_casa_nome})[0] 

        self.jogador_pedra_mover(
            pedra=pedra_escolhida_executar, 
            jogar_da_casa=jogar_da_casa_executar, 
            jogar_para_casa=jogar_para_casa_executar
        )

    def jogador_pedra_mover(self, pedra, jogar_da_casa, jogar_para_casa):
        pedra.pedra_se_mudar(casa_antiga=jogar_da_casa, casa_nova=jogar_para_casa)


    def pedra_capturar(self):
        return str("pedra_capturar")








def jogadores_criar():
    jogadores = []
    a = 0
    while a<2:
        a += 1
        if a == 1:
            y = 1
        else:
            y = -1
        jogador = Jogador(nome = "jogador_"+str(a), pedras_quantidade = 12, movimento_y = y)
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
        casa = tabuleiro.casas_ocupaveis[i]
        jogador_1.pedra_posicionar(pedra=pedra, casa=casa)

    for i in range(len(jogador_2.pedras)):
        pedra = jogador_2.pedras[i]
        casa = tabuleiro.casas_ocupaveis[len(tabuleiro.casas_ocupaveis)-1-i]
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
