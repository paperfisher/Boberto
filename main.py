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

        wait(100)

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


kp = 1.65 #1
kd = 1.3 # 0.5
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

   


    ## quando ele chama o girar graus dentro do grie até achar ele da um erro estranho, tem q ver dps
    ## e acontece coisas parecidas no gap

    erroo = erro()
    p = erroo * kp 
    d = erroo - erro_anterior * kd

    # print(erro(), p, d, "         ", todos_linha())
    
    vb = 75
    valor = p + d

    motor_a_esquerdo.dc(vb - valor)
    motor_b_direito.dc(vb + valor)

    erro_anterior = erroo

    #     # parar(run)

    while relogio.tempo() < 25:

        continue


#COMENTA ESSA MERDA, tudo oque você faz tem que ser entendivel