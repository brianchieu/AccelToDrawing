from upm import pyupm_adxl345 as adxl345
import mraa
import time
delta_t = 0.05
no_of_init_samples = 20

def initialize():
    myAccel = adxl345.Adxl345(0)
    x = mraa.I2c(0)
    x.address(0x53)
    x.writeReg(0x31,0x08)
    x.writeReg(0x2C, 0x0C)

    u_x, u_y = [0,0]
    init_values = [0,0,0]
    for i in range(no_of_init_samples):
        myAccel.update()
        accel = myAccel.getAcceleration()
        for i in range(3):
            init_values[i] += accel[i]
        time.sleep(delta_t)

    for i in range(3):
        init_values[i] = init_values[i] / no_of_init_samples
        print init_values[i]
    
    return myAccel, init_values

if __name__ == "__main__":
	initialize() 