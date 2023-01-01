
import sys
import random


class Pedra():
    instancias = []
    def __init__(self, pedra_nome, pedra_dono_inicial):
        self.pedra_dono_inicial = pedra_dono_inicial
        self.pedra_dono = pedra_dono_inicial
        self.pedra_nome = pedra_nome
        self.pedra_ocupando_casa = ""
        self.__class__.instancias.append(self)

    def pedra_ocupar_casa(self, casa):
        self.pedra_ocupando_casa = casa
        casa.casa_se_ocupar(pedra = self)

    def pedra_se_mudar(self, casa_antiga, casa_nova):
        self.pedra_ocupar_casa(casa = casa_nova)
        casa_nova.casa_se_ocupar(pedra = self)
        casa_antiga.casa_se_desocupar()

    def pedra_dono_novo(self, dono_novo):
        self.pedra_dono = dono_novo
        self.pedra_ocupando_casa = ""

    def __str__(self):
        return self.pedra_nome
                

class Casa():
    instancias = []
    def __init__(self, casa_x, casa_y):
        self.casa_x = casa_x
        self.casa_y = casa_y
        self.casa_nome = ""
        self.casa_ocupada = ""
        self.casa_ocupavel = ""
        self.__class__.instancias.append(self)

    def casa_se_desocupar(self):
        self.casa_ocupada = "nao"

    def casa_se_ocupar(self, pedra):
        self.casa_ocupada = pedra

    def casa_nomear(self):
        self.casa_nome = str(self.casa_x)+"_"+str(self.casa_y)
    
    def __str__(self):
        return self.casa_nome

    @staticmethod
    def casas_pedras(casas):
        c = []
        for i in casas:
            if i != "False":
                c.append(i.casa_ocupada)
            else:
                c.append("False")
        return c


    @staticmethod
    def casas_nomes(casas_nomes):
        a = list(i.casa_nome for i in Casa.instancias)
        b = []
        for i in casas_nomes:
            if i in a:
                b.append(i)
            else:
                b.append("False")
        return b

    @staticmethod
    def casas_nomes_casas(casas_nomes):
        a = list(i.casa_nome for i in Casa.instancias)
        b = []
        d = []
        for i in casas_nomes:
            if i in a:
                b.append(i)
            else:
                b.append("False")
        for j in b:
            for k in Casa.instancias:
                if k.casa_nome==j:
                    d.append(k)
            if j=="False":
                d.append("False")      
        return d

    @staticmethod
    def casas_nomes_pedras(casas_nomes):
        casas_n = Casa.casas_nomes_casas(casas_nomes)
        a = []
        for i in casas_n:
            if i != "False":
                b = i.casa_ocupada
                a.append(b)
            else:
                a.append("False")
        return a


class Tabuleiro():
    instancias = []
    def __init__(self, tabuleiro_largura, tabuleiro_altura):
        self.tabuleiro_largura = tabuleiro_largura
        self.tabuleiro_altura = tabuleiro_altura
        self.tabuleiro_casas = []
        self.tabuleiro_casas_ocupaveis = ""
        self.tabuleiro_casas_nao_ocupaveis = ""
        self.__class__.instancias.append(self)

    def tabuleiro_casas_ocupaveis_vazias(self):
        aa = self.tabuleiro_casas_vazias()
        a = list(i for i in aa if i.casa_ocupavel == "sim")
        return a

    def tabuleiro_casas_ocupaveis_vazias_nomes(self):
        aa = self.tabuleiro_casas_ocupaveis_vazias()
        a = list(i.casa_nome for i in aa)
        return a

    def tabuleiro_casas_nomes(self):
        return list(i.casa_nome for i in self.tabuleiro_casas)
    
    def tabuleiro_casas_vazias(self):
        return list(i for i in self.tabuleiro_casas if i.casa_ocupada == "nao")

    def tabuleiro_casas_vazias_nomes(self):
        return list(i.casa_nome for i in self.tabuleiro_casas if i.casa_ocupada == "nao")

    def tabuleiro_casas_criar(self):
        for altura in range(1, self.tabuleiro_altura +1):
            for largura in range(1, self.tabuleiro_largura +1):
                casa = Casa(casa_x = largura, casa_y = altura)
                casa.casa_nomear()
                casa.casa_se_desocupar()
                a = bool(largura%2)
                b = bool(altura%2)
                if a==b:
                    casa.casa_ocupavel = "sim"
                else:
                    casa.casa_ocupavel = "nao"
                self.tabuleiro_casas.append(casa)
        self.tabuleiro_casas_ocupaveis_criar()
        self.tabuleiro_casas_nao_ocupaveis_criar()
        
    def tabuleiro_casas_ocupaveis_criar(self,):   
        self.tabuleiro_casas_ocupaveis = list(i for i in self.tabuleiro_casas if i.casa_ocupavel == "sim" )

    def tabuleiro_casas_nao_ocupaveis_criar(self,):   
        self.tabuleiro_casas_nao_ocupaveis = list(i for i in self.tabuleiro_casas if i.casa_ocupavel == "nao")


class Jogador():
    instancias = []
    def __init__(self, jogador_nome, jogador_pedras_quantidade, jogador_movimento_y):
        self.jogador_nome = jogador_nome
        self.jogador_pedras_quantidade = jogador_pedras_quantidade
        self.jogador_pedras = []
        self.jogador_pedras_capturadas = []
        self.jogador_movimento_y = jogador_movimento_y
        self.__class__.instancias.append(self)

    def jogador_pedras_criar(self):
        for i in range(1, self.jogador_pedras_quantidade +1):
            jogador_pedra = Pedra(pedra_nome = str(self.jogador_nome+"_"+str(i)), pedra_dono_inicial = self)
            self.jogador_pedras.append(jogador_pedra)

    def jogador_pedra_posicionar(self, pedra, casa):
        pedra.pedra_ocupar_casa(casa)
    
    def jogador_pedras_casas_nomes(self):
        return list(i.pedra_ocupando_casa.casa_nome for i in self.jogador_pedras)
    
    def jogador_pedras_casas(self):
        return list(i.pedra_ocupando_casa for i in self.jogador_pedras)

    def jogador_buscar_pedra_capturar(self, tabuleiro, adversario):
        jogador_pedras_casas_nomes = self.jogador_pedras_casas_nomes()
        adversario_pedras_casas_nomes = adversario.jogador_pedras_casas_nomes()
        tabuleiro_casas_nomes = tabuleiro.tabuleiro_casas_nomes()
        tabuleiro_casas_vazias_nomes = tabuleiro.tabuleiro_casas_vazias_nomes() 
        tabuleiro_casas_ocupaveis_vazias = tabuleiro.tabuleiro_casas_ocupaveis_vazias()
        jogadas_captura = []
        for pedra in self.jogador_pedras:
            print(pedra.pedra_nome)
            print(pedra.pedra_ocupando_casa)
            casa = pedra.pedra_ocupando_casa
            x = casa.casa_x
            y = casa.casa_y
            d1 = [f"{x}_{y}", f"{x+1}_{y+1}", f"{x+2}_{y+2}"]
            d2 = [f"{x}_{y}", f"{x-1}_{y+1}", f"{x-2}_{y+2}"]
            d3 = [f"{x}_{y}", f"{x-1}_{y-1}", f"{x-2}_{y-2}"]
            d4 = [f"{x}_{y}", f"{x+1}_{y-1}", f"{x+2}_{y-2}"]
            print(d1,d2,d3,d4)
            casas_01 = Casa.casas_nomes_casas(casas_nomes=d1)
            casas_02 = Casa.casas_nomes_casas(casas_nomes=d2)
            casas_03 = Casa.casas_nomes_casas(casas_nomes=d3)
            casas_04 = Casa.casas_nomes_casas(casas_nomes=d4)
            a = casas_01+casas_02+casas_03+casas_04

            pedras_01 = Casa.casas_pedras(casas=casas_01)
            pedras_02 = Casa.casas_pedras(casas=casas_02)
            pedras_03 = Casa.casas_pedras(casas=casas_03)
            pedras_04 = Casa.casas_pedras(casas=casas_04)
            b = pedras_01+pedras_02+pedras_03+pedras_04
            for i in b:
                print(i)
            jogadas = [casas_01+pedras_01, casas_02+pedras_02, casas_03+pedras_03, casas_04+pedras_04]
            """
            print(jogadas)
            
            for i in a:
                if i!=False:
                    print(i.casa_ocupada)
            """
            """
            b = d1+d2+d3+d4
            for i in b:
                print(i)
            """
            #print(casas_01)
            #print(casas_02)
            #print(casas_03)
            #print(casas_04)
            #pedras_01 = Casa.casas_nomes_pedras(d1)#Casa.casas_pedras(casas_01)
            #pedras_02 = Casa.casas_nomes_pedras(d2)#Casa.casas_pedras(casas_02)
            #pedras_03 = Casa.casas_nomes_pedras(d3)#Casa.casas_pedras(casas_03)
            #pedras_04 = Casa.casas_nomes_pedras(d4)#Casa.casas_pedras(casas_04)
            #print(pedras_01)
            #print(pedras_02)
            #print(pedras_03)
            #print(pedras_04)
            #print(jogadas)
            """
            pedras_01 = [pedra, pedra, pedra, pedra]
            pedras_02 = Casa.casas_pedras(casas_02)
            pedras_03 = Casa.casas_pedras(casas_03)
            #k = list(zip(casas_01, casas_02, casas_03, pedras_01, pedras_02, pedras_03))
            kk = list(zip(casas_01,casas_02,casas_03))
            for i in kk:
                print(i[0],i[1],i[2])
            print("oi"*20)

                #print(i[0],i[1],i[2],i[3],i[4],i[5])
            """
        return []
    

    def jogador_buscar_pedra_mover(self, tabuleiro, adversario):
        jogador_pedras_casas_nomes = self.jogador_pedras_casas_nomes()
        adversario_pedras_casas_nomes = adversario.jogador_pedras_casas_nomes()
        tabuleiro_casas_nomes = tabuleiro.tabuleiro_casas_nomes()
        tabuleiro_casas_vazias_nomes = tabuleiro.tabuleiro_casas_vazias_nomes() 
        tabuleiro_casas_ocupaveis_vazias_nomes = tabuleiro.tabuleiro_casas_ocupaveis_vazias_nomes() 

        
        """
            print("jogador: (pedra.nome em casa.nome)")
            print(len(jogador_pedras_casas_nomes))
            print(list(zip(list(i.pedra_nome for i in self.jogador_pedras), jogador_pedras_casas_nomes)))

            print("adversario (pedra.nome em casa.nome)")
            print(len(adversario_pedras_casas_nomes))
            print(list(zip( list(i.pedra_nome for i in adversario.jogador_pedras), adversario_pedras_casas_nomes)))

            print("tabuleiro_casas_nomes")
            print(len(tabuleiro_casas_nomes))
            print(tabuleiro_casas_nomes)

            print("tabuleiro_casas_vazias_nomes")
            print(len(tabuleiro_casas_vazias_nomes))
            print(tabuleiro_casas_vazias_nomes)

            print("tabuleiro_casas_ocupaveis_vazias_nomes")
            print(len(tabuleiro_casas_ocupaveis_vazias_nomes))
            print(tabuleiro_casas_ocupaveis_vazias_nomes)
        """

        while True:
            jogar_da_casa_nome = input("jogada da casa x_y: ")  
            if jogar_da_casa_nome not in tabuleiro_casas_nomes:
                print("Casa não existe no tabuleiro!")
            elif jogar_da_casa_nome in adversario_pedras_casas_nomes:
                print("Pedra do adversário!")
            elif jogar_da_casa_nome in tabuleiro_casas_vazias_nomes:
                print("Casa vazia!") 
            elif jogar_da_casa_nome in jogador_pedras_casas_nomes:
                jogar_da_casa_executar = list({i for i in tabuleiro.tabuleiro_casas if i.casa_nome==jogar_da_casa_nome})[0]
                a, b, c = jogar_da_casa_executar.casa_x + 1, jogar_da_casa_executar.casa_x-1, jogar_da_casa_executar.casa_y + self.jogador_movimento_y
                d = [f"{a}_{c}", f"{b}_{c}"]
                e = list(i for i in d if i in tabuleiro_casas_ocupaveis_vazias_nomes)
                if len(e)>0:
                    print(jogar_da_casa_nome)
                    break
                else:
                    print("Não é possível mover essa sua peça!")

        
        while True:
            jogar_para_casa_nome = input("jogada para a casa x_y: ")
            if jogar_para_casa_nome not in e:
                print(e)
                if jogar_para_casa_nome not in tabuleiro_casas_nomes:
                    print("Casa não existe no tabuleiro!")
                elif jogar_para_casa_nome in adversario_pedras_casas_nomes:
                    print("Casa ocupada por uma pedra do adversário!") 
                elif jogar_para_casa_nome in tabuleiro.tabuleiro_casas_nao_ocupaveis:
                    print("Nenhuma pedra pode ficar nessa casa!")
            else:
                print(jogar_para_casa_nome)
                pedra_escolhida_executar = list({i for i in self.jogador_pedras if i.pedra_ocupando_casa.casa_nome==jogar_da_casa_nome})[0]
                break

        jogar_para_casa_executar = list({i for i in tabuleiro.tabuleiro_casas if i.casa_nome==jogar_para_casa_nome})[0] 

        self.jogador_pedra_mover(
            pedra=pedra_escolhida_executar, 
            jogar_da_casa=jogar_da_casa_executar, 
            jogar_para_casa=jogar_para_casa_executar
        )


    def jogador_vez(self, tabuleiro, adversario):
        print(self.jogador_nome)
        jogadas_captura = self.jogador_buscar_pedra_capturar(tabuleiro = tabuleiro, adversario=adversario)
        if not len(jogadas_captura) > 0:
            self.jogador_buscar_pedra_mover(tabuleiro = tabuleiro, adversario=adversario)


    def jogador_pedra_mover(self, pedra, jogar_da_casa, jogar_para_casa):
        pedra.pedra_se_mudar(casa_antiga=jogar_da_casa, casa_nova=jogar_para_casa)

    def jogador_pedra_capturar(self, pedra_capturada, pedra_casa):
        for i in pedra_casa:
            i.casa_se_desocupar()
        self.jogador_pedras_capturadas.append(pedra_capturada)
        pedra_capturada.pedra_dono_novo(dono_novo=self)


class Damas():
    instancias = []
    def __init__(self):           
        self.damas_jogadores = self.damas_jogadores_criar()
        self.damas_tabuleiro = self.damas_tabuleiro_criar()
        self.damas_pedras_posicionar(jogadores=self.damas_jogadores, tabuleiro=self.damas_tabuleiro)
        self.__class__.instancias.append(self)


    def damas_iniciar(self):
        while True:
            vez = [[0,1],[1,0]]
            for i in vez:
                jogando = self.damas_jogadores[i[0]]
                adversario = self.damas_jogadores[i[1]]
                jogando.jogador_vez(tabuleiro = self.damas_tabuleiro, adversario = adversario)

         
    def damas_jogadores_criar(self):
        jogadores = []
        jogadores_quantidade = 2
        jogador_pedras_quantidade = 12
        movimentos_y = [1,-1]
        for i in range(jogadores_quantidade):
            jogador = Jogador(
                jogador_nome = "jogador_"+str(i+1), 
                jogador_pedras_quantidade = jogador_pedras_quantidade, 
                jogador_movimento_y = movimentos_y[i]
            )
            jogador.jogador_pedras_criar()
            jogadores.append(jogador)
        return jogadores

    def damas_tabuleiro_criar(self):
        tabuleiro_altura = 8
        tabuleiro_largura = 8
        tabuleiro = Tabuleiro(
            tabuleiro_altura = tabuleiro_altura, 
            tabuleiro_largura = tabuleiro_largura
        )
        tabuleiro.tabuleiro_casas_criar()
        return tabuleiro

    def damas_pedras_posicionar(self, jogadores, tabuleiro):
        jogador_1 = jogadores[0]
        jogador_2 = jogadores[1]
        for i in range(len(jogador_1.jogador_pedras)):
            pedra = jogador_1.jogador_pedras[i]
            casa = tabuleiro.tabuleiro_casas_ocupaveis[i]
            jogador_1.jogador_pedra_posicionar(pedra=pedra, casa=casa)

        for i in range(len(jogador_2.jogador_pedras)):
            pedra = jogador_2.jogador_pedras[i]
            casa = tabuleiro.tabuleiro_casas_ocupaveis[len(tabuleiro.tabuleiro_casas_ocupaveis)-1-i]
            jogador_2.jogador_pedra_posicionar(pedra=pedra, casa=casa)


jogo = Damas()
jogo.damas_iniciar()
