from init import *

class GUI:
  def __init__(self, ratio, map):
    global map_width
    global map_height
    global lockQueue
    global lockMap
    global lockSim
    global simFinished
    global mapRandom
    global runSim
    global nodeQueue
    global number_of_obstacles, number_of_robots
    self.nodeQueue = nodeQueue
    self.draw_ratio = ratio
    self.map = map
    map = None
    self.top = Tkinter.Tk()
    self.toolbar = Tkinter.Frame(self.top, bg="grey")
    self.canvas = Tkinter.Canvas(self.top, bg="white", height=self.apply_ratio(map_height), width=self.apply_ratio(map_width))
    self.miniToolBar = Tkinter.Frame(self.toolbar, bg="grey")
    self.miniToolBar.pack(side=Tkinter.RIGHT)
    
    #Buttons
    self.simulateButton = Tkinter.Button(self.toolbar, text="Simulate", command=self.simulate)
    self.simulateButton.pack(side=Tkinter.LEFT, padx=2, pady=2)
    self.restartMap = Tkinter.Button(self.toolbar, text="Restart", command=self.restart)
    self.restartMap.pack(side=Tkinter.LEFT, padx=2, pady=2)
    self.updateParamsButton = Tkinter.Button(self.miniToolBar, text="Update", command=self.update_params)
    
    #default values
    v = Tkinter.StringVar()
    v.set(str(growth_rate))
    s = Tkinter.StringVar()
    s.set(str(chance_expand_goal))
    
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
    
    self.canvas.pack(side=Tkinter.BOTTOM,)
    self.toolbar.pack(side=Tkinter.TOP, fill=Tkinter.X)
    self.top.mainloop()

  def update_params(self):
    self.growth_rate = int(self.growthEntry.get())
    self.chance_expand_goal = float(self.PercentageEntry.get())
    
  def apply_ratio(self, x):
    return int(x/self.draw_ratio)

  def restart(self):
    lockSim.acquire()
    time.sleep(0.5)
    self.canvas.delete("all")
    self.map = None
    runSim = False
    simFinished = False
    lockSim.release()

  def simulate(self):
    lockSim.acquire()
    runSim = True
    if(mapRandom == True):
      self.map.generate_random_map(number_of_obstacles, number_of_robots)
    self.draw_map()
    lockSim.release()

  def draw_node(self, new_node):
    line = self.canvas.create_line(self.apply_ratio(new_node.point.x), self.apply_ratio(new_node.point.y), self.apply_ratio(new_node.parent.point.x), self.apply_ratio(new_node.parent.point.y))
    self.canvas.pack()

  def draw_new_nodes(self):
    lockSim.acquire()
    if(runSim == True):
      lockQueue.acquire()
      while not nodeQueue.empty():
        new_node = nodeQueue.get()
        self.draw_node(new_node)
      lockQueue.release()
      self.top.after(10, self.draw_new_nodes)
    lockSim.release()

  def draw_map(self):
    for obs in self.map.obstacles:
      print obs.p1.x, obs.p1.y, obs.p2.x, obs.p2.y
      self.canvas.create_rectangle(self.apply_ratio(obs.p1.x), self.apply_ratio(obs.p1.y),  self.apply_ratio(obs.p2.x), self.apply_ratio(obs.p2.y), outline="#fb0")
      self.canvas.pack()
  
  def draw_robot(self, robot):
    self.canvas.create_oval(self.apply_ratio(robot.location.x-robot.radius), self.apply_ratio(robot.location.y-robot.radius), self.apply_ratio(robot.location.x+robot.radius), self.apply_ratio(robot.location.y+robot.radius))
    canvas_id = self.canvas.create_text(self.apply_ratio(robot.location.x), self.apply_ratio(robot.location.y), anchor="n")
    self.canvas.itemconfig(canvas_id, text="Robot 1")
    self.canvas.insert(canvas_id, 12, "")
    
    canvas_id = self.canvas.create_text(self.apply_ratio(robot.goal.x), self.apply_ratio(robot.goal.y), anchor="n")
    self.canvas.itemconfig(canvas_id, text="Goal 1")
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
    self.top.after(10, self.draw_new_nodes) 
    self.top.mainloop()