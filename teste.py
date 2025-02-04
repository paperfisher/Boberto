#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.iodevices import I2CDevice, LUMPDevice
from pybricks.parameters import Port
from pybricks.ev3devices import Motor
from pybricks.robotics import DriveBase
from pybricks.ev3devices import UltrasonicSensor, ColorSensor
from pybricks.parameters import Stop, Direction
from pybricks.tools import wait


import time


# Initialize the EV3
ev3 = EV3Brick()

sensorLinha = LUMPDevice(Port.S3)
valoresSensorLinha = sensorLinha.read(2)


giroscopio = LUMPDevice(Port.S2)

# sensores do vendra
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

##giroscopio

def giro():
    return giroscopio.read(0)[2]


motor_d_esquerdo = Motor(Port.A, Direction.COUNTERCLOCKWISE) #horario
motor_a_direito = Motor(Port.B, Direction.CLOCKWISE) #antihorario

bobo = DriveBase(motor_a_direito, motor_d_esquerdo, 50, 123)

branco = 68
preto = 40


kp = 1.2 #1
kd = 1.8 # 0.5


#os melhores valores foram 1.5 e 1.5

def erro():
    erro = (CorEsquerdaEXvendra() + CorEsquerdaVendra()) - (CorDireitaVendra() + CorDireitaEXvendra())
    return erro

   

def pd():
    p = erro() * kp 
    d = erro() - erro_anterior * kd
    return p + d


def seguirlinha():
    
    vb = 60
    valor = pd()

    motor_d_esquerdo.dc(vb + valor)
    motor_a_direito.dc(vb - valor)

    
    erro_anterior = erro()

    wait(25)


def checar_90():
    if sensoresEs() > branco and sensoresDir() < preto:
        print("noventa dir")
        
        return "dir"
    elif sensoresDir() > branco and sensoresEs() < preto:
        print("noventa esq")
        print(CorEsquerdaEXvendra(), CorEsquerdaVendra(), CorDireitaVendra(), CorDireitaEXvendra())
        return "esq"
    else:
        False

def pararMotores():
    stop()

def NoventaDir():
    atual = giro()

    while giro() < (atual + 90):
        # print(giro())

        motor_d_esquerdo.dc(50)
        motor_a_direito.dc(-50)

def NoventaEsq():
    atual = giro()

    while giro() > (atual - 90):
        # print(giro())

        motor_d_esquerdo.dc(-50)
        motor_a_direito.dc(50)

a = 1
def e_gap():
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

def gap():
    while tudobranco() == True:
        pararMotores()
        bobo.straight(10)


def girargraus(graus, direcao):

    if direcao == "esq":

        atual = giro()

        while giro() < (atual + graus):
            # print(giro())

            motor_d_esquerdo.dc(50)
            motor_a_direito.dc(-50)

    if direcao == "dir":

        atual = giro()

        while giro() > (atual - graus):
            # print(giro())

            motor_d_esquerdo.dc(-50)
            motor_a_direito.dc(50)

def gira_ate_achar():

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

        motor_d_esquerdo.dc(50)
        motor_a_direito.dc(50)

        wait(300)

        if tudobranco() == True:
            
            print(CorEsquerdaEXvendra(), CorEsquerdaVendra(), CorDireitaVendra(), CorDireitaEXvendra())
            pararMotores()  
            NoventaDir()

            motor_d_esquerdo.dc(-50)
            motor_a_direito.dc(-50)

            wait(400)

            if tudobranco() == True:

                girargraus(30, "dir")
                if tudobranco() == True:
                    girargraus(60, "esq")

                    if tudobranco() == True:

                        while tudobranco() == True:

                            girargraus(15, "esq")
                    
            
    if checar_90() == "esq":

        motor_d_esquerdo.dc(50)
        motor_a_direito.dc(50)

        wait(400)

        if tudobranco() == True:

            print(CorEsquerdaEXvendra(), CorEsquerdaVendra(), CorDireitaVendra(), CorDireitaEXvendra())
            pararMotores()  
            NoventaEsq()

            motor_d_esquerdo.dc(-50)
            motor_a_direito.dc(-50)

            wait(300)

            if tudobranco() == True:

                girargraus(30, "dir")
                if tudobranco() == True:
                    girargraus(60, "esq")

                    if tudobranco() == True:

                        while tudobranco() == True:

                            girargraus(15, "esq")
                            

erro_anterior = 0
while True:
    # if e_gap() == True:
    #     gap()

    # noventa_semverde()
    # gira_ate_achar()

    erroo = erro()
    p = erroo * kp 
    d = erroo - erro_anterior * kd
    
    vb = 40
    valor = p + d

    motor_d_esquerdo.dc(vb + valor)
    motor_a_direito.dc(vb - valor)

    erro_anterior = erroo

    wait(25)