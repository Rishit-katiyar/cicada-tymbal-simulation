import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parameters
num_frames = 100  # Number of frames in the animation
num_segments = 100  # Number of segments in the tymbal muscle
tymbal_length = 1.0  # Length of the tymbal muscle
wave_speed_factor = 0.5  # Factor for wave speed variation
damping_factor = 0.01  # Damping factor for realism
t = np.linspace(0, tymbal_length, num_segments)

# Initial displacement of the tymbal muscle with varying amplitude
initial_displacement = np.sin(2 * np.pi * t) * np.exp(-5 * t) * (1 - np.linspace(0, 1, num_segments)**2)  # Non-uniform initial displacement

# Function to update the plot for each frame
def update(frame):
    ax.clear()
    wave_speed = wave_speed_factor * (1 - np.sin(2 * np.pi * frame / num_frames))  # Variable wave speed
    displacement = initial_displacement * np.cos(2 * np.pi * wave_speed * frame / num_frames) * np.exp(-damping_factor * frame)  # Damped wave
    ax.plot(t, displacement, color='b')
    ax.set_xlim(0, tymbal_length)
    ax.set_ylim(-1.2, 1.2)
    ax.set_title(f'Time Step: {frame}/{num_frames}')

# Create a figure and axis
fig, ax = plt.subplots()

# Animate
ani = FuncAnimation(fig, update, frames=num_frames, interval=50)

# Save animation as GIF
ani.save('tymbal_animation.gif', writer='imagemagick')

plt.show()
