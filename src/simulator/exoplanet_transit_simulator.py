import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch
from matplotlib.gridspec import GridSpec
import matplotlib.colors as colors
from matplotlib.collections import LineCollection

class ExoplanetSystem:
    """
    Simulates a star system with two exoplanets and calculates transit photometry.
    """
    def __init__(self):
        # Star properties (based on Sun)
        self.star_radius = 1.0  # Solar radius (normalized)
        self.star_luminosity = 1.0  # Solar luminosity (normalized)
        
        # Planet 1 properties (Earth-like)
        self.planet1_radius = 0.009  # Earth radius relative to Sun (scaled)
        self.planet1_semi_major_axis = 1.0  # 1 AU
        self.planet1_period = 365.25  # days
        
        # Planet 2 properties (closer, larger planet)
        self.planet2_radius = 0.02  # Larger than Earth
        self.planet2_semi_major_axis = 0.5  # 0.5 AU
        self.planet2_period = 0.5 * 365.25 * np.sqrt(0.5**3)  # Kepler's third law
        
        # Simulation parameters
        self.days_to_simulate = 14  # Two-week period
        self.time_resolution = 200  # Points per day (increased for smoother animation)
        
        # Initialize time array
        self.time_points = np.linspace(0, self.days_to_simulate, 
                                      self.days_to_simulate * self.time_resolution)
        
        # Calculate planet positions and light curve
        self.calculate_positions()
        self.calculate_light_curve()
        self.calculate_light_rays()
    
    def calculate_positions(self):
        """Calculate positions of planets over time."""
        # Convert periods to angular velocities
        omega1 = 2 * np.pi / self.planet1_period
        omega2 = 2 * np.pi / self.planet2_period
        
        # Calculate orbital positions (assuming circular orbits and edge-on view)
        # X is the horizontal position (in the plane of sky)
        # Y is the position along line of sight (positive is behind the star)
        
        # Planet 1
        self.planet1_x = self.planet1_semi_major_axis * np.cos(omega1 * self.time_points)
        self.planet1_y = self.planet1_semi_major_axis * np.sin(omega1 * self.time_points)
        
        # Planet 2
        self.planet2_x = self.planet2_semi_major_axis * np.cos(omega2 * self.time_points)
        self.planet2_y = self.planet2_semi_major_axis * np.sin(omega2 * self.time_points)
    
    def calculate_light_curve(self):
        """Calculate the light curve based on planet transits."""
        # Initialize light curve at full brightness
        self.light_curve = np.ones_like(self.time_points)
        
        # For each time point, check if planets are transiting
        for i, t in enumerate(self.time_points):
            # Planet is transiting if |x| < star_radius and y < 0 (in front of star)
            
            # Check planet 1
            if abs(self.planet1_x[i]) < self.star_radius and self.planet1_y[i] < 0:
                # Calculate how much of the star is blocked (simplified model)
                blocked_area1 = np.pi * self.planet1_radius**2
                self.light_curve[i] -= blocked_area1 / (np.pi * self.star_radius**2)
            
            # Check planet 2
            if abs(self.planet2_x[i]) < self.star_radius and self.planet2_y[i] < 0:
                # Calculate how much of the star is blocked (simplified model)
                blocked_area2 = np.pi * self.planet2_radius**2
                self.light_curve[i] -= blocked_area2 / (np.pi * self.star_radius**2)
        
        # Ensure light curve doesn't go below 0 (shouldn't happen with realistic parameters)
        self.light_curve = np.maximum(self.light_curve, 0)
    
    def calculate_light_rays(self):
        """Calculate the visibility of light rays at each time point."""
        # Number of light rays to simulate
        self.num_rays = 15
        
        # Ray positions across the star (evenly spaced)
        ray_positions = np.linspace(-self.star_radius * 0.9, self.star_radius * 0.9, self.num_rays)
        
        # Initialize ray visibility array (1 = visible, 0 = blocked)
        self.ray_visibility = np.ones((len(self.time_points), self.num_rays))
        
        # For each time point, check if rays are blocked by planets
        for i, t in enumerate(self.time_points):
            for j, ray_pos in enumerate(ray_positions):
                # Check if ray is blocked by planet 1
                if (self.planet1_y[i] < 0 and  # Planet is in front of star
                    abs(ray_pos - self.planet1_x[i]) < self.planet1_radius):
                    self.ray_visibility[i, j] = 0
                
                # Check if ray is blocked by planet 2
                if (self.planet2_y[i] < 0 and  # Planet is in front of star
                    abs(ray_pos - self.planet2_x[i]) < self.planet2_radius):
                    self.ray_visibility[i, j] = 0
        
        # Store ray positions for visualization
        self.ray_positions = ray_positions


class ExoplanetTransitVisualizer:
    """
    Creates an animation of exoplanet transits and the resulting light curve.
    """
    def __init__(self, exoplanet_system):
        self.system = exoplanet_system
        self.setup_figure()
        
    def setup_figure(self):
        """Set up the figure and axes for animation."""
        self.fig = plt.figure(figsize=(14, 10))
        gs = GridSpec(3, 1, height_ratios=[3, 1, 1])
        
        # Top subplot for the star system visualization
        self.ax_system = self.fig.add_subplot(gs[0])
        self.ax_system.set_xlim(-1.5, 1.5)
        self.ax_system.set_ylim(-0.8, 0.8)
        self.ax_system.set_aspect('equal')
        self.ax_system.set_title('Exoplanet Transit Simulation', fontsize=16)
        self.ax_system.set_xlabel('Distance (AU)', fontsize=12)
        self.ax_system.set_ylabel('Distance (AU)', fontsize=12)
        self.ax_system.grid(True, linestyle='--', alpha=0.7)
        
        # Create star with gradient color
        star_cmap = colors.LinearSegmentedColormap.from_list('star_cmap', ['#FFFF00', '#FFA500'])
        self.star = Circle((0, 0), self.system.star_radius, color=star_cmap(0.5), zorder=1)
        self.ax_system.add_patch(self.star)
        
        # Create planets with gradient colors
        planet1_cmap = colors.LinearSegmentedColormap.from_list('planet1_cmap', ['#0077BE', '#00BFFF'])
        planet2_cmap = colors.LinearSegmentedColormap.from_list('planet2_cmap', ['#8B0000', '#FF4500'])
        
        self.planet1 = Circle((0, 0), self.system.planet1_radius, color=planet1_cmap(0.5), zorder=3)
        self.planet2 = Circle((0, 0), self.system.planet2_radius, color=planet2_cmap(0.5), zorder=3)
        self.ax_system.add_patch(self.planet1)
        self.ax_system.add_patch(self.planet2)
        
        # Create light rays
        self.rays = []
        for i in range(self.system.num_rays):
            # Create a ray from the star to the observer (bottom of the plot)
            ray_x = self.system.ray_positions[i]
            ray = FancyArrowPatch((ray_x, 0), (ray_x, -0.7), 
                                 color='yellow', alpha=0.7, linewidth=1.5,
                                 arrowstyle='->', mutation_scale=15, zorder=0)
            self.ax_system.add_patch(ray)
            self.rays.append(ray)
        
        # Add observer icon at bottom
        observer_x = 0
        observer_y = -0.75
        observer = plt.Circle((observer_x, observer_y), 0.05, color='black', zorder=4)
        self.ax_system.add_patch(observer)
        self.ax_system.text(observer_x, observer_y - 0.1, 'Observer', 
                           ha='center', va='top', fontsize=10)
        
        # Add direction of orbit arrows
        orbit_arrow1 = FancyArrowPatch((self.system.planet1_semi_major_axis + 0.1, 0), 
                                      (self.system.planet1_semi_major_axis + 0.1, 0.2), 
                                      color='blue', arrowstyle='->', mutation_scale=15)
        orbit_arrow2 = FancyArrowPatch((self.system.planet2_semi_major_axis + 0.1, 0), 
                                      (self.system.planet2_semi_major_axis + 0.1, 0.2), 
                                      color='red', arrowstyle='->', mutation_scale=15)
        self.ax_system.add_patch(orbit_arrow1)
        self.ax_system.add_patch(orbit_arrow2)
        
        # Middle subplot for the light curve
        self.ax_light = self.fig.add_subplot(gs[1])
        self.ax_light.set_xlim(0, self.system.days_to_simulate)
        self.ax_light.set_ylim(0.995, 1.001)  # Adjusted to show small dips
        self.ax_light.set_title('Light Curve (Photometric Data)', fontsize=14)
        self.ax_light.set_xlabel('Time (days)', fontsize=12)
        self.ax_light.set_ylabel('Relative Brightness', fontsize=12)
        self.ax_light.grid(True, linestyle='--', alpha=0.7)
        
        # Initialize light curve line
        self.light_line, = self.ax_light.plot([], [], 'k-', lw=2)
        
        # Add vertical line to track current time
        self.time_line = self.ax_light.axvline(x=0, color='r', linestyle='-', alpha=0.7)
        
        # Bottom subplot for the transit events annotation
        self.ax_events = self.fig.add_subplot(gs[2])
        self.ax_events.set_xlim(0, self.system.days_to_simulate)
        self.ax_events.set_ylim(0, 1)
        self.ax_events.set_title('Transit Events Timeline', fontsize=14)
        self.ax_events.set_xlabel('Time (days)', fontsize=12)
        self.ax_events.set_yticks([0.25, 0.75])
        self.ax_events.set_yticklabels(['Planet 2', 'Planet 1'])
        self.ax_events.grid(True, linestyle='--', alpha=0.7)
        
        # Create transit event markers
        self.transit_markers1 = []
        self.transit_markers2 = []
        
        # Find transit events
        for i, t in enumerate(self.system.time_points):
            # Planet 1 transit
            if (abs(self.system.planet1_x[i]) < self.system.star_radius and 
                self.system.planet1_y[i] < 0):
                rect = Rectangle((t, 0.7), 0.01, 0.1, color='blue', alpha=0.5)
                self.ax_events.add_patch(rect)
                self.transit_markers1.append(rect)
            
            # Planet 2 transit
            if (abs(self.system.planet2_x[i]) < self.system.star_radius and 
                self.system.planet2_y[i] < 0):
                rect = Rectangle((t, 0.2), 0.01, 0.1, color='red', alpha=0.5)
                self.ax_events.add_patch(rect)
                self.transit_markers2.append(rect)
        
        # Add current time marker
        self.event_time_line = self.ax_events.axvline(x=0, color='r', linestyle='-', alpha=0.7)
        
        # Add legend
        self.ax_system.legend([self.star, self.planet1, self.planet2], 
                             ['Host Star', 'Planet 1 (Earth-like)', 'Planet 2 (Hot Jupiter)'],
                             loc='upper right', fontsize=10)
        
        # Add annotation for light rays
        self.ax_system.text(1.3, -0.6, 'Light Rays', color='yellow', fontsize=10, 
                           ha='center', bbox=dict(facecolor='black', alpha=0.5))
        
        self.fig.tight_layout()
    
    def init_animation(self):
        """Initialize the animation."""
        self.planet1.center = (0, 0)
        self.planet2.center = (0, 0)
        self.light_line.set_data([], [])
        self.time_line.set_xdata(0)
        self.event_time_line.set_xdata(0)
        
        # Initialize all rays as visible
        for ray in self.rays:
            ray.set_visible(True)
        
        return [self.planet1, self.planet2, self.light_line, 
                self.time_line, self.event_time_line] + self.rays
    
    def animate(self, i):
        """Update the animation for frame i."""
        # For continuous looping
        n_frames = len(self.system.time_points)
        i = i % n_frames  # Wrap around to beginning when reaching the end
        
        # Update planet positions
        self.planet1.center = (self.system.planet1_x[i], self.system.planet1_y[i])
        self.planet2.center = (self.system.planet2_x[i], self.system.planet2_y[i])
        
        # Update light curve (show up to current time)
        # For continuous looping, we need to handle the case where we're starting over
        if i == 0:
            self.light_line.set_data([], [])
        else:
            self.light_line.set_data(self.system.time_points[:i+1], self.system.light_curve[:i+1])
        
        # Update time markers
        current_time = self.system.time_points[i]
        self.time_line.set_xdata(current_time)
        self.event_time_line.set_xdata(current_time)
        
        # Update light ray visibility
        for j, ray in enumerate(self.rays):
            ray.set_visible(bool(self.system.ray_visibility[i, j]))
            
            # Adjust ray color based on whether it's blocked
            if self.system.ray_visibility[i, j]:
                ray.set_color('yellow')
            else:
                # Make blocked rays red and more visible
                ray.set_color('red')
        
        return [self.planet1, self.planet2, self.light_line, 
                self.time_line, self.event_time_line] + self.rays
    
    def create_animation(self, save_path=None):
        """Create and display the animation."""
        n_frames = len(self.system.time_points)
        
        # Create animation with continuous looping
        ani = animation.FuncAnimation(self.fig, self.animate, frames=n_frames,
                                     init_func=self.init_animation, blit=True, 
                                     interval=10)  # Faster interval for smoother animation
        
        if save_path:
            # Use a higher fps for smoother saved animation
            ani.save(save_path, writer='ffmpeg', fps=60)
            print(f"Animation saved to {save_path}")
        
        plt.show()
        return ani


def main():
    """Main function to run the simulation."""
    print("Initializing enhanced exoplanet transit simulation...")
    
    # Create the exoplanet system
    system = ExoplanetSystem()
    
    # Create the visualizer
    visualizer = ExoplanetTransitVisualizer(system)
    
    # Run the animation
    print("Starting animation...")
    print("The simulation will loop continuously. Press Ctrl+C in the terminal to stop.")
    ani = visualizer.create_animation()
    
    # Keep the plot window open
    plt.show()


if __name__ == "__main__":
    main()
