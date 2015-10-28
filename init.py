import math
import time
import random
import Tkinter
import time
from sympy.geometry import *
import Queue
import threading
from rrt import *
from map import *
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
map_width = 10000 
map_height = 10000
robot_radius = 180
number_of_obstacles = 6
number_of_robots = 1
max_velocity = 200
max_acceleration = 20
drawing_ratio = 20

growth_rate = 500
chance_expand_goal = 0.2
######################
######################
######################

nodeQueue = Queue.Queue()
rejectedNodeQueue = Queue.Queue()
lockQueue = threading.Lock()
lockMap = threading.Lock()
lockSim = threading.Lock()
mapRandom = True
runSim = False
simFinished = False