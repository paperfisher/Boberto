#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.iodevices import I2CDevice, LUMPDevice
from pybricks.parameters import Port
from pybricks.ev3devices import Motor
from pybricks.robotics import DriveBase
from pybricks.ev3devices import UltrasonicSensor, ColorSensor
from pybricks.parameters import Stop, Direction
from pybricks.tools import wait
from cronometro import Cronometro

import time

ev3 = EV3Brick()

sensorLinha = LUMPDevice(Port.S4)
valoresSensorLinha = sensorLinha.read(2)


giroscopio = LUMPDevice(Port.S2)

motor_a_esquerdo = Motor(Port.A, Direction.COUNTERCLOCKWISE) #antihorario
motor_b_direito = Motor(Port.B, Direction.CLOCKWISE) #horario

bobo = DriveBase(motor_a_esquerdo, motor_b_direito, 48, 116)

branco = 78
preto = 36

#relacionado aos sensores

#region

## VALORES HSV
def sensoresdecor():
    return sensorLinha.read(2)[20], sensorLinha.read(2)[21], sensorLinha.read(2)[22], sensorLinha.read(2)[23], sensorLinha.read(2)[24], sensorLinha.read(2)[25], sensorLinha.read(2)[26], sensorLinha.read(2)[27], sensorLinha.read(2)[28]

def sensordecorDir():
    return sensorLinha.read(2)[20], sensorLinha.read(2)[21], sensorLinha.read(2)[22]
    
def sensordecorMeio():
    return sensorLinha.read(2)[23], sensorLinha.read(2)[24], sensorLinha.read(2)[25]

def sensordecorEs():
    return sensorLinha.read(2)[26], sensorLinha.read(2)[27], sensorLinha.read(2)[28]

def sensoresdecor2():
    return sensordecorEs(), sensordecorMeio(), sensordecorDir()


# SENSORES DE SEGUIR LINHA

#checa se está vendo vermelho
def checarcor(sensor):

    h = sensor[0]
    s = sensor[1]
    v = sensor[2]

    if ((10 >= h >= 0) or (120 >= h >= 110))and (s >= 40) and (v > 10):

        wait(10)

        if ((10 >= h >= 0) or (120 >= h >= 110))and (s >= 40) and (v > 10):

            ev3.speaker.beep(300,100)
            print("vermelho")
            return "vermelho"
    
    elif (55 >= h >= 25) and (s >= 40) and (v > 10):

        wait(10)

        if (55 >= h >= 25) and (s >= 40) and (v > 10):

            ev3.speaker.beep(100,50)
            print("verde")
            return "verde"

    else:
        return "erro"

# cor do sensor da esquerda do meio
def CorEsquerdaVendra():
    return sensorLinha.read(2)[1]

# cor do sensor da esquerda extrema
def CorEsquerdaEXvendra():
    return sensorLinha.read(2)[0]

# cor do sensor da direita do meio
def CorDireitaVendra():
    return sensorLinha.read(2)[2]

# cor do sensor da direita extrema
def CorDireitaEXvendra():
    return sensorLinha.read(2)[3]

def todos_linha():
    return (CorEsquerdaEXvendra(), CorEsquerdaVendra(), CorDireitaVendra(), CorDireitaEXvendra())

## direita e da esquerda juntos

def sensoresDir():
    return (CorDireitaVendra() + CorDireitaEXvendra()) / 2

def sensoresEs():
    return (CorEsquerdaEXvendra() + CorEsquerdaVendra()) / 2

# o index 0 é o da direita

def tudobranco():
    if CorEsquerdaVendra() > branco and CorEsquerdaEXvendra() > branco and CorDireitaVendra() > branco and CorDireitaEXvendra() > branco:
        return True
    else:
        return False

def viupreto():

    if CorEsquerdaVendra() < preto or CorEsquerdaEXvendra() < preto or CorDireitaVendra() < preto or CorDireitaEXvendra() < preto:
        return True
    else:
        return False
#endregion

## FUNÇÕES BASICAS

def pararMotores():

    beep(100,100)

    motor_a_esquerdo.stop
    motor_b_direito.stop

##giroscopio

def giro():
    return giroscopio.read(0)[2]

#os melhores valores foram 1.5 e 1.5

def erro():
    erro = (CorEsquerdaEXvendra() + CorEsquerdaVendra()) - (CorDireitaVendra() + CorDireitaEXvendra())
    return erro


def pd(): ##não ta sendo utilizado
    p = erro() * kp 
    d = erro() - erro_anterior * kd
    return p + d   

def checar_90():

    if sensoresEs() > branco and sensoresDir() < preto:
           
        print("noventa dir")
        
        return "dir"

    elif sensoresDir() > branco and sensoresEs() < preto:
        
        print("noventa esq")
        # print(CorEsquerdaEXvendra(), CorEsquerdaVendra(), CorDireitaVendra(), CorDireitaEXvendra())
        return "esq"

    else:
        False

def girargraus(graus, direcao):

    if direcao == "esq":

        atual = giro()

        while giro() < (atual + graus):
            # print(giro())

            motor_a_esquerdo.dc(70)
            motor_b_direito.dc(-70)

    if direcao == "dir":

        atual = giro()

        while giro() > (atual - graus):
            # print(giro())

            motor_a_esquerdo.dc(-70)
            motor_b_direito.dc(70)

def NoventaDir():
    atual = giro()

    while tudobranco() == True:
        # print(giro())

        motor_a_esquerdo.dc(50)
        motor_b_direito.dc(-50)

def NoventaEsq():
    atual = giro()

    while tudobranco() == True:
        # print(giro())

        motor_a_esquerdo.dc(-50)
        motor_b_direito.dc(50)

a = 1
def e_gap(): #tem que olhar melhor

    global a
    for i in range(a):
        pararMotores()
        bobo.straight(10)
        a = a + 1
        if a > 10:
            bobo.straight(-a * 10)
            return False
            break
        if tudobranco() == False:
            pass
        else:
            return False

def gap(): #tem que olhar melhor

    while tudobranco() == True:
        pararMotores()
        bobo.straight(10)

def gira_ate_achar(): #tem que olhar melhor

    if tudobranco() == True:

        #verifica se é gap
        if e_gap() == True:
            gap()

        else:
            girargraus(30, "dir")
            if tudobranco() == True:
                girargraus(60, "esq")

                if tudobranco() == True:

                    while tudobranco() == True:

                        girargraus(15, "esq")
                    
def noventa_semverde():

    if checar_90() == "dir": 

        ev3.speaker.beep(600,200)
        print(todos_linha())

        motor_a_esquerdo.dc(50)
        motor_b_direito.dc(50)

        wait(100)

        if tudobranco() == True:
            
            print(CorEsquerdaEXvendra(), CorEsquerdaVendra(), CorDireitaVendra(), CorDireitaEXvendra())
            pararMotores()  
            NoventaDir()

            # motor_a_esquerdo
            #.dc(-50)
            # motor_b_direito.dc(-50)

            wait(250)

            if tudobranco() == True:

                girargraus(30, "dir")
                if tudobranco() == True:
                    girargraus(60, "esq")

                    if tudobranco() == True:

                        while tudobranco() == True:

                            girargraus(15, "dir")

        else:
            pararMotores()
            motor_a_esquerdo.dc(-50)
            motor_b_direito.dc(-50)

            wait(150)
                    
            
    if checar_90() == "esq":

        ev3.speaker.beep(300,100)
        print(todos_linha())

        motor_a_esquerdo.dc(50)
        motor_b_direito.dc(50)

        wait(100)

        if tudobranco() == True:

            print(CorEsquerdaEXvendra(), CorEsquerdaVendra(), CorDireitaVendra(), CorDireitaEXvendra())
            pararMotores()  
            NoventaEsq()

            # motor_a_esquerdo
            #.dc(-50)
            # motor_b_direito.dc(-50)

            wait(250)

            if tudobranco() == True:

                girargraus(30, "dir")
                if tudobranco() == True:
                    girargraus(60, "esq")

                    if tudobranco() == True:

                        while tudobranco() == True:

                            girargraus(15, "esq")

        else:
            pararMotores()
            motor_a_esquerdo.dc(-50)
            motor_b_direito.dc(-50)

            wait(150)

def noventaverde():

    graus = 90

    if checarcor(sensordecorEs()) == "verde" and checarcor(sensordecorDir()) != "verde":

        motor_a_esquerdo.dc(50)
        motor_b_direito.dc(50)

        wait(300)

        pararMotores()
        gcount = 0

        bobo.straight(100)
        bobo.stop()

        motor_a_esquerdo.run(720)
        motor_b_direito.run(-720)

        atual = giro()

        while giro() < (atual + (graus/2)):

            continue

        atual = giro()

        while giro() < (atual - (graus/2)):

            if viupreto() == True:

                break

            continue

        # while gcount < 6 or tudobranco() == False:
        #     girargraus(15, "esq")
        #     if tudobranco() == False:
        #         gcount = 6
        #     gcount += 1
            
        # motor_a_esquerdo.dc(-50)
        # motor_b_direito.dc(-50)

    elif checarcor(sensordecorDir()) == "verde" and checarcor(sensordecorEs()) != "verde":

        motor_a_esquerdo.dc(50)
        motor_b_direito.dc(50)

        wait(300)           
          
        pararMotores() 
        gcount = 0
 
        bobo.straight(100)
        bobo.stop()

        motor_a_esquerdo.run(-720)
        motor_b_direito.run(720)

        atual = giro()

        while giro() > (atual - (graus/2)):

            continue
        
        atual = giro()

        while giro() > (atual - (graus/2)):

            if viupreto() == True:

                break

            continue

        wait(400)

    elif checarcor(sensordecorDir()) == "verde" and checarcor(sensordecorEs()) == "verde":

        girargraus(180, "dir")

def parar(run):

    parar = 0 

    if checarcor(sensordecorDir()) == "vermelho":
        parar += 1   

    if checarcor(sensordecorMeio()) == "vermelho":
        parar += 1      

    if checarcor(sensordecorEs()) == "vermelho":
        parar += 1

    if parar >= 2:
        run = False

   

def jinglebell():
    ev3.speaker.play_notes(["D4/4", "D4/4", "D4/2", "Db4/4", "Db4/4", "Db4/2", "B3/4", "Db4/4", "B3/2", "F#3/3"], 238)

def beep(freq=500, dur=100):
    ev3.speaker.beep(freq, dur)

relogio = Cronometro("tempo")

relogio.carrega()


kp = 1.5 #1
kd = 0.8 # 0.5
erro_anterior = 0
run = True

# bobo.straight(300)
# beep(100,100)
# pararMotores()



def girar90():   
    
    bobo.turn(312)

# girargraus(75, "esq")

while run == True:
    relogio.reseta()

    print(todos_linha())

    # if e_gap() == True:
    #     gap()

    noventa_semverde()
    # noventaverde()
    # gira_ate_achar() 

    ## quando ele chama o girar graus dentro do grie até achar ele da um erro estranho, tem q ver dps
    ## e acontece coisas parecidas no gap

    erroo = erro()
    p = erroo * kp 
    d = erroo - erro_anterior * kd

    # print(erro(), p, d, "         ", todos_linha())
    
    vb = 67
    valor = p + d

    motor_a_esquerdo.dc(vb - valor)
    motor_b_direito.dc(vb + valor)

    erro_anterior = erroo

    #     # parar(run)

    while relogio.tempo() < 25:

        continue


#COMENTA ESSA MERDA, tudo oque você faz tem que ser entendivel