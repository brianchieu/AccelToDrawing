
g = 980.665
thresh = 30
delta_t = 0.05
no_of_samples = 1
no_of_init_samples = 20

def get_acceleration(myAccel, args):
    thresh = args[0]
    alpha = args[1]
    p_accel = args[2]
    init_values = args[3]

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