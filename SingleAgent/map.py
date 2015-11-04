import init
from sympy.geometry import *
import rrt
import random

class Map:
  def __init__(self):
    self.obstacles = []
    self.robots = []

  def generate_random_map(self):
    self.generate_random_obstacles(init.number_of_obstacles)
    self.generate_robots(init.number_of_robots)
    
  def generate_random_obstacles(self, num):
    while(num>0):
      flag = False
      point1 = Point(random.randint(0,init.map_width-1000),random.randint(0,init.map_height-1000))
      w = random.randint(1000, 2000)
      h = random.randint(1000, 2000)

      new_obstacle = Obstacle(point1, Point(point1.x+w, point1.y+h))
      for obstacle in self.obstacles:
        print "inspecting new obstacle"
        if (new_obstacle.check_obstacle_collision(obstacle)):
          flag = True
          break
      if not flag:
        self.obstacles.append(new_obstacle)
        num -= 1
        print "added obstacle"
    
  def generate_robots(self, num):
    global robot_radius
    while(num > 0):
      flag = False
      location = Point(random.randint(100,init.map_width),random.randint(100,init.map_height))
      goal = Point(random.randint(100,init.map_width),random.randint(100,init.map_height))
      for obstacle in self.obstacles:
        if(obstacle.get_polygon().encloses_point(location)) or (obstacle.get_polygon().encloses_point(goal)):
          flag = True
          break
      if not flag:
        self.robots.append(rrt.Robot(location, goal, num))
        num -= 1
        print "added obstacle"

  def sample_node(self):
    point = Point(random.randint(0,init.map_width),random.randint(0,init.map_height))
    node = rrt.TreeNode(point, 0.0, None, None)
    return node

  def restart_map(self):
    self.obstacles = []
    self.robots = []

  def set_obstacles(self, obstacles):
    self.obstacles = obstacles

  def set_robots(self, robots):
    self.robots = robots

    

    
class Obstacle:
  def __init__(self, p1, p2):
    self.p1 = p1
    self.p2 = p2
  
  def get_polygon(self):
    return Polygon(*self.get_vertices())
    
  def get_line_segments(self):
    return [Segment(self.p1,Point(self.p2.x,self.p1.y)), Segment(Point(self.p2.x,self.p1.y),self.p2), Segment(self.p2, Point(self.p1.x,self.p2.y)), Segment(Point(self.p1.x,self.p2.y),self.p1)]

  def get_vertices(self):
    return [self.p1, Point(self.p2.x,self.p1.y), self.p2, Point(self.p1.x,self.p2.y)]

  def check_obstacle_collision(self, obstacle):
    if(Polygon(*self.get_vertices()).encloses_point(obstacle.p1) or Polygon(*obstacle.get_vertices()).encloses_point(self.p1)):
      return True 
    for lineSeg in self.get_line_segments():
      for lineSeg2 in obstacle.get_line_segments():
        if (lineSeg.intersection(lineSeg2)):
          return True
    return False

  def obstacle_line_intersection(self, p1, p2):
    #checks if line between p1 and p2 is blocked by an obstacle
    pass



