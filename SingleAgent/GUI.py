import init
import Tkinter
import Queue
from sympy.geometry import *
import map
import rrt 

class GUI:
  def __init__(self, ratio, map):
    self.draw_ratio = ratio
    self.map = map
    print self.map
    map = None
    self.top = Tkinter.Tk()
    self.toolbar = Tkinter.Frame(self.top, bg="grey")
    self.canvas = Tkinter.Canvas(self.top, bg="white", height=self.apply_ratio(init.map_height), width=self.apply_ratio(init.map_width))
    self.miniToolBar = Tkinter.Frame(self.toolbar, bg="grey")
    self.miniToolBar.pack(side=Tkinter.RIGHT)

    #widgets and variables for drawing new map
    self.map_toolbar = Tkinter.Frame(self.top, bg="grey")
    self.drawingDoneButton = Tkinter.Button(self.map_toolbar, text="Done", command=self.construct_drawn_map)
    self.drawingDoneButton.pack(side=Tkinter.LEFT, padx=2, pady=2)
    #variables for drawing maps
    self.drawObstacle = Tkinter.Button(self.map_toolbar, text="Add Obstacles", command=self.add_obstacle)
    self.drawObstacle.pack(side=Tkinter.LEFT, padx=2, pady=2)
    self.originObstacleX = None
    self.originObstacleY = None 
    self.current_drawn_obstacle = None
    self.drawn_obstacles = []
    #variables for drawing robots
    self.drawObstacle = Tkinter.Button(self.map_toolbar, text="Add Robot/Goal", command=self.add_robot)
    self.drawObstacle.pack(side=Tkinter.LEFT, padx=2, pady=2)
    self.drawn_robots = []
    self.current_drawn_robot = None


    #Buttons
    self.simulateButton = Tkinter.Button(self.toolbar, text="Simulate", command=self.simulate)
    self.simulateButton.pack(side=Tkinter.LEFT, padx=2, pady=2)
    self.restartMap = Tkinter.Button(self.toolbar, text="Restart", command=self.restart)
    self.restartMap.pack(side=Tkinter.LEFT, padx=2, pady=2)
    self.drawMapButton = Tkinter.Button(self.toolbar, text="Draw Map", command=self.draw_new_map)
    self.drawMapButton.pack(side=Tkinter.LEFT, padx=2, pady=2)
    self.updateParamsButton = Tkinter.Button(self.miniToolBar, text="Update", command=self.update_params)
    

    #default values
    v = Tkinter.StringVar()
    v.set(str(init.growth_factor))
    s = Tkinter.StringVar()
    s.set(str(init.chance_expand_goal))
    
    #Labels and Entries
    self.growthRate = Tkinter.Label(self.miniToolBar, text="Growth Rate:", bg="grey", fg="Blue", font = 20)
    self.growthRate.grid(row=0)
    self.Percentage = Tkinter.Label(self.miniToolBar, text="Percentage:",  bg="grey", fg="Blue", font = 20)
    self.Percentage.grid(row=1)

    self.growthEntry = Tkinter.Entry(self.miniToolBar, textvariable=v)
    self.growthEntry.grid(row=0, column=1)
    self.PercentageEntry = Tkinter.Entry(self.miniToolBar, textvariable=s)
    self.PercentageEntry.grid(row=1, column = 1)
    self.updateParamsButton.grid(row=2, column = 1)
    
    self.canvas.pack(side=Tkinter.BOTTOM)
    self.toolbar.pack(side=Tkinter.TOP, fill=Tkinter.X)
    self.top.mainloop()

  def update_params(self):
    init.growth_factor = int(self.growthEntry.get())
    init.chance_expand_goal = float(self.PercentageEntry.get())
    
  def apply_ratio(self, x):
    return int(x/self.draw_ratio)

  def construct_drawn_map(self):
    self.map.set_obstacles(self.drawn_obstacles)
    self.map.set_robots(self.drawn_robots)
    init.mapRandom = False
    self.drawn_obstacles = []
    self.drawn_robots = []
    self.map_toolbar.pack_forget()
    self.canvas.unbind("<Button-1>")
    self.canvas.unbind("<B1-Motion>")
    self.canvas.unbind("<ButtonRelease-1>")

  def draw_new_map(self):
    print "Reached draw_map function"
    self.map_toolbar.pack(side=Tkinter.BOTTOM, fill=Tkinter.X)
    #self.map_toolbar.pack_forget()


  def add_obstacle(self):
    self.canvas.bind("<Button-1>", self.set_obstacle_origin)
    self.canvas.bind("<B1-Motion>", self.draw_obstacle)
    self.canvas.bind("<ButtonRelease-1>", self.set_obstacle)

  def set_obstacle_origin(self, event):
    self.originObstacleX = event.x
    self.originObstacleY = event.y

  def draw_obstacle(self, event):
    self.canvas.delete(self.current_drawn_obstacle)
    self.current_drawn_obstacle = self.canvas.create_rectangle(self.originObstacleX, self.originObstacleY,  event.x, event.y, outline="#fb0")
    self.canvas.pack()
    
  def set_obstacle(self, event):
    obst = self.canvas.create_rectangle(self.originObstacleX, self.originObstacleY,  event.x, event.y, outline="#fb0")
    self.drawn_obstacles.append(map.Obstacle(Point(self.originObstacleX*init.drawing_ratio, self.originObstacleY*init.drawing_ratio),  Point(event.x*init.drawing_ratio, event.y*init.drawing_ratio))) 
    self.canvas.pack()
  
  def add_robot(self):
    #unbind mouse dragging events in case they were already set by map drawing
    self.canvas.unbind("<B1-Motion>")
    self.canvas.unbind("<ButtonRelease-1>")
    self.canvas.bind("<Button-1>", self.set_robot_location)
  
  def set_robot_location(self,event):
    self.canvas.unbind("<Button-1>")
    self.current_drawn_robot = rrt.Robot(Point(event.x*init.drawing_ratio, event.y*init.drawing_ratio), Point(-50,-50), len(self.drawn_robots))
    self.canvas.bind("<Button-1>", self.set_goal_location)

  def set_goal_location(self, event):
    self.canvas.unbind("<Button-1>")
    new_robot = rrt.Robot(self.current_drawn_robot.location, Point(event.x*init.drawing_ratio,event.y*init.drawing_ratio), self.current_drawn_robot.index)
    self.drawn_robots.append(new_robot)
    self.draw_robot(new_robot)
    self.canvas.bind("<Button-1>", self.set_robot_location)

  def restart(self):
    #clears and resets all the resources
    init.lockSim.acquire()
    init.runSim = False
    init.simFinished = True
    self.canvas.delete("all")
    init.lockMap.acquire()
    self.map.restart_map()
    init.lockMap.release()
    init.lockQueue.acquire()
    init.nodeQueue.queue.clear()
    init.lockQueue.release()
    init.lockSim.release()
    print "Restart is done"


  def simulate(self):
    init.lockSim.acquire()
    init.runSim = True
    init.simFinished = False
    if(init.mapRandom == True):
      self.map.generate_random_map()
    self.draw_map()
    init.mapRandom = True
    self.top.after(30, self.draw_new_nodes)
    init.lockSim.release()
    

  def draw_node(self, new_node):
    line = self.canvas.create_line(self.apply_ratio(new_node.point.x), self.apply_ratio(new_node.point.y), self.apply_ratio(new_node.parent.point.x), self.apply_ratio(new_node.parent.point.y))
    self.canvas.pack()

  def draw_new_nodes(self):
    init.lockSim.acquire()
    if(init.runSim == True):
      init.lockQueue.acquire()
      while not init.nodeQueue.empty():
        new_node = init.nodeQueue.get()
        init.nodeQueue.task_done()
        self.draw_node(new_node)
      init.lockQueue.release()
    if(init.simFinished == True and not init.nodeQueue.empty()):
      goalNode = init.goalNode
      self.draw_path(goalNode)
      init.lockSim.release()
      self.top.after(30, self.draw_new_nodes)
      return
    init.lockSim.release()
    self.top.after(30, self.draw_new_nodes)

  def draw_map(self):
    for robot in self.map.robots:
      self.draw_robot(robot)
    for obs in self.map.obstacles:
      print obs.p1.x, obs.p1.y, obs.p2.x, obs.p2.y
      self.canvas.create_rectangle(self.apply_ratio(obs.p1.x), self.apply_ratio(obs.p1.y),  self.apply_ratio(obs.p2.x), self.apply_ratio(obs.p2.y), outline="#fb0")
      self.canvas.pack()
  
  def draw_robot(self, robot):
    self.canvas.create_oval(self.apply_ratio(robot.location.x-robot.radius), self.apply_ratio(robot.location.y-robot.radius), self.apply_ratio(robot.location.x+robot.radius), self.apply_ratio(robot.location.y+robot.radius))
    canvas_id = self.canvas.create_text(self.apply_ratio(robot.location.x), self.apply_ratio(robot.location.y), anchor="n")
    self.canvas.itemconfig(canvas_id, text=("Robot "+str(robot.index)))
    self.canvas.insert(canvas_id, 12, "")
    
    canvas_id = self.canvas.create_text(self.apply_ratio(robot.goal.x), self.apply_ratio(robot.goal.y), anchor="n")
    self.canvas.itemconfig(canvas_id, text=("Goal "+str(robot.index)))
    self.canvas.insert(canvas_id, 12, "")

  def draw_rrt(self,current_node):
    if not current_node.children:
      return
    else:
      for child_node in current_node.children:
        line = self.canvas.create_line(self.apply_ratio(current_node.point.x), self.apply_ratio(current_node.point.y), self.apply_ratio(child_node.point.x), self.apply_ratio(child_node.point.y))
        self.canvas.pack()
        self.draw_rrt(child_node)

  def draw_path(self, path_node):
    while not (path_node.parent==None):
      line = self.canvas.create_line(self.apply_ratio(path_node.point.x), self.apply_ratio(path_node.point.y), self.apply_ratio(path_node.parent.point.x), self.apply_ratio(path_node.parent.point.y), fill="red", width=4.0)
      self.canvas.pack()
      path_node = path_node.parent
    
  def draw(self):
    self.top.after(0, self.draw_new_nodes) 
    self.top.mainloop()
