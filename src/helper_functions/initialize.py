"""
This module is used when the accelerometer first connects with the Edison. 
"""
from upm import pyupm_adxl345 as adxl345
import mraa
import time
delta_t = 0.05
no_of_init_samples = 20				#Number of samples used for calibration.

def initialize():
	"""
	This helper method is responsible for initializing the connection between edison and the Adxl345.
	It obtains an handler to interface with the accelerometer. 
	The method also obtains obtains an initial calibration of the values based on the position of the accelerometer. 

	Input:
	void
	
	Return:
	myAccel -> Object handler of Adxl345
	init_values -> list()
	
	"""
    myAccel = adxl345.Adxl345(0)  #object handler to the accelerometer
    x = mraa.I2c(0)
    x.address(0x53)
    x.writeReg(0x31,0x08)
    x.writeReg(0x2C, 0x0C)

    init_values = [0,0,0]
	#Loop over initial no of samples to obtain calibrated values
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
