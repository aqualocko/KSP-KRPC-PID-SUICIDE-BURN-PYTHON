# -*- coding: utf-8 -*-
'''
==========Controlador PID =================
-Codigo Traduzido de Java para Python
- Arquivo auxiliar Ao SB.py
- Traduzido e aprimorador Por Maurício Mazur
'''
import time
universal = float()
valorEntrada = float()
valorLimite = float()
termoInt = float()
saidaMax = float()
saidaMin = float()
valorSaida = float()
ki = float()
ultValorEntrada = float()
kp = float()
kd = float()
tempo = float()
amostraTempo = float()
ultCalculo = float()

class ControladorPID(object):
    def __init__(self, p, i, d, universal, tempo):
        self.p = p
        self.i = i
        self.d = d
        self.universal = universal
        self.tempo = tempo
        global kp, ki, kd
        kp = p
        ki = i
        kd = d
    global tempo, universal, tempopasado, agora
    global kp, ki, kd  # // variaveis de ajuste do PID 0.025, 0.001, 1)
    global valorEntrada, valorSaida, valorLimite  # // variáveis de valores
    global termoInt, ultValorEntrada  # // variáveis de cálculo de erro
    global mudancaTempo, amostraTempo
    global erro
    global dvalorEntrada
    global saidaMin, saidaMax

    def setValorEntrada(self, valor):
        global valorEntrada
        self.valor = valor
        if (valor > 0):
            valorEntrada = valor
        return valorEntrada

    def setValorLimite(self, valor):
        global valorLimite
        self.valor = valor
        if (valor > 0):
            valorLimite = valor
        return valorLimite

    def setLimiteSaida(self, minimo, maximo):
        self.minimo = minimo
        self.maxim = maximo
        Min = minimo
        Max = maximo
        global termoInt
        global saidaMax
        global saidaMin
        global valorSaida
        if Min > Max:
            return
        saidaMin = Min
        saidaMax = Max

        if termoInt > saidaMax :
            termoInt = saidaMax

        elif (termoInt < saidaMin):
            termoInt = saidaMin

        if (valorSaida > saidaMax):
            valorSaida = saidaMax

        elif (valorSaida < saidaMin):
            valorSaida = saidaMin
        return valorSaida, saidaMax, saidaMin, termoInt

    def setTEmpo(self, Tempo):
        self.tempo = Tempo

    def saidaPID(self, hora, amostra):
        self.hora = hora
        self.amostra = amostra
        global mudancaTempo, erro, valorLimite, valorSaida, valorEntrada, saidaMin, saidaMax, dvalorEntrada, kp
        global termoInt, ultValorEntrada, ki, kd, ultCalculo  # // variáveis de cálculo de erro
        tempo = hora
        tempopasado = tempo - 0.025
        agora = hora  # ; // variável que busca o tempo imediato
        global mudancaTempo
        mudancaTempo = agora - tempopasado  # ; // variável que compara o tempo de cálculo
        amostraTempo = amostra
        if mudancaTempo >= amostraTempo:  # {// se a mudança for maior que o tempo de amostra, o cálculo é feito.
            # // variáveis para o cálculo do valor de saída
            erro = valorLimite - valorEntrada
            termoInt += ki * erro
            if (termoInt > saidaMax):
                termoInt = saidaMax
            elif (termoInt < saidaMin):
                termoInt = saidaMin
            dvalorEntrada = (valorEntrada - ultValorEntrada)
            # // computando o valor de saída
            valorSaida = kp * erro + ki * termoInt - kd * dvalorEntrada
            if (valorSaida > saidaMax):
                valorSaida = saidaMax
            elif (valorSaida < saidaMin):
                valorSaida = saidaMin
            # // relembrando os valores atuais para a próxima vez
            ultValorEntrada = valorEntrada
            ultCalculo = agora
        return valorSaida





