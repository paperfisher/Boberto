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
<<<<<<< HEAD
giroscopio = LUMPDevice(Port.S3)
laser = LUMPDevice(Port.S1)

=======


giroscopio = LUMPDevice(Port.S2)
>>>>>>> 4e7acdd5ab1cbd562077c804ccd7f7daca112e23
motor_a_esquerdo = Motor(Port.A, Direction.COUNTERCLOCKWISE) #antihorario
motor_b_direito = Motor(Port.B, Direction.CLOCKWISE) #horario

bobo = DriveBase(motor_a_esquerdo, motor_b_direito, 48, 116)
bobo.settings(300, 1000, 400, 1000)

<<<<<<< HEAD
branco = 74
preto = 35
=======
branco = 68 #73
preto = 20
>>>>>>> 4e7acdd5ab1cbd562077c804ccd7f7daca112e23

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

    # verde
    if (55 >= h >= 22) and (s >= 35) and (v > 10):

        # wait(1)
        # if (55 >= h >= 25) and (s >= 40) and (v > 10):
        # beep(100,50)
        # print("verde")
        return "verde"

    elif ((15 >= h >= 0) or (125 >= h >= 103)) and (s >= 35) and (v > 9): #VERMELHO

        # wait(1)
        # if ((10 >= h >= 0) or (120 >= h >= 110))and (s >= 40) and (v > 10):
        beep(300,100)
        print("vermelho")
        return "vermelho"
    
    else:
        return "erro"

# cor do sensor da esquerda do meio
def CorEsquerdaVendra():
    return sensorLinha.read(2)[3]

# cor do sensor da esquerda extrema
def CorEsquerdaEXvendra():
    return sensorLinha.read(2)[2]

# cor do sensor da direita do meio
def CorDireitaVendra():
    return sensorLinha.read(2)[1]

# cor do sensor da direita extrema
def CorDireitaEXvendra():
    return sensorLinha.read(2)[0]

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

    if CorEsquerdaVendra() < pretso or CorEsquerdaEXvendra() < preto or CorDireitaVendra() < preto or CorDireitaEXvendra() < preto:
        return True
    else:
        return False
#endregion

#region
## FUNÇÕES BASICAS

def pararMotores():
    bobo.stop()
    motor_a_esquerdo.brake()
    motor_b_direito.brake()
    motor_a_esquerdo.stop()
    motor_b_direito.stop()

##giroscopio
def giro(): #angulo
    return giroscopio.read(0)[2]

def inclinacao():
    return giroscopio.read(0)[0]

def dist(): #sensor a laser, medida em milimetros
    return laser.read(0)[0]

def erro():
    erro = (CorEsquerdaEXvendra() + CorEsquerdaVendra()) - (CorDireitaVendra() + CorDireitaEXvendra())
    return erro

def girargraus_errado(graus, direcao):

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

def girargraus(gr, direc):
    pararMotores()
    graus = gr * 3.1

    if direc == "esq":
        bobo.turn(-graus)
    if direc == "dir":
        bobo.turn(graus)
    pararMotores()

def reto(mm):
    pararMotores()
    bobo.straight(mm * 2)
    pararMotores()

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
#endregion

def noventasemverde(): #ta funcionando bem, so tem q ajustar o kp e o kd melhor, e a condicao um pouquinho e tentar checar mais
    
    ##se ver 90 checar se tem linha dps, pq se tiver e pra ignorar

    if CorEsquerdaVendra() < preto - 10 and CorEsquerdaEXvendra() < preto - 5 and CorDireitaVendra() > branco - 30 and CorDireitaEXvendra() > branco - 10:
        print("esq") 
        print(todos_linha())
        beep()
        reto(50)
        
        while tudobranco() == True:
            girargraus(30,"esq")
        reto(-50)

    if CorDireitaVendra() < preto - 10 and CorDireitaEXvendra() < preto - 5 and CorEsquerdaVendra() > branco - 30 and CorEsquerdaEXvendra() > branco - 10:
        print("dir") 
        print(todos_linha())
        beep()
        reto(50)
       
        while tudobranco() == True:
            girargraus(30,"dir")
        reto(-50)


    ## esses numeros que eu to subtraindo nas condicoes q nem o "CorEsquerdaVendra() < preto - 10"
    ## tao servindo pra calibrar o valor minimo q o sensor tem q estar vendo pra ele dar a condicao como verdade com mais precisao
    ## eu to preferindo ver cada sensor individualmente pq e mais preciso doq calcular a media, mas precisa calibrar bem esses valores

def verde(): 

    vai = 40
    volta = -20
    if checarcor(sensordecorDir()) == "verde" and checarcor(sensordecorEs()) != "verde": # se ele ver verde na direita e nao na esquerda
           
        print(sensoresdecor2())
        beep(300,180)
        print("dir")
        pararMotores()
        if CorDireitaEXvendra() > branco - 10:
            pass
        else:
            beep(300,180)
            reto(vai)
            girargraus(90, "dir")
            reto(volta)
        # girargraus(90, "dir")
        # reto(-10)

    elif checarcor(sensordecorEs()) == "verde" and checarcor(sensordecorDir()) != "verde": # se ele ver verde na esquerda e nao na direita

        print(sensoresdecor2())
        beep(50,180)
        print("esq")
        pararMotores()
        if CorEsquerdaEXvendra() > branco - 10:
            pass
        else:
            beep(50,180)
            reto(vai)
            girargraus(90, "esq")
            reto(volta)
        # girargraus(90, "esq")
        # reto(-10)

    elif checarcor(sensordecorDir()) == "verde" and checarcor(sensordecorEs()) == "verde": # se ver verde nos dois lado, ele gira 180

        print(sensoresdecor2())
        beep(600,90)
        print("180")
        pararMotores()
        if CorEsquerdaEXvendra() < preto - 5 or CorDireitaEXvendra() < preto - 5:
            beep(50,180)
            reto(vai)
            girargraus(180, "esq")
            reto(volta)
        # girargraus(180, "esq")
        # reto(-10)

    #lembrar de pedir pra verificar dps de andar um pouco pra frente se viu preto, pra ver se e verde falso
    #ta funfando relativamente

def rampa_():

    if inclinacao() > 17 or inclinacao() < -17:
        beep()
        while inclinacao() > 17 or inclinacao() < -17:
            vb = 120
        beep()
        reto(-40)

def obstaculo(): #TROCAR PRO DESVIO CIRCULAR
    if dist() < 120:
        beep(100, 100)

        reto(-20)
        girargraus(60, "esq")
        reto(70)
        # girargraus(70, "dir")
        # reto(200)
        # girargraus(70, "dir")
        # reto(160)
        # girargraus(70, "esq")

        while tudobranco() == True:
            motor_a_esquerdo.dc(190)
            motor_b_direito.dc(35)

        reto(50)
        girargraus(40, "esq")



        


#fazer a funcao de parar o robo no vermelho

def jinglebell():
    ev3.speaker.play_notes(["D4/4", "D4/4", "D4/2", "Db4/4", "Db4/4", "Db4/2", "B3/4", "Db4/4", "B3/2", "F#3/3"], 238)

def beep(freq=500, dur=100):
    ev3.speaker.beep(freq, dur)

relogio = Cronometro("tempo")

relogio.carrega()

kp = 1.3 #1.2
kd = 1 # 1
erro_anterior = 0
rampa = False

run = 1
while run == 1:
    relogio.reseta()

    # noventasemverde()
    # verde()
    obstaculo()

<<<<<<< HEAD
=======
    # if sensoresDir() > branco and sensoresEs() < preto: 
    #     print("esq") 
    #     beep()
    #     reto(70)
    #     if tudobranco() == True:
    #         while tudobranco() == True:
    #             girargraus(30,"esq")
    #         reto(-50)


    # if sensoresEs() > branco and sensoresDir() < preto:
    #     print("esq") 
    #     beep()
    #     reto(70)
    #     if tudobranco() == True:
    #         while tudobranco() == True:
    #             girargraus(30,"dir")
    #         reto(-50)



    ## quando ele chama o girar graus dentro do grie até achar ele da um erro estranho, tem q ver dps
    ## e acontece coisas parecidas no gap
>>>>>>> 4e7acdd5ab1cbd562077c804ccd7f7daca112e23

    erroo = erro()
    p = erroo * kp 
    d = erroo - erro_anterior * kd

    vb = 120

<<<<<<< HEAD
    #region RAMPA (TA DANDO CERTO)
    # # checa se o robo ta na rampa
    # if inclinacao() < -17:
    #     # beep()
    #     rampa = True

    # #checa se o robo acabou de sair da rampa
    # if rampa == True and not(inclinacao() < -17):
    #     beep()
    #     rampa = False
    #     reto(-40)
    #endregion
    
    valor = p + d #variacao da potencia do motor

=======
>>>>>>> 4e7acdd5ab1cbd562077c804ccd7f7daca112e23
    motor_a_esquerdo.dc(vb + valor)
    motor_b_direito.dc(vb - valor)

    erro_anterior = erroo

<<<<<<< HEAD
    # print(dist())
    print(todos_linha())
    # print(inclinacao())
=======
        # parar(run)
>>>>>>> 4e7acdd5ab1cbd562077c804ccd7f7daca112e23

    while relogio.tempo() < 25:
        continue

#COMENTA ESSA MERDA, tudo oque você faz tem que ser entendivel

#antes de mecher com as funcoes tem q ajustar BEM o kp e kd

#dps disso calibrar BEM as condicoes q ativam as funcoes, pra n ficar ativando em momentos errados
#fica pedindo so pra beepar, e n fazer mais nada
#dai dps comeca a trabalhar nas funcoes em si


#LEMBRAR DE CALIBRAR DIREITO NO ROBO E CRIAR FUNCAO Q CALIBRA SOZINHO TBM