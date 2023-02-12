from machine import Pin, PWM, ADC,I2C
from time import sleep_ms
from pca9685 import PCA9685
from servo import Servos
import sys

# Inicializar los pines SDA y SCL
sda = Pin(20)
scl = Pin(21)
id = 0
# Inicializar el bus I2C y el objeto PCA9685
i2c = I2C(id=id, sda=sda, scl=scl)
pca = PCA9685(i2c=i2c)

# Inicializar los servos
servo = Servos(i2c=i2c)
# Establecer la frecuencia de los servos
pca.frequency = 50

# Inicializar el joystick
joystick_x = ADC(Pin(26))
joystick_y = ADC(Pin(27))
joystick_z = ADC(Pin(28))
btn_pin = Pin(22, Pin.IN, Pin.PULL_UP)
camb = Pin(4, Pin.IN, Pin.PULL_UP)
led = machine.Pin(25, machine.Pin.OUT)

#Funcion Map para convertir datos de entrada
def Map(x, in_min, in_max, out_min, out_max):
    return int((x-in_min)*(out_max-out_min)/(in_max-in_min)+out_min)

using_joysticks = True

while True:
    #Verificar si la variable using_joysticks es True o False para cambiar la fuente de datos
    if camb.value() == 0:
        using_joysticks = not using_joysticks
        print("\n",using_joysticks)
        
    if using_joysticks:
        led.value(0)
    else:
        led.value(1)
        
    if using_joysticks:
        # Leer la posición del eje x del joystick
        x_pos = joystick_x.read_u16()
        y_pos = joystick_y.read_u16()
        z_pos = joystick_z.read_u16()
        btn_1 = btn_pin.value()
        
        # Calcular el ángulo para el servo en función de la posición del eje x
        angle_x = Map(x_pos, 0, 65535, 0, 180)
        angle_y = Map(y_pos, 0, 65535, 180, 0)
        angle_z = Map(z_pos, 0, 65535, 180, 0)

        # Establecer la posición del servo
        servo.position(index=0, degrees=angle_x)
        servo.position(index=2, degrees=angle_y)
        servo.position(index=4, degrees=angle_z)
        if btn_1 == 0:
            servo.position(index=6, degrees=90)
        else:
            servo.position(index=6, degrees=0)
    
        print("X: ",angle_x," /Y: ",angle_y," /Z: ",angle_z," /btn: ",btn_1)
         
    else:
        
        received_data = sys.stdin.readline().strip()
        slider_values = received_data.split(',')
        if len(slider_values) >= 4:
            try:
                slider_1 = int(slider_values[0])
            except ValueError:
                slider_1 = 0
            try:
                slider_2 = int(slider_values[1])
            except ValueError:
                slider_2 = 0
            try:
                slider_3 = int(slider_values[2])
            except ValueError:
                slider_3 = 0
            try:
                slider_4 = int(slider_values[3])
            except ValueError:
                slider_4 = 0
                
            if slider_1 != 0:
                servo.position(index=0, degrees=slider_1)
            if slider_2 != 0:
                servo.position(index=2, degrees=slider_2)
            if slider_3 != 0:
                servo.position(index=4, degrees=slider_3)
            if slider_4 != 0:
                servo.position(index=6, degrees=slider_4)
            print("\n-S1: ",slider_1," -S2: ",slider_2," -S3: ",slider_3," -S4: ",slider_4)
            sleep_ms(150)