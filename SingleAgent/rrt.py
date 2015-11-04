import init
import map
import math
import random
from sympy.geometry import *

class RRT:
  def __init__(self, root, goal):
    self.root = root
    self.goal = goal
    self.leaves = []
  def add_new_node(self, map):
    #returns new node sampled from the map
    while(True):
      if(random.uniform(0.0, 1.0) >= init.chance_expand_goal):
        new_node = map.sample_node()
      else: 
        new_node = TreeNode(self.goal, 0.0, None, None)
      closest_node = self.find_closest_node(new_node, self.root)
      if(Segment(new_node.point, closest_node.point).length>init.growth_factor):
        new_node = TreeNode(Point(int(closest_node.point.x+(new_node.point.x-closest_node.point.x)*(init.growth_factor/Segment(new_node.point, closest_node.point).length)), int(closest_node.point.y+(new_node.point.y-closest_node.point.y)*(init.growth_factor/Segment(new_node.point, closest_node.point).length))), 0.0, None, None)
      if not (self.check_obstacle_intersections(Segment(new_node.point, closest_node.point), map)):  
        distance = Segment(new_node.point, closest_node.point).length
        delta_t = self.sample_time(distance)
        new_node.time = closest_node.time + delta_t
        new_node.velocity = Vector((new_node.point.x-closest_node.point.x)/delta_t, (new_node.point.y-closest_node.point.y)/delta_t)
        print closest_node.velocity.x, closest_node.velocity.y
        print new_node.velocity.x, new_node.velocity.y
        average_acceleration = (new_node.velocity.subtract(closest_node.velocity))
        average_acceleration.divide(delta_t)
        print average_acceleration.x, average_acceleration.y
        print "/n"
        if (average_acceleration.length() <= init.max_acceleration):
          new_node.acceleration = average_acceleration
          closest_node.add_child(new_node)
          new_node.parent = closest_node
          return new_node


  def find_closest_node(self, node, current_node):
    if not current_node.children:
      return current_node
    else:
      node_list = [current_node]
      for child_node in current_node.children:
        node_list.append(self.find_closest_node(node,child_node))
      node_list = sorted(node_list, key = lambda new_node: (node.point.x-new_node.point.x)**2+(node.point.y-new_node.point.y)**2)
      return node_list[0]

  def sample_time(self, distance):
      #return random.uniform(distance/init.max_velocity, 5*distance/init.max_velocity)
      return init.time_step
      
  def extend(self,closest_node, new_node):
    #check that the distance is less than growth factor
    pass
  def check_obstacle_intersections(self, segment, map):
    for obstacle in map.obstacles:
      if(intersection(Polygon(*obstacle.get_vertices()), segment)):
        return True
    return False

  def traverse_tree_path(self, node):
    path = []
    while(node.parent != None):
      path.insert(0,(node.point.x, node.point.y, node.time, node.velocity, node.acceleration))
      node = node.parent
    path.insert(0,(node.point.x, node.point.y, node.time, node.velocity, node.acceleration))
    return path

  def get_all_leaves(self,leaves, node):
    if(node.children):
      for child in node.children:
        self.get_all_leaves(leaves, child)
    else:
      self.leaves.append(node)
      return


class Robot:
  def __init__(self, location, goal, index):
    self.root = TreeNode(location, 0.0, Vector(0,0), Vector(0,0))
    self.location = location
    self.rrt = RRT(self.root, goal)
    self.goal = goal
    self.radius = init.robot_radius
    self.finished = False
    self.goal_node = None
    self.index = index
    
class TreeNode:
  def __init__(self, point, time, velocity, acceleration):
    self.children = []
    self.point  = point
    self.time = time
    self.velocity = velocity
    self.acceleration = acceleration
    self.parent = None
  def add_child(self, tree_node):
    self.children.append(tree_node)
  def __str__(self):
    return self.point, self.time,  self.velocity, self.acceleration


class Vector:
  def __init__(self, x,y):
    self.x = float(x)
    self.y = float(y)
  def add(self, vec):
    return Vector(self.x+vec.x, self.y+vec.y)
  def subtract(self, vec):
    return Vector(self.x-vec.x, self.y-vec.y)
  def length(self):
    return math.sqrt(self.x**2+self.y**2)
  def divide(self, d):
    self.x = self.x/d
    self.y = self.y/d
