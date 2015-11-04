import init
import time
import Queue

class Simulation:
  def __init__(self, map):
    self.map = map
    print self.map

  def run_simulation(self):
    while(True):
      while(True):
        init.lockSim.acquire()
        if(init.runSim == True and init.simFinished == False):
          init.lockSim.release()
          print "simulation is running now"
          break
        else:
          init.lockSim.release()
          print "simulation is sleeping"
          time.sleep(1.5)
      init.lockMap.acquire()
      node = self.sample_new_node()
      for robot in self.map.robots:
        if(robot.finished==True):
          print "simulation is finished!"
          init.lockSim.acquire()
          init.goalNode = node
          init.simFinished = True
          init.runSim = False
          init.lockSim.release()
      init.lockMap.release()
      init.lockQueue.acquire()
      init.nodeQueue.put(node)
      init.lockQueue.release()

  def sample_new_node(self):
    new_node = self.map.robots[0].rrt.add_new_node(self.map)
    if (new_node.point.x != self.map.robots[0].goal.x) or (new_node.point.y != self.map.robots[0].goal.y):
      return new_node
    self.map.robots[0].goal_node = new_node
    self.map.robots[0].finished = True
    return new_node
