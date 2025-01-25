import pandas as pd
from shapely.geometry import Polygon, Point
from pulp import LpProblem, LpMinimize, LpMaximize, LpVariable, lpSum, PULP_CBC_CMD
import matplotlib.pyplot as plt
import numpy as np

def load_city_boundary(file):
    df = pd.read_csv(file)
    coordinates = list(zip(df['Longitude'], df['Latitude']))
    return Polygon(coordinates)

def generate_grid(city, spacing_km):
    grid_spacing = spacing_km / 111.0
    min_x, min_y, max_x, max_y = city.bounds

    x_grid_points = np.arange(min_x, max_x + grid_spacing, grid_spacing)
    y_grid_points = np.arange(min_y, max_y + grid_spacing, grid_spacing)

    grid_x, grid_y = np.meshgrid(x_grid_points, y_grid_points)
    all_points = np.c_[grid_x.ravel(), grid_y.ravel()]
    return [Point(x, y) for x, y in all_points if city.contains(Point(x, y))]

def solve_fire_hall_placement(candidate_locations, points_to_cover, coverage_radius, fixed_halls=None):
    coverage = {}

    for i, fire_hall in enumerate(candidate_locations):
        coverage[i] = []
        for j, point in enumerate(points_to_cover):
            if fire_hall.distance(point) <= coverage_radius:
                coverage[i].append(j)

    problem = LpProblem("FireHallPlacement", LpMinimize)
    x = LpVariable.dicts("FireHall", range(len(candidate_locations)), 0, 1, cat="Binary")
    
    problem += lpSum(x[i] for i in range(len(candidate_locations)))
    
    for j in range(len(points_to_cover)):
        problem += lpSum(x[i] for i in range(len(candidate_locations)) if j in coverage[i]) >= 1

    if fixed_halls:
        for idx in fixed_halls:
            if idx < len(candidate_locations):
                problem += x[idx] == 1

    problem.solve(PULP_CBC_CMD(threads=1, cuts='on', strong=3, presolve='on', msg=True))

    return [candidate_locations[i] for i in range(len(candidate_locations)) if x[i].value() == 1]