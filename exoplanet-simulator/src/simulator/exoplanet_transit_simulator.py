import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch
from matplotlib.gridspec import GridSpec
import matplotlib.colors as colors
from matplotlib.collections import LineCollection

class ExoplanetSystem:
    def __init__(self):
        self.star_radius = 1.0
        self.star_luminosity = 1.0
        
        self.planet1_radius = 0.009
        self.planet1_semi_major_axis = 1.0
        self.planet1_period = 365.25
        
        self.planet2_radius = 0.02
        self.planet2_semi_major_axis = 0.5
        self.planet2_period = 0.5 * 365.25 * np.sqrt(0.5**3)
        
        self.days_to_simulate = 14
        self.time_resolution = 200
        
        self.time_points = np.linspace(0, self.days_to_simulate, 
                                      self.days_to_simulate * self.time_resolution)
        
        self.calculate_positions()
        self.calculate_light_curve()
        self.calculate_light_rays()
    
    def calculate_positions(self):
        omega1 = 2 * np.pi / self.planet1_period
        omega2 = 2 * np.pi / self.planet2_period
        
        self.planet1_x = self.planet1_semi_major_axis * np.cos(omega1 * self.time_points)
        self.planet1_y = self.planet1_semi_major_axis * np.sin(omega1 * self.time_points)
        
        self.planet2_x = self.planet2_semi_major_axis * np.cos(omega2 * self.time_points)
        self.planet2_y = self.planet2_semi_major_axis * np.sin(omega2 * self.time_points)
    
    def calculate_light_curve(self):
        self.light_curve = np.ones_like(self.time_points)
        
        for i, t in enumerate(self.time_points):
            if abs(self.planet1_x[i]) < self.star_radius and self.planet1_y[i] < 0:
                blocked_area1 = np.pi * self.planet1_radius**2
                self.light_curve[i] -= blocked_area1 / (np.pi * self.star_radius**2)
            
            if abs(self.planet2_x[i]) < self.star_radius and self.planet2_y[i] < 0:
                blocked_area2 = np.pi * self.planet2_radius**2
                self.light_curve[i] -= blocked_area2 / (np.pi * self.star_radius**2)
        
        self.light_curve = np.maximum(self.light_curve, 0)
    
    def calculate_light_rays(self):
        self.num_rays = 15
        
        ray_positions = np.linspace(-self.star_radius * 0.9, self.star_radius * 0.9, self.num_rays)
        
        self.ray_visibility = np.ones((len(self.time_points), self.num_rays))
        
        for i, t in enumerate(self.time_points):
            for j, ray_pos in enumerate(ray_positions):
                if (self.planet1_y[i] < 0 and 
                    abs(ray_pos - self.planet1_x[i]) < self.planet1_radius):
                    self.ray_visibility[i, j] = 0
                
                if (self.planet2_y[i] < 0 and 
                    abs(ray_pos - self.planet2_x[i]) < self.planet2_radius):
                    self.ray_visibility[i, j] = 0
        
        self.ray_positions = ray_positions


class ExoplanetTransitVisualizer:
    def __init__(self, exoplanet_system):
        self.system = exoplanet_system
        self.setup_figure()
        
    def setup_figure(self):
        self.fig = plt.figure(figsize=(14, 10))
        gs = GridSpec(3, 1, height_ratios=[3, 1, 1])
        
        self.ax_system = self.fig.add_subplot(gs[0])
        self.ax_system.set_xlim(-1.5, 1.5)
        self.ax_system.set_ylim(-0.8, 0.8)
        self.ax_system.set_aspect('equal')
        self.ax_system.set_title('Exoplanet Transit Simulation', fontsize=16)
        self.ax_system.set_xlabel('Distance (AU)', fontsize=12)
        self.ax_system.set_ylabel('Distance (AU)', fontsize=12)
        self.ax_system.grid(True, linestyle='--', alpha=0.7)
        
        star_cmap = colors.LinearSegmentedColormap.from_list('star_cmap', ['#FFFF00', '#FFA500'])
        self.star = Circle((0, 0), self.system.star_radius, color=star_cmap(0.5), zorder=1)
        self.ax_system.add_patch(self.star)
        
        planet1_cmap = colors.LinearSegmentedColormap.from_list('planet1_cmap', ['#0077BE', '#00BFFF'])
        planet2_cmap = colors.LinearSegmentedColormap.from_list('planet2_cmap', ['#8B0000', '#FF4500'])
        
        self.planet1 = Circle((0, 0), self.system.planet1_radius, color=planet1_cmap(0.5), zorder=3)
        self.planet2 = Circle((0, 0), self.system.planet2_radius, color=planet2_cmap(0.5), zorder=3)
        self.ax_system.add_patch(self.planet1)
        self.ax_system.add_patch(self.planet2)
        
        self.rays = []
        for i in range(self.system.num_rays):
            ray_x = self.system.ray_positions[i]
            ray = FancyArrowPatch((ray_x, 0), (ray_x, -0.7), 
                                 color='yellow', alpha=0.7, linewidth=1.5,
                                 arrowstyle='->', mutation_scale=15, zorder=0)
            self.ax_system.add_patch(ray)
            self.rays.append(ray)
        
        observer_x = 0
        observer_y = -0.75
        observer = plt.Circle((observer_x, observer_y), 0.05, color='black', zorder=4)
        self.ax_system.add_patch(observer)
        self.ax_system.text(observer_x, observer_y - 0.1, 'Observer', 
                           ha='center', va='top', fontsize=10)
        
        orbit_arrow1 = FancyArrowPatch((self.system.planet1_semi_major_axis + 0.1, 0), 
                                      (self.system.planet1_semi_major_axis + 0.1, 0.2), 
                                      color='blue', arrowstyle='->', mutation_scale=15)
        orbit_arrow2 = FancyArrowPatch((self.system.planet2_semi_major_axis + 0.1, 0), 
                                      (self.system.planet2_semi_major_axis + 0.1, 0.2), 
                                      color='red', arrowstyle='->', mutation_scale=15)
        self.ax_system.add_patch(orbit_arrow1)
        self.ax_system.add_patch(orbit_arrow2)
        
        self.ax_light = self.fig.add_subplot(gs[1])
        self.ax_light.set_xlim(0, self.system.days_to_simulate)
        self.ax_light.set_ylim(0.995, 1.001)
        self.ax_light.set_title('Light Curve (Photometric Data)', fontsize=14)
        self.ax_light.set_xlabel('Time (days)', fontsize=12)
        self.ax_light.set_ylabel('Relative Brightness', fontsize=12)
        self.ax_light.grid(True, linestyle='--', alpha=0.7)
        
        self.light_line, = self.ax_light.plot([], [], 'k-', lw=2)
        
        self.time_line = self.ax_light.axvline(x=0, color='r', linestyle='-', alpha=0.7)
        
        self.ax_events = self.fig.add_subplot(gs[2])
        self.ax_events.set_xlim(0, self.system.days_to_simulate)
        self.ax_events.set_ylim(0, 1)
        self.ax_events.set_title('Transit Events Timeline', fontsize=14)
        self.ax_events.set_xlabel('Time (days)', fontsize=12)
        self.ax_events.set_yticks([0.25, 0.75])
        self.ax_events.set_yticklabels(['Planet 2', 'Planet 1'])
        self.ax_events.grid(True, linestyle='--', alpha=0.7)
        
        self.transit_markers1 = []
        self.transit_markers2 = []
        
        for i, t in enumerate(self.system.time_points):
            if (abs(self.system.planet1_x[i]) < self.system.star_radius and 
                self.system.planet1_y[i] < 0):
                rect = Rectangle((t, 0.7), 0.01, 0.1, color='blue', alpha=0.5)
                self.ax_events.add_patch(rect)
                self.transit_markers1.append(rect)
            
            if (abs(self.system.planet2_x[i]) < self.system.star_radius and 
                self.system.planet2_y[i] < 0):
                rect = Rectangle((t, 0.2), 0.01, 0.1, color='red', alpha=0.5)
                self.ax_events.add_patch(rect)
                self.transit_markers2.append(rect)
        
        self.event_time_line = self.ax_events.axvline(x=0, color='r', linestyle='-', alpha=0.7)
        
        self.ax_system.legend([self.star, self.planet1, self.planet2], 
                             ['Host Star', 'Planet 1 (Earth-like)', 'Planet 2 (Hot Jupiter)'],
                             loc='upper right', fontsize=10)
        
        self.ax_system.text(1.3, -0.6, 'Light Rays', color='yellow', fontsize=10, 
                           ha='center', bbox=dict(facecolor='black', alpha=0.5))
        
        self.fig.tight_layout()
    
    def init_animation(self):
        self.planet1.center = (0, 0)
        self.planet2.center = (0, 0)
        self.light_line.set_data([], [])
        self.time_line.set_xdata(0)
        self.event_time_line.set_xdata(0)
        
        for ray in self.rays:
            ray.set_visible(True)
        
        return [self.planet1, self.planet2, self.light_line, 
                self.time_line, self.event_time_line] + self.rays
    
    def animate(self, i):
        n_frames = len(self.system.time_points)
        i = i % n_frames
        
        self.planet1.center = (self.system.planet1_x[i], self.system.planet1_y[i])
        self.planet2.center = (self.system.planet2_x[i], self.system.planet2_y[i])
        
        if i == 0:
            self.light_line.set_data([], [])
        else:
            self.light_line.set_data(self.system.time_points[:i+1], self.system.light_curve[:i+1])
        
        current_time = self.system.time_points[i]
        self.time_line.set_xdata(current_time)
        self.event_time_line.set_xdata(current_time)
        
        for j, ray in enumerate(self.rays):
            ray.set_visible(bool(self.system.ray_visibility[i, j]))
            
            if self.system.ray_visibility[i, j]:
                ray.set_color('yellow')
            else:
                ray.set_color('red')
        
        return [self.planet1, self.planet2, self.light_line, 
                self.time_line, self.event_time_line] + self.rays
    
    def create_animation(self, save_path=None):
        n_frames = len(self.system.time_points)
        
        ani = animation.FuncAnimation(self.fig, self.animate, frames=n_frames,
                                     init_func=self.init_animation, blit=True, 
                                     interval=10)
        
        if save_path:
            ani.save(save_path, writer='ffmpeg', fps=60)
            print(f"Animation saved to {save_path}")
        
        plt.show()
        return ani


def main():
    print("Initializing enhanced exoplanet transit simulation...")
    
    system = ExoplanetSystem()
    
    visualizer = ExoplanetTransitVisualizer(system)
    
    print("Starting animation...")
    print("The simulation will loop continuously. Press Ctrl+C in the terminal to stop.")
    ani = visualizer.create_animation()
    
    plt.show()


if __name__ == "__main__":
    main()
