import math
import tkinter as tk
from tkinter import filedialog
from matplotlib.patches import Circle
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from shapely import Point
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
    # circle = Circle((x, y), radius, color='red', fill=, linewidth=2)
    # fill with opaque red
    circle = Circle((x, y), radius, color='red', alpha=0.2, linewidth=2)
    ax.add_patch(circle)
    ax.figure.canvas.draw()

def solve_placement_1963():
    solve_placement("data/coordinates1963.csv")

def solve_placement_2005():
    solve_placement("data/coordinates2005.csv")

def solve_placement_2011():
    solve_placement("data/coordinates2011.csv")

def solve_placement(file_name):
    print("Solving placement")
    city_polygon_1 = load_city_boundary(file_name)
    candidate_locations_1 = generate_grid(city_polygon_1, 2)
    points_to_cover_1 = generate_grid(city_polygon_1, 1)

    # https://stackoverflow.com/questions/1253499/simple-calculations-for-working-with-lat-lon-and-km-distance
    # 1 deg = math.cos(math.radians(loc[0].y)) * 111.320
    # convert 2.5 km to degrees using that formula
    rad = 2.5 / (111.320 * math.cos(math.radians(candidate_locations_1[0].y)))

    fire_hall_locations_1 = solve_fire_hall_placement(candidate_locations_1, points_to_cover_1, rad)
    print(len(fire_hall_locations_1))

    ax.clear()
    ax.plot(*zip(*city_polygon_1.exterior.coords), 'b-', label="City Boundary")

    print(f"Total fire halls: {len(fire_hall_locations_1)}")

    for loc in fire_hall_locations_1:
        ax.plot(loc.x, loc.y, 'bo')
        draw_circle(loc.x, loc.y, rad)

    # ax.legend()
    canvas.draw()
    canvas.get_tk_widget().pack()

def solve_all():
    print("Solving placement")
    csv_map1 = "data/coordinates1963.csv"
    city_polygon_1 = load_city_boundary(csv_map1)
    candidate_locations_1 = generate_grid(city_polygon_1, 2)
    points_to_cover_1 = generate_grid(city_polygon_1, 1)

    # https://stackoverflow.com/questions/1253499/simple-calculations-for-working-with-lat-lon-and-km-distance
    # 1 deg = math.cos(math.radians(loc[0].y)) * 111.320
    # convert 2.5 km to degrees using that formula
    rad = 2.5 / (111.320 * math.cos(math.radians(candidate_locations_1[0].y)))

    fire_hall_locations_1 = solve_fire_hall_placement(candidate_locations_1, points_to_cover_1, rad)

    csv_map2 = "data/coordinates2005.csv"
    city_polygon_2 = load_city_boundary(csv_map2)
    difference_polygon = city_polygon_2.difference(city_polygon_1)
    candidate_locations_2 = generate_grid(difference_polygon, 2)
    points_to_cover_2 = generate_grid(difference_polygon, 1)
    points_to_cover_2 = [point for point in points_to_cover_2 if all([point.distance(fire_hall) > rad for fire_hall in fire_hall_locations_1])]
    fixed_halls = [candidate_locations_1.index(fh) for fh in fire_hall_locations_1]

    fire_hall_locations_2 = solve_fire_hall_placement(candidate_locations_2, points_to_cover_2, rad, fixed_halls=fixed_halls)
    
    csv_map3 = "data/coordinates2011.csv"
    city_polygon_3 = load_city_boundary(csv_map3)
    difference_polygon = city_polygon_3.difference(city_polygon_2)
    candidate_locations_3 = generate_grid(difference_polygon, 2)
    points_to_cover_3 = generate_grid(difference_polygon, 1)
    points_to_cover_3 = [point for point in points_to_cover_3 if all([point.distance(fire_hall) > rad for fire_hall in fire_hall_locations_2])]
    fixed_halls = fixed_halls + [candidate_locations_2.index(fh) for fh in fire_hall_locations_2]


    fire_hall_locations_3 = solve_fire_hall_placement(candidate_locations_3, points_to_cover_3, rad, fixed_halls=fixed_halls)

    ax.clear()
    ax.plot(*zip(*city_polygon_1.exterior.coords), 'b-', label="1963 City Boundary")
    ax.plot(*zip(*city_polygon_2.exterior.coords), 'g-', label="2005 City Boundary")
    ax.plot(*zip(*city_polygon_3.exterior.coords), 'y-', label="2011 City Boundary")

    fire_hall_locations = fire_hall_locations_1 + fire_hall_locations_2 + fire_hall_locations_3

    print(f"Total fire halls: {len(fire_hall_locations)}")

    for loc in fire_hall_locations:
        ax.plot(loc.x, loc.y, 'bo')
        draw_circle(loc.x, loc.y, rad)

    # ax.legend()
    canvas.draw()
    canvas.get_tk_widget().pack()
            

buttons = tk.Frame(root)
buttons.pack()

make_circles_button = tk.Button(buttons, text="Start", command=solve_all)
make_circles_button.pack(side=tk.RIGHT, padx=20, pady=20)

make_circles_button = tk.Button(buttons, text="1963", command=solve_placement_1963)
make_circles_button.pack(side=tk.RIGHT, padx=20, pady=20)

make_circles_button = tk.Button(buttons, text="2005", command=solve_placement_2005)
make_circles_button.pack(side=tk.RIGHT, padx=20, pady=20)

make_circles_button = tk.Button(buttons, text="2011", command=solve_placement_2011)
make_circles_button.pack(side=tk.RIGHT, padx=20, pady=20)

root.mainloop()
