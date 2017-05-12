"""
This module contains the get_acceleration helper method that reads the raw acceleration and returns processed acceleration.
"""
#Constants
g = 980.665         #Acceleration due to gravity, upto 3 decimal points.

def get_acceleration(myAccel, args):
    """
    This method reads raw acceleration from the accelerometer, removes the noise and effect of gravity
    to provide with the final processed values.
    
    Input:
    myAccel - an object handler to the adxl345 accelerometer
    args - list()
    
    Output:
    x,y,z   - list()
    p_accel - list()
    """
    thresh = args[0]        #Threshold to remove noise
    alpha = args[1]         #senisitivy factor --> that alters the rate at which the components of 'g' changes 
                            #with change of angle
    p_accel = args[2]       #Previous value of acceleration 
    init_values = args[3]   #The initial values of acceleration obtained during calibiration 

    myAccel.update()
    accel = myAccel.getAcceleration()
    accel_list = [0, 0, 0]
    for i in range(3):
        accel_list[i] = accel[i]
        if abs( accel[i] - p_accel[i]) < (thresh / g) or abs( accel[i] - init_values[i]) < (thresh / g) :
            init_values[i] = alpha * init_values[i] + (1-alpha) * accel[i]
    p_accel = accel_list
    x, y, z = accel[0] - init_values[0], accel[1] - init_values[1], accel[2] - init_values[2]
    x = 0 if abs(x * g) < thresh else x * g
    y = 0 if abs(y * g) < thresh else y * g
    z = 0 if abs(z * g) < thresh else z * g

    return [x,y,z], p_accel
