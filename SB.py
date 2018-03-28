# -*- coding: utf-8 -*-
"""
Suicide Burn com calculos PID

Para rodar é necessario:
- Kerbal Space Program (testado na versao 1.4.0)
- mod kRPC (testado na versão 0.4.4)
- Testado no Python 2.7 https://www.python.org/download/releases/2.7/
- Desenvolvido em Java por PesteRenam (https://github.com/Pesterenan )
- Inicialmente Traduzido para Python por Andrey Oliveira - tendo iniciado 18/03/2018
- Aprimorado e ajustado por Maurício Mazur

"""
import krpc, time
import controlePID
nome = 'sb'
conn = krpc.connect(nome)
ksp = conn.space_center
vessel = ksp.active_vessel
body = vessel.orbit.body
flight = vessel.flight(body.reference_frame)
controle = vessel.control
#variaveis de informações
surAlt = conn.add_stream(getattr, flight, 'surface_altitude')
horizontal = conn.add_stream(getattr, flight, 'horizontal_speed')
thrust_max = conn.add_stream(getattr, vessel, 'max_thrust')
massa = conn.add_stream(getattr, vessel, 'mass')
gravidade = conn.add_stream(getattr, body, 'surface_gravity')
velocidade = conn.add_stream(getattr, flight, 'speed')
situacao = conn.add_stream(getattr, vessel, 'situation')
#tempo
UT =conn.add_stream(getattr, ksp, 'ut')
pouso = False
pousado_agua = conn.space_center.VesselSituation.splashed
pousado = conn.space_center.VesselSituation.landed
prelancamento = conn.space_center.VesselSituation.pre_launch
distanciaDaQueima = float()
distanciaPouso = 10 # altura hover
TWRMax = float()
#from PID import ControlePID
from controlePID import ControladorPID
def atualizarvariaveis():
    global TWRMax
    TWRMax = thrust_max() / (massa() * gravidade())
    acelMax = (TWRMax * gravidade()) - gravidade()
    tempoDaQueima = velocidade() / acelMax
    global distanciaDaQueima
    distanciaDaQueima = velocidade() * tempoDaQueima + 1 / 2 * acelMax * (tempoDaQueima ** 2)
    return TWRMax, acelMax, tempoDaQueima, distanciaDaQueima
class suicideBurn:
    def suicide(self):
        global pouso
        global distanciaDaQueima
        global TWRMax
        if situacao == pousado or situacao == pousado_agua:
            pouso = False
        while pouso == False:
            #definindo valores do PID
            PID = controlePID.ControladorPID(0.021, 0.001, 1, UT(), UT()) #<================================= ajustes do PID
            global distanciaDaQueima
            global distanciaPouso
            atualizarvariaveis()
            PID.setValorEntrada(surAlt())
            PID.setValorLimite(distanciaPouso + distanciaDaQueima)
            PID.setLimiteSaida(-1, 1)
            atualizarvariaveis()
            #verificações
            #  <============================================================== Controle de SAS
            controle.sas = True
            if horizontal() > 2 and surAlt() <= (distanciaPouso + 30 ) :
                controle.sas_mode = controle.sas_mode.retrograde
            elif horizontal() < 2 and surAlt() <= distanciaPouso:
                controle.sas_mode = controle.sas_mode.radial
            if surAlt() < 300:                                   #<=========================== perninhas
                controle.gear = True
            else:
                controle.gear = False
            controle.brakes = True

            #atualizar
            atualizarvariaveis()
            correcao = PID.saidaPID(UT(), 0.019)


            # Imprimir informacoes
            print "TWR           : %2.f" % TWRMax
            print "Dist. Queima  : %f" % distanciaDaQueima
            print "Altitude Voo  : %3.f" % surAlt()
            print "Correcao      : ",  correcao #PID.saidaPID(UT(), 0.025)

            novaAcel = (1 / TWRMax + correcao) # <--------------------------------------------    calculo de aceleracao

            print "Acc Calculada : %f" % novaAcel
            print "                  "
            if situacao() == pousado or situacao() == pousado_agua:
                controle.throttle = 0
                pouso = True
            else:
                controle.throttle = novaAcel
            #time.sleep(0.2)
burn = suicideBurn()

if situacao() == pousado or situacao() == prelancamento:
    teste = surAlt() - 10
    while teste < distanciaPouso:
        teste = surAlt() - 15
        print("Subindo...")
        controle.gear = False
        atualizarvariaveis()
        controle.throttle = (float (1 / TWRMax * 1.5))

controle.throttle = 0
burn.suicide()
