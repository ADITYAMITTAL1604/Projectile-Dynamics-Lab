import numpy as np
from scipy.integrate import solve_ivp

class ProjectileSimulator:
    def __init__(self):
        # Physical constants
        self.g_earth = 9.81
        self.g_moon = 1.62
        self.g_mars = 3.71
        self.g_jupiter = 24.79
        
        # Air densities (kg/m³)
        self.rho_earth = 1.225
        self.rho_moon = 0.0
        self.rho_mars = 0.02
        self.rho_jupiter = 0.16
        
        # Current values
        self.g = self.g_earth
        self.rho = self.rho_earth
        self.Cd = 0.47  # Drag coefficient for sphere
        
    def set_environment(self, planet: str):
        """Set gravity and air density based on planet"""
        planet_lower = planet.lower()
        if 'earth' in planet_lower:
            self.g = self.g_earth
            self.rho = self.rho_earth
        elif 'moon' in planet_lower:
            self.g = self.g_moon
            self.rho = self.rho_moon
        elif 'mars' in planet_lower:
            self.g = self.g_mars
            self.rho = self.rho_mars
        elif 'jupiter' in planet_lower:
            self.g = self.g_jupiter
            self.rho = self.rho_jupiter
        else:
            self.g = self.g_earth
            self.rho = self.rho_earth
            
    def without_air_resistance(self, u: float, theta: float, 
                              g: float = None) -> tuple:
        """Analytical solution without drag"""
        if g is None:
            g = self.g
            
        theta_rad = np.radians(theta)
        
        # Calculate time of flight
        t_flight = 2 * u * np.sin(theta_rad) / g
        
        # Generate time array
        t = np.linspace(0, t_flight, 200)
        
        # Calculate positions
        x = u * np.cos(theta_rad) * t
        y = u * np.sin(theta_rad) * t - 0.5 * g * t**2
        
        # Filter out negative y values
        valid = y >= 0
        return x[valid], y[valid]
    
    def _drag_equation(self, t: float, state: list, mass: float, radius: float) -> list:
        """ODE function for drag force - FIXED VERSION"""
        vx, vy, x, y = state
        v = np.sqrt(vx**2 + vy**2)
        
        # Default gravity acceleration
        ax = 0
        ay = -self.g
        
        # Add drag if velocity > 0 and air density > 0
        if v > 0.01 and self.rho > 0.001:
            # Cross-sectional area
            A = np.pi * radius**2
            
            # DRAG FORCE: F_d = 0.5 * ρ * Cd * A * v²
            drag_magnitude = 0.5 * self.rho * self.Cd * A * v**2
            
            # Drag acceleration components (a_drag = F_d / m)
            # Direction opposite to velocity
            ax_drag = -drag_magnitude * (vx / v) / mass
            ay_drag = -drag_magnitude * (vy / v) / mass
            
            # Total acceleration = gravity + drag
            ax = ax_drag
            ay = ay - drag_magnitude * (vy / v) / mass
        
        return [ax, ay, vx, vy]
    
    def with_air_resistance(self, u: float, theta: float, 
                           mass: float = 0.1, 
                           radius: float = 0.05) -> tuple:
        """Numerical solution with drag - IMPROVED"""
        theta_rad = np.radians(theta)
        
        # Initial conditions [vx, vy, x, y]
        initial_state = [
            u * np.cos(theta_rad),  # vx
            u * np.sin(theta_rad),  # vy
            0.0,                    # x
            0.0                     # y
        ]
        
        # Event to stop when projectile hits ground
        def hit_ground(t, state):
            return state[3]  # y position
        hit_ground.terminal = True
        hit_ground.direction = -1
        
        # Time span (max 50 seconds for safety)
        t_span = (0, 50)
        
        try:
            # Solve ODE with higher precision
            solution = solve_ivp(
                fun=lambda t, y: self._drag_equation(t, y, mass, radius),
                t_span=t_span,
                y0=initial_state,
                method='RK45',
                events=[hit_ground],
                max_step=0.001,  # Smaller step for accuracy
                rtol=1e-9,
                atol=1e-12,
                dense_output=True
            )
            
            # Extract solution
            if len(solution.t) > 0:
                t_sol = solution.t
                x_sol = solution.y[2]
                y_sol = solution.y[3]
                
                # Filter positive y values
                valid = y_sol >= -0.01  # Small tolerance for ground impact
                if np.any(valid):
                    return t_sol[valid], x_sol[valid], y_sol[valid]
            
            # Fallback if no valid solution
            return self._simple_drag_model(u, theta, mass, radius)
            
        except Exception as e:
            print(f"ODE solver error: {e}")
            return self._simple_drag_model(u, theta, mass, radius)
    
    def _simple_drag_model(self, u: float, theta: float, 
                          mass: float, radius: float) -> tuple:
        """Simple Euler integration fallback - IMPROVED"""
        theta_rad = np.radians(theta)
        dt = 0.0005  # Smaller time step for accuracy
        
        # Initial values
        vx = u * np.cos(theta_rad)
        vy = u * np.sin(theta_rad)
        x, y = 0, 0
        
        # Store results
        t_list, x_list, y_list = [0], [0], [0]
        
        # Cross-sectional area
        A = np.pi * radius**2
        
        # Simulation loop
        max_steps = 20000
        for step in range(max_steps):
            if y < -0.01:  # Stop when below ground
                break
            
            v = np.sqrt(vx**2 + vy**2)
            
            # Calculate drag if applicable
            if v > 0.01 and self.rho > 0.001:
                drag = 0.5 * self.rho * self.Cd * A * v**2
                ax_drag = -drag * vx / (mass * v)
                ay_drag = -drag * vy / (mass * v)
            else:
                ax_drag = 0
                ay_drag = 0
            
            # Update velocities (Euler integration)
            vx += ax_drag * dt
            vy += (-self.g + ay_drag) * dt
            
            # Update positions
            x += vx * dt
            y += vy * dt
            
            # Store results
            t_list.append(t_list[-1] + dt)
            x_list.append(x)
            y_list.append(y)
        
        return np.array(t_list), np.array(x_list), np.array(y_list)

# Test function
if __name__ == "__main__":
    # Test the simulation
    sim = ProjectileSimulator()
    sim.set_environment('earth')
    
    print("Testing drag effect...")
    
    # Test without drag
    x_ideal, y_ideal = sim.without_air_resistance(30, 45)
    print(f"Ideal range: {x_ideal[-1]:.2f} m")
    
    # Test with drag
    t_real, x_real, y_real = sim.with_air_resistance(30, 45, mass=0.1, radius=0.05)
    print(f"Real range with drag: {x_real[-1]:.2f} m")
    
    # Calculate efficiency
    if len(x_ideal) > 0 and len(x_real) > 0:
        efficiency = (x_real[-1] / x_ideal[-1]) * 100
        print(f"Efficiency: {efficiency:.1f}%")
        print(f"Drag reduction: {100 - efficiency:.1f}%")