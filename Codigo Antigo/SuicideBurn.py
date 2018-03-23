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

def main():
        
    #  DECLARACAO DE VARIAVEIS

    # Importando arquivo pid.py
    import pid
    from pid import computarPID
    controle = computarPID # importa funcao computarPID

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
            piloto.engage()
            piloto.target_pitch_and_heading(90, 90)
            naveAtual.control.brakes = True
            forcaGravidade = foguete.orbit.body.surface_gravity
            TWRMax = empuxoMax / (massa * forcaGravidade)
            acelMax = (TWRMax * forcaGravidade) - forcaGravidade
            tempoDaQueima = speed / acelMax
            distanciaDaQueima = speed * tempoDaQueima + 1/2 * acelMax * pow(tempoDaQueima, 2)

            # Imprimir informacoes
            print "TWR           : %f" % pid.TWRMax
            print "Dist. Queima  : %f" % pid.distanciaDaQueima
            print "Altitude Voo  : %d" % pid.surAlt
            print "Elev. Terreno : %d" % pid.elevacaoTerreno
            print "Correcao      : %f" % controle() # esse valor que nao esta atualizando, e deveria atualizar
            
            novaAcel = 1 / TWRMax + controle() # calculo de aceleracao
            
            print "Acc Calculada : %f" % novaAcel
            print "                  "
            
            text.content = 'Correcao: %f' % controle() # mostra calculo na tela do jogo
            
            if altitudeNave < 100:
                    naveAtual.control.gear = True # altitude para trem de pouso
            naveAtual.control.throttle = novaAcel
            time.sleep(0.05)

            # atualiza informacoes no arquivo pid.py para serem relidos pelo while loop
            pid.surAlt = surAlt
            pid.distanciaDaQueima = distanciaDaQueima
            pid.elevacaoTerreno = elevacaoTerreno
            pid.TWRMax = TWRMax
            pid.acelMax = acelMax
            pid.forcaGravidade = forcaGravidade
            pid.tempoDaQueima = tempoDaQueima
            pid.computarPID
        


main()

