import math
import time
import random
import Tkinter
import time
from sympy.geometry import *
import Queue
import threading
import sys
sys.path.append("/home/vagrant/Desktop/shared_files/Research/RRT")

import matplotlib as mpl
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import colorConverter

######################
###Global Variables###
######################
global map_width, map_height, robot_radius, number_of_obstacles, number_of_robots, max_velocity, max_acceleration, drawing_ratio, growth_factor, chance_expand_goal, time_step
map_width = 10000 
map_height = 10000
robot_radius = 180
number_of_obstacles = 6
number_of_robots = 1
max_velocity = 200
max_acceleration = 50000
drawing_ratio = 20

growth_factor = 500
chance_expand_goal = 0.2
time_step = random.uniform(growth_factor/max_velocity, 5*growth_factor/max_velocity)
######################
######################
######################
global nodeQueue, rejectedNodeQueue, lockQueue, lockMap, lockSim, mapRandom, runSim, simFinished
nodeQueue = Queue.Queue()
rejectedNodeQueue = Queue.Queue()
lockQueue = threading.Lock()
lockMap = threading.Lock()
lockSim = threading.Lock()
goalNode = None
mapRandom = True
runSim = False
simFinished = True
