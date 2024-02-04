from machine import Pin, I2C, PWM
from ssd1306 import SSD1306_I2C
import framebuf,sys
from time import sleep

sg90 = PWM(Pin(12, mode=Pin.OUT)) # Signal pin of sg90 connected to gp12
sg90.freq(50) # sg90 freq

pix_res_x  = 128 # SSD1306 horizontal resolution
pix_res_y = 64   # SSD1306 vertical resolution

i2c_dev = I2C(1,scl=Pin(27),sda=Pin(26),freq=200000)  # start I2C on I2C1 (GPIO 26/27)
i2c_addr = [hex(ii) for ii in i2c_dev.scan()] # get I2C address in hex format
if i2c_addr==[]:
    print('No I2C Display Found') 
    sys.exit() # exit routine if no dev found
else:
    print("I2C Address      : {}".format(i2c_addr[0])) # I2C device address
    print("I2C Configuration: {}".format(i2c_dev)) # print I2C params


oled = SSD1306_I2C(pix_res_x, pix_res_y, i2c_dev) # oled controller


# Load the raspberry pi logo into the framebuffer (the image is 32x32)

def oledPrint(text):
    oled.fill(0)
    oled.text(text,60,30)
    oled.show()


def setDegree(degree):
    if degree > 180:
        degree=180
    if degree < 0:
        degree=0

    maxDutyCycle = 8400
    minDutyCycle = 1500

    newDutyCycle=minDutyCycle+(maxDutyCycle-minDutyCycle)*(degree/180)

    sg90.duty_u16(int(newDutyCycle))


while True:
    sleep(1)
    for degree in range(0,181,10):
        
        setDegree(degree)
        oledPrint(str(degree))
        sleep(0.1)
    
    

