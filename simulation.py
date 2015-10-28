from init import *

class Simulation:
  def __init__(self, map):
    global growth_factor
    global chance_expand_goal
    global lockQueue
    global lockMap
    global lockSim
    global simFinished
    global mapRandom
    global runSim
    global nodeQueue
    self.map = map 
    
  def run_simulation(self):
    while(True):
      while(True):
        lockSim.acquire()
        if(runSim == True):
          lockSim.release()
          break
        else:
          lockSim.release()
          time.sleep(0.05)
      for robot in self.map.robots:
        if(robot.finished==True):
          print "simulation is finished!"
          lockSim.acquire()
          simFinished = True
          lockSim.release()
      node = sample_new_node()
      lockQueue.acquire()
      nodeQueue.put(node)
      lockQueue.release()
      
  def sample_new_point(self):
    new_node = self.map.robots[0].rrt.add_new_node(self.map)
    if (new_node.point.x != self.map.robots[0].goal.x) or (new_node.point.y != self.map.robots[0].goal.y):
      self.canvas.pack()
      return new_node
    self.map.robots[0].goal_node = new_node
    self.map.robots[0].finished = True
