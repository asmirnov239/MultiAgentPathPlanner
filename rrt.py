from init import *



class Robot:
  def __init__(self, location, goal, radius):
    global max_velocity
    global max_acceleration
    global growth_factor
    global chance_expand_goal
    self.root = TreeNode(location, 0.0, Vector(0,0), Vector(0,0))
    self.location = location
    self.rrt = RRT(self.root, growth_factor, chance_expand_goal, goal)
    self.goal = goal
    self.radius = radius
    self.finished = False
    self.goal_node = None
    self.index = index
    
    
    
class RRT:
  def __init__(self, root, goal):
    global max_velocity
    global max_acceleration
    global growth_factor
    global chance_expand_goal
    self.root = root
    self.goal = goal
    self.leaves = []
  def add_new_node(self, map):
    #returns new node sampled from the map
    while(True):
      if(random.uniform(0.0, 1.0) >= self.chance_expand_goal):
        new_node = map.sample_node()
      else: 
        new_node = TreeNode(self.goal, 0.0, None, None)
      closest_node = self.find_closest_node(new_node, self.root)
      if(Segment(new_node.point, closest_node.point).length>self.growth_factor):
        new_node = TreeNode(Point(int(closest_node.point.x+(new_node.point.x-closest_node.point.x)*(self.growth_factor/Segment(new_node.point, closest_node.point).length)), int(closest_node.point.y+(new_node.point.y-closest_node.point.y)*(self.growth_factor/Segment(new_node.point, closest_node.point).length))), 0.0, None, None)
      if not (self.check_obstacle_intersections(Segment(new_node.point, closest_node.point), map)):  
        distance = Segment(new_node.point, closest_node.point).length
        delta_t = self.sample_time(distance)
        new_node.time = closest_node.time + delta_t
        new_node.velocity = Vector((new_node.point.x-closest_node.point.x)/delta_t, (new_node.point.y-closest_node.point.y)/delta_t)
        print closest_node.velocity.x, closest_node.velocity.y
        print new_node.velocity.x, new_node.velocity.y
        average_acceleration = (new_node.velocity.subtract(closest_node.velocity))
        average_acceleration.divide(delta_t)
        if (average_acceleration.length() <= max_acceleration):
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
      return random.uniform(distance/max_velocity, 5*distance/max_velocity)
      
      
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