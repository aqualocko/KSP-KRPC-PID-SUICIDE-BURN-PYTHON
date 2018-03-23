#!/usr/bin/env python
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

###

# Elementos de layout

conn = krpc.connect(name='Suicide Burn')
canvas = conn.ui.stock_canvas
screen_size = canvas.rect_transform.size
panel = canvas.add_panel()
rect = panel.rect_transform
rect.size = (400,100)
rect.position = (250-(screen_size[0]/2),-100)
text = panel.add_text("Telemetria")
text.rect_transform.position = (-30,0)
text.color = (1,1,1)
text.size = 16

###
refer = conn.space_center.active_vessel.orbit.body.reference_frame
surAlt = conn.space_center.active_vessel.flight(refer).surface_altitude

def main():
        
    #  DECLARACAO DE VARIAVEIS

    
    

    ksc = conn.space_center
    foguete = ksc.active_vessel

    foguete.control.throttle = 0
    foguete.control.activate_next_stage() #inicia zerando throttle e ligando motores

                
    
      
    while True:

            # Atencao!
            # Variaveis bagunçadas pois acabei juntando as que eu havia criado
            # com as do PesteRenan, mas nao influencia negativamente no codigo

            # Variaveis
            ksc = conn.space_center
            foguete = ksc.active_vessel
            refer = foguete.orbit.body.reference_frame
            centroEspacial = conn.space_center
            naveAtual = ksc.active_vessel
            vooNave = foguete.flight(refer)
            pontoRef = foguete.orbit.body.reference_frame
            UT = conn.space_center.ut
            TWRMax = float()
            distanciaDaQueima = float()
            tempoDaQueima = float()
            acelMax = float()
            alturaPouso = 20.0
            speed = float(foguete.flight(refer).speed)
            altitudeNave = foguete.flight(refer).bedrock_altitude
            elevacaoTerreno = foguete.flight(refer).elevation
            massaTotalNave = foguete.mass
            velVertNave = foguete.flight(refer).vertical_speed
            piloto = foguete.auto_pilot
            refer = foguete.orbit.body.reference_frame
            vooNave = foguete.flight(refer)
            surAlt = foguete.flight(refer).surface_altitude
            elevacaoTerreno = foguete.flight(refer).elevation
            velVertNave = foguete.flight(refer).vertical_speed
            massa = foguete.mass
            empuxoMax = foguete.max_thrust

            #foguete.control.sas = True
            #foguete.control.sas_mode = foguete.control.sas_mode.retrograde
            #piloto.engage()
            #piloto.target_pitch_and_heading(90, 90)
                        
            naveAtual.control.brakes = True
            forcaGravidade = foguete.orbit.body.surface_gravity
            TWRMax = empuxoMax / (massa * forcaGravidade)
            acelMax = (TWRMax * forcaGravidade) - forcaGravidade
            tempoDaQueima = speed / acelMax
            distanciaDaQueima = speed * tempoDaQueima + 1/2 * acelMax * pow(tempoDaQueima, 2)
            distanciaPouso = alturaPouso

           





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
            kp = float(.024) #.02
            global ki
            ki = float(.001)#.001
            global kd
            kd = float(1) #1

            global amostraTempo
            amostraTempo = 25 / 1000 # tempo de amostragem

            global saidaMin
            global saidaMax
            saidaMin = float(-1)
            saidaMax = float(1) # limitar saída dos valores

            #
            global agora
            global mudancaTempo
            agora = ksc.ut # var busca tempo imediato
            mudancaTempo = agora - ultCalculo # var compara tempo calculo

            global termoInt
            termoInt = float()
            

            def computarPID() :
                    global ultCalculo
                    global ultValorEntrada
                    global valorSaida
                    global termoInt
                    
                            
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

                    if termoInt > saidaMax:
                        termoInt = saidaMax
                    elif termoInt < saidaMin:
                        termoInt = saidaMin
                    if valorSaida > saidaMax:
                        valorSaida = saidaMax
                    elif valorSaida < saidaMin:
                        valorSaida = saidaMin
                    
                    return(valorSaida)
                
            
            
            
            
            # Imprimir informacoes
            print "TWR           : %f" % TWRMax
            print "Dist. Queima  : %f" % distanciaDaQueima
            print "Altitude Voo  : %d" % surAlt
            print "Elev. Terreno : %d" % elevacaoTerreno
            print "Correcao      : %f" % computarPID() # esse valor que nao esta atualizando, e deveria atualizar
            
            novaAcel = 1 / TWRMax + computarPID() # calculo de aceleracao
            
            print "Acc Calculada : %f" % novaAcel
            print "                  "
            
            text.content = 'Correcao: %f' % computarPID() # mostra calculo na tela do jogo
            
            if altitudeNave < 500:
                naveAtual.control.gear = True # altitude para trem de pouso

            if altitudeNave > 500:
                naveAtual.control.gear = False
                
            if altitudeNave < 5:
                naveAtual.control.throttle = 0
            else:
                naveAtual.control.throttle = novaAcel
            #time.sleep(.25)
           
        

if surAlt > 3:
    main()
else:
    print("Foguete atualmente pousado")
    print("Encerrando processo...")
    text.content = 'Foguete Pousado'
