"""
This module is resposible for integrating all the helper methods responsible of interfacing the edison with
the accelerometer, read raw values from accelerometer, pre-process the readings and compute displacement. The 
computed displacement is then pushed onto a queue to be read by the bluetooth server running on the Edison.
"""

import time
import copy
from helper_functions.update_pos import *
from helper_functions.get_accel import *
from helper_functions.initialize import *
from Queue import Queue

g = 980.665					#Acceleration due to gravity, upto 3 decimal points.
thresh = 30					#Threshold used to eliminate/weed out noise.

def main(myAccel, init_values, q):
	"""
	
	Input:
	myAccel 	- Object handler for the Adxl345
	q 		- queue()
	init_values	- list()
	
	"""
	p_accel = [0,0,0]
	alpha = 0.99				#senisitivy factor --> that alters the rate at which the 
						#components of 'g' changes with change of angle
	u_x = 0
	u_y = 0
	
	try:
		current_position = [0,0]
		while(True):
			avg_acc = [[0,0,0]]
			init_time = time.time()	#Time before the start of the loop	
			dt = 0
			count = 0
			while ( dt < 0.2):	
				acc, p_accel = get_acceleration(myAccel, [thresh, alpha, p_accel,init_values])
								#Use the helper method to read from the accelerometer and 
								#obtain processed values for acceleration
				for i in range(3):
					avg_acc[0][i] += acc[i]

				time.sleep(0.001)		#A sleep of 0.001 secs to ensure the accerlerometer 
								#has enough time to read new values without much loss in data.
				count += 1			#Count of number of readings to compute average acceleration
				dt = time.time() - init_time	#Time elapsed in this iteration
			
			for i in range(3):
				avg_acc[0][i] /= count		#Compute average velocity of each of the component involved.

			change_in_position, u_x, u_y = compute_position(avg_acc, [0, 0], dt, u_x, u_y)
								#Compute the new displacement using the helper method
			
			current_position[0] += change_in_position[0]	#Obtain the new 'x' component of displacement 
			current_position[1] += change_in_position[1]	#Obtain the new 'y' component of displacement 

			q.put(current_position)			#Put the newly calculated position into the thread-safe queue.

	except KeyboardInterrupt:
		q.task_done()
		return
		exit
	
if __name__ == "__main__":
	myAccel, init_values = initialize()
	Q = Queue()
	main(myAccel,init_values,Q) 
