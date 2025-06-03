from machine import Pin, ADC, I2C, PWM
from time import sleep_ms
from pca9685 import PCA9685
from servo import Servos
import sys
import select

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
Btn_mod = Pin(0,Pin.IN,Pin.PULL_UP)
Pi_ON = Pin(16,Pin.IN,Pin.PULL_DOWN)
Pi_OFF = Pin(17,Pin.IN,Pin.PULL_DOWN)

#Definicion de variables
Cont = 0
Btn_mod_antes = 1
ix = 90
iy = 90
iz = 90
Pi = 0
modo = True

S.position(index=0,degrees=90)
S.position(index=2,degrees=90)
S.position(index=4,degrees=90)
S.position(index=6,degrees=0)

while True:
    #---Modo remoto---
    if select.select([sys.stdin],[],[],0)[0]:
        received_data = sys.stdin.readline().strip()
        sl_value = received_data.split(',')
                
        if len(sl_value) >= 4:
            try:
                sl_1 = int(sl_value[0])
            except ValueError:
                sl_1 = None
                        
            try:
                sl_2 = int(sl_value[1])
            except ValueError:
                sl_2 = None
                    
            try:
                sl_3 = int(sl_value[2])
            except ValueError:
                sl_3 = None
                    
            try:
                Btn_ = int(sl_value[3])
            except ValueError:
                Btn_ = None
                    
            if sl_1 is not None:
                S.position(index=0,degrees=sl_1)
            if sl_2 is not None:
                S.position(index=2,degrees=sl_2)
            if sl_3 is not None:
                S.position(index=4,degrees=sl_3)
            if Btn_ is not None:
                if Btn_ == 2 and Pi < 90:
                    Pi += 2
                    S.position(index=6,degrees=Pi)
                if Btn_ == 1 and Pi > 0:
                    Pi -= 2
                    S.position(index=6,degrees=Pi)
                    
            print("Datos Remoto S1: ",sl_1,"S2: ",sl_2,"S3: ",sl_3,"Pinza: ",Pi)
