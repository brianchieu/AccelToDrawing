"""
This module contains the helper method which computes the position of the pen/accelermeter from the acceleration values
using the kinematic equations.
"""
def compute_position(accel, init_position, delta_t, u_x, u_y):
	"""
	
	This helper method uses the kinematic equations to compute the exact position of the accelerometer from the 
	linear acceleration obtained. 
	
	Input:
	accel 		- list(list)
	init_position 	- list()
	delta_t		- float
	u_x		- float
	u_y 		- float
	
	Return:
	list(), float, float
	"""
    
	s_x,s_y = init_position
	delta_t_sq_half = 0.5 * (delta_t**2)

	for x,y,z in accel:
		v_x = (u_x + delta_t * x) if x != 0.0  else 0.0		#Equate final velocity to zero if acceleration is zero
		v_y = (u_y + delta_t * y) if y != 0.0 else 0.0		#Equate final velocity to zero if acceleration is zero
		
		s_x += (u_x * delta_t + x * delta_t_sq_half)		#Compute displacement using : s = ut + 1/2*a*t^2
		s_y += (u_y * delta_t + y * delta_t_sq_half)		#Compute displacement using : s = ut + 1/2*a*t^2
		u_x, u_y = v_x,v_y

	return [s_x, s_y], v_x, v_y
