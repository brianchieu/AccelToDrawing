def compute_position(accel, init_position, delta_t, u_x, u_y):
    
	s_x,s_y = init_position
	delta_t_sq_half = 0.5 * (delta_t**2)

	for x,y,z in accel:
		v_x = (u_x + delta_t * x) if x != 0.0  else 0.0
		v_y = (u_y + delta_t * y) if y != 0.0 else 0.0
		
		s_x += (u_x * delta_t + x * delta_t_sq_half)
		s_y += (u_y * delta_t + y * delta_t_sq_half)
		u_x, u_y = v_x,v_y

	return [s_x, s_y], v_x, v_y