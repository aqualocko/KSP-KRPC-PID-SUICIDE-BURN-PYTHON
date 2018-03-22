# -*- coding: cp1252 -*-

"""
Suicide Burn com calcullos PID

Para rodar eh necessario:
- Kerbal Space Program (testado na versao 1.4.0)
- mod kRPC (testado na versão 0.4.4)
- Testado no Python 2.7 https://www.python.org/download/releases/2.7/
- Em desenvolvimento por Andrey Oliveira - tendo iniciado 18/03/2018

"""

import krpc
import time
import logging
import time
import math


conn = krpc.connect(name='Suicide Burn')
ksc = conn.space_center
foguete = ksc.active_vessel


#PID

        
refer = foguete.orbit.body.reference_frame
surAlt = foguete.flight(refer).surface_altitude
forcaGravidade = foguete.orbit.body.surface_gravity
massa = foguete.mass
empuxoMax = foguete.max_thrust
TWRMax = empuxoMax / (massa * forcaGravidade)
acelMax = (TWRMax * forcaGravidade) - forcaGravidade
speed = float(foguete.flight(refer).speed)
tempoDaQueima = speed / acelMax
alturaPouso = 20.0
distanciaPouso = alturaPouso
elevacaoTerreno = foguete.flight(refer).elevation
distanciaDaQueima = speed * tempoDaQueima + 1/2 * acelMax * pow(tempoDaQueima, 2)

global ultCalculo
ultCalculo = 0 # tempo do ultimo calculo
global valorEntrada
valorEntrada = float(surAlt)
global valorSaida
valorSaida = float()
global valorLimite
valorLimite = float(distanciaPouso + distanciaDaQueima) # variáveis de valores

        
global ultValorEntrada
ultValorEntrada = float() # variáveis de cálculo de erro

        
global kp
kp = float(.02)
global ki
ki = float(.001)
global kd
kd = float(1) #variaveis de ajuste do PID

global amostraTempo
amostraTempo = 0.020 # tempo de amostragem

global saidaMin
global saidaMax
saidaMin = float(-1)
saidaMax = float(1) # limitar saída dos valores

#
global agora
global mudancaTempo
agora = ksc.ut # var busca tempo imediato
mudancaTempo = agora - ultCalculo # var compara tempo calculo

        
        

def computarPID() :
        global ultCalculo
        global ultValorEntrada
        global valorSaida

        global termoInt
        termoInt = float()
                
        agora = ksc.ut # var busca tempo imediato
        mudancaTempo = agora - ultCalculo # var compara tempo calculo

                
        if mudancaTempo >= amostraTempo: # se a mudança for > q o tempo de amostra, o calculo é feito
                # var calculo valor saida
                erro = valorLimite - valorEntrada
                termoInt += ki * erro
                if termoInt > saidaMax:
                        termoInt = saidaMax
                elif termoInt < saidaMax:
                        termoInt = saidaMin
                dvalorEntrada = (valorEntrada - ultValorEntrada)
                # computando valor saida
                valorSaida = kp * erro + ki * termoInt - kd * dvalorEntrada
                if valorSaida > saidaMax:
                        valorSaida = saidaMax
                elif valorSaida < saidaMin:
                        valorSaida = saidaMin

                # relembra valores atuais pra prox

                ultValorEntrada = valorEntrada
                ultCalculo = agora

        return(valorSaida)

        
        
def ValorEntrada(valor) :
        if valor > 0:
                valorEntrada = valor


def ValorLimite(valor) :
        if valor > 0:
                valorLimite = valor

        
def LimiteSaida(Min, Max) :
        if Min > Max:
                return
                
        saidaMin = Min
        saidaMax = Max
        if termoInt > saidaMax:
                termoInt = saidaMax
        elif termoInt < saidaMin:
                termoInt = saidaMin
        if valorSaida > saidaMax:
                valorSaida = saidaMax
        elif valorSaida < saidaMin:
                valorSaida = saidaMin

def Ajustes(Kp,Ki,Kd):
        kp = Kp
        ki = Ki
        kd = Kd

        
def AmostraTempo(novaAmostraTempo):
        if novaAmostraTempo > 0:
                amostraTempo = novaAmostraTempo / 1000
        
"""def AtualizarVariaveis():
        forcaGravidade = foguete.orbit.body.surface_gravity
        TWRMax = foguete.max_thrust / (foguete.mass * forcaGravidade)
        acelMax = (TWRMax * forcaGravidade) - forcaGravidade
        tempoDaQueima = foguete.flight().vertical_speed / acelMax
        surAlt = foguete.flight(refer).surface_altitude
        distanciaDaQueima = (foguete.flight().vertical_speed * tempoDaQueima + 1/2 * acelMax * pow(tempoDaQueima, 2))
        print "TWR         : %d" % TWRMax
        print "Dist. Queima: %d" % distanciaDaQueima
        print "Altitude Voo: %d" % altitudeNave
        print "Elevacao: %d" % elevacaoTerreno
        print "Correcao    : %d" % computarPID"""









