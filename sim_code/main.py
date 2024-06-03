import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def get_input(prompt, default, cast_func, condition=lambda x: True):

    while True:
        try:
            user_input = input(f"{prompt} (default: {default}): ").strip()
            if not user_input:
                return default
            value = cast_func(user_input)
            if condition(value):
                return value
            else:
                print("Input does not meet the required condition.")
        except ValueError:
            print("Invalid input. Please enter a valid value.")

def ask_customization():

    while True:
        choice = input("Do you want to use default settings? (y/n): ").strip().lower()
        if choice in ['y', 'n']:
            return choice == 'n'
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def get_config():

    if ask_customization():
        config = {
            'num_frames': get_input("Enter number of frames in the animation", 100, int, lambda x: x > 0),
            'num_segments': get_input("Enter number of segments in the tymbal muscle", 100, int, lambda x: x > 0),
            'tymbal_length': get_input("Enter the length of the tymbal muscle", 1.0, float, lambda x: x > 0),
            'wave_speed_factor': get_input("Enter the factor for wave speed variation", 0.5, float, lambda x: x > 0),
            'damping_factor': get_input("Enter the damping factor for realism", 0.01, float, lambda x: x >= 0),
            'amplitude_decay_rate': get_input("Enter the rate of exponential decay of initial amplitude", 5, float, lambda x: x >= 0),
            'initial_displacement_factor': get_input("Enter the factor for initial displacement frequency", 2 * np.pi, float, lambda x: x >= 0),
            'wave_frequency': get_input("Enter the frequency of the wave", 2 * np.pi, float, lambda x: x >= 0),
            'line_color': get_input("Enter the color of the wave line", 'b', str),
            'line_width': get_input("Enter the width of the wave line", 2, float, lambda x: x > 0),
            'x_lim': (0, get_input("Enter the upper limit of the x-axis", 1.0, float, lambda x: x > 0)),
            'y_lim': (-1.2, 1.2),
            'plot_title': get_input("Enter the plot title", 'Tymbal Muscle Displacement', str),
            'frame_interval': get_input("Enter the interval between frames in milliseconds", 50, int, lambda x: x > 0)
        }
    else:
        config = {
            'num_frames': 100,
            'num_segments': 100,
            'tymbal_length': 1.0,
            'wave_speed_factor': 0.5,
            'damping_factor': 0.01,
            'amplitude_decay_rate': 5,
            'initial_displacement_factor': 2 * np.pi,
            'wave_frequency': 2 * np.pi,
            'line_color': 'b',
            'line_width': 2,
            'x_lim': (0, 1.0),
            'y_lim': (-1.2, 1.2),
            'plot_title': 'Tymbal Muscle Displacement',
            'frame_interval': 50
        }
    return config

def generate_positions(config):

    return np.linspace(0, config['tymbal_length'], config['num_segments'])

def generate_initial_displacement(t, config):

    return (
        np.sin(config['initial_displacement_factor'] * t) * 
        np.exp(-config['amplitude_decay_rate'] * t) * 
        (1 - np.linspace(0, 1, config['num_segments'])**2)
    )

def update(frame, t, initial_displacement, ax, config):

    ax.clear()
    wave_speed = config['wave_speed_factor'] * (1 - np.sin(config['wave_frequency'] * frame / config['num_frames']))
    displacement = (
        initial_displacement * 
        np.cos(config['wave_frequency'] * wave_speed * frame / config['num_frames']) * 
        np.exp(-config['damping_factor'] * frame)
    )
    ax.plot(t, displacement, color=config['line_color'], linewidth=config['line_width'])
    ax.set_xlim(config['x_lim'])
    ax.set_ylim(config['y_lim'])
    ax.set_title(f'{config["plot_title"]}\nTime Step: {frame}/{config["num_frames"]}')

def create_animation(config):

    t = generate_positions(config)
    initial_displacement = generate_initial_displacement(t, config)
    
    fig, ax = plt.subplots()
    ani = FuncAnimation(fig, update, fargs=(t, initial_displacement, ax, config), frames=config['num_frames'], interval=config['frame_interval'])
    plt.show()

# Main execution
if __name__ == "__main__":
    config = get_config()
    create_animation(config)
