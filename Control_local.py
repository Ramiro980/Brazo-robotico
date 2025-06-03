from machine import Pin, ADC, I2C, PWM
from time import sleep_ms
from pca9685 import PCA9685
from servo import Servos

#Inicilizar bus I2C y el objeto PCA9685
i2c = I2C(id=1, sda=Pin(14), scl=Pin(15))
pca = PCA9685(i2c=i2c)

#Inicializar servos y establecer frecuencia
S = Servos(i2c=i2c)
pca.frequency = 50

#Inicializar joystick
x = ADC(Pin(26))
yz = ADC(Pin(27))
Btn = Pin(22,Pin.IN,Pin.PULL_UP)
Pi_ON = Pin(16,Pin.IN,Pin.PULL_DOWN)
Pi_OFF = Pin(17,Pin.IN,Pin.PULL_DOWN)

#Definicion de variables
Cont = 0
ix = 90
iy = 90
iz = 90
Pi = 0

#Funcion conversion
def Conv(a):
    return int((a*4)/65535)

#Funcion suma de iteraciones
def Sum(i,C):
    if C < 3 and i > 0:
        i -= 1
    elif C > 3 and i < 180:
        i += 1
    return i

S.position(index=0,degrees=90)
S.position(index=2,degrees=90)
S.position(index=4,degrees=90)
S.position(index=6,degrees=0)

while True:
    #---Condicion para cambiar de modo---
    if Btn.value() == 0:
        Cont += 1
        if Cont > 2:
            Cont = 0

        print("Cambio de servo")
        sleep_ms(150)
    
    #---Condicion para controlar pinza---
    if Pi_ON.value() == 1 and Pi < 90:
        Pi += 1
        S.position(index=6,degrees=Pi)
        
    if Pi_OFF.value() == 1 and Pi > 0:
        Pi -= 1
        S.position(index=6,degrees=Pi)
        
    #---Condicion para controlar eje X---
    if Cont == 0:
        Cx = x.read_u16()
        Cx1 = Conv(Cx)
        
        ix = Sum(ix,Cx1)
        
        S.position(index=0,degrees=ix)
        
        print("--|Servo 1: ",ix)
    
    #---Condicion para controlar eje Y---
    if Cont == 1:
        Cy = yz.read_u16()
        Cy1 = Conv(Cy)
        
        iy = Sum(iy,Cy1)
        
        S.position(index=2,degrees=iy)
        
        print("--|Servo 2:",iy)
    
    #---Condicion para controlar eje Z---
    if Cont == 2:
        Cz = yz.read_u16()
        Cz1 = Conv(Cz)
        
        iz = Sum(iz,Cz1)
        
        S.position(index=4,degrees=iz)
        
        print("--|Servo 3:",iz)
    
    sleep_ms(15)
