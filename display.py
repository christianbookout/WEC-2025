import math
import tkinter as tk
from tkinter import filedialog
from matplotlib.patches import Circle
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from data.parser import read_from_file
from solver.solve import load_city_boundary, generate_grid, solve_fire_hall_placement



# Base layout taken from this link:
# https://www.geeksforgeeks.org/how-to-embed-matplotlib-charts-in-tkinter-gui/

root = tk.Tk()
root.title("Cowgary Firehall Optimization")
fig = plt.Figure()
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack()

file_path = str()

def load_data():
    global file_path
    file_path = filedialog.askopenfilename()
    if file_path:
        print(f"Loading data from {file_path}")

        x, y = read_from_file(file_path)
        
        ax.clear()
        ax.plot(x, y, 'b')
        
        canvas.draw()
        canvas.get_tk_widget().pack()


def draw_circle(x, y, radius):
    circle = Circle((x, y), radius, color='red', fill=False, linewidth=2)
    
    ax.add_patch(circle)
    ax.figure.canvas.draw()


def solve_placement():
    global file_path
    if file_path:
        print("Solving placement")

        city_polygon = load_city_boundary(file_path)

        candidate_locations = generate_grid(city_polygon, 2)

        # # map candidate locations
        # for loc in candidate_locations:
        #     ax.plot(loc.x, loc.y, 'bo')

        points_to_cover = generate_grid(city_polygon, 1)

        
        for pt in points_to_cover:
            ax.plot(pt.x, pt.y, 'go')

        # https://stackoverflow.com/questions/1253499/simple-calculations-for-working-with-lat-lon-and-km-distance
        # 1 deg = math.cos(math.radians(loc[0].y)) * 111.320
        # convert 2.5 km to degrees using that formula
        rad = 2.5 / (111.320 * math.cos(math.radians(candidate_locations[0].y)))
        print("radius is", rad)

        fire_hall_locations = solve_fire_hall_placement(candidate_locations, points_to_cover, rad)

        ax.clear()
        ax.plot(*zip(*city_polygon.exterior.coords), 'b-', label="City Boundary")

        for loc in fire_hall_locations:
            print(f"Fire Hall Location: {loc.x}, {loc.y}")
            ax.plot(loc.x, loc.y, 'ro')
            draw_circle(loc.x, loc.y, rad)

        ax.legend()
        canvas.draw()
        canvas.get_tk_widget().pack()
            

buttons = tk.Frame(root)
buttons.pack()

load_data_button = tk.Button(buttons, text="Load From CSV", command=load_data)
load_data_button.pack(side=tk.LEFT, padx=20, pady=20)

make_circles_button = tk.Button(buttons, text="Generate Optimal Coverage", command=solve_placement)
make_circles_button.pack(side=tk.RIGHT, padx=20, pady=20)

root.mainloop()
