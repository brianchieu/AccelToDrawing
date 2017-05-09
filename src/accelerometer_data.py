import time
import copy
from helper_functions.update_pos import *
from helper_functions.get_accel import *
from helper_functions.initialize import *
from Queue import Queue

g = 980.665
thresh = 30
delta_t = 0.05
no_of_samples = 1
sample_number = 5

def main(myAccel, init_values, q):
	p_accel = [0,0,0]
	alpha = 0.99
	u_x = 0
	u_y = 0
	
	try:
		current_position = [0,0]
		while(True):
			avg_acc = [[0,0,0]]
			init_time = time.time()
			dt = 0
			count = 0
			while ( dt < 0.2):	
				acc, p_accel = get_acceleration(myAccel, [thresh, alpha, p_accel,init_values])
				for i in range(3):
					avg_acc[0][i] += acc[i]

				time.sleep(0.001)
				count += 1
				dt = time.time() - init_time
			
			for i in range(3):
				avg_acc[0][i] /= count
			print avg_acc
			change_in_position, u_x, u_y = compute_position(avg_acc, [0, 0], dt, u_x, u_y)
			current_position[0] += change_in_position[0]
			current_position[1] += change_in_position[1]
			print current_position
			q.put(current_position)

	except KeyboardInterrupt:
		q.task_done()
		return
		exit
	
if __name__ == "__main__":
	myAccel, init_values = initialize()
	Q = Queue()
	main(myAccel,init_values,Q) 