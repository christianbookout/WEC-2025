import math
import tkinter as tk
from tkinter import filedialog
from matplotlib.patches import Circle
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from data.parser import read_from_file

# Base layout taken from this link:
# https://www.geeksforgeeks.org/how-to-embed-matplotlib-charts-in-tkinter-gui/

root = tk.Tk()
root.title("Cowgary Firehall Optimization")
fig = plt.Figure()
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack()

def load_data():
    file_path = filedialog.askopenfilename()
    if file_path:
        x, y = read_from_file(file_path)
        
        ax.clear()
        ax.plot(x, y, 'b')
        draw_circle(x[0], y[0])
        
        canvas.draw()
        canvas.get_tk_widget().pack()

def draw_circle(x, y, radius_km=2.5):
    # visually estimate the radius of the circle based on lat long coordinates
    # very much an estimate but it works since it's just visual I guess
    # https://stackoverflow.com/questions/1253499/simple-calculations-for-working-with-lat-lon-and-km-distance
    radius_lat = radius_km / 110.574
    radius_lon = radius_km / (111.320 * math.cos(math.radians(y)))
    circle = Circle((x, y), max(radius_lat, radius_lon), color='red', fill=False, linewidth=2)
    
    ax.add_patch(circle)
    ax.figure.canvas.draw()

buttons = tk.Frame(root)
buttons.pack()

load_data_button = tk.Button(buttons, text="Load From CSV", command=load_data)
load_data_button.pack(side=tk.LEFT, padx=20, pady=20)

make_circles_button = tk.Button(buttons, text="Generate Optimal Coverage", command=lambda: print("Generate Circles"))
make_circles_button.pack(side=tk.RIGHT, padx=20, pady=20)

root.mainloop()
