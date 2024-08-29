class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp  # Proportional gain
        self.ki = ki  # Integral gain
        self.kd = kd  # Derivative gain
        self.integral = 0
        self.previous_error = 0

    def update(self, error, dt):
        # Proportional 
        proportional = self.kp * error

        # Integral 
        self.integral += error * dt
        integral = self.ki * self.integral

        # Derivative 
        derivative = self.kd * (error - self.previous_error) / dt
        self.previous_error = error

        # Total output
        return proportional + integral + derivative
