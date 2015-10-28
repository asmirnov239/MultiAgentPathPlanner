from init import *
import GUI
import simulation


if __name__ == '__main__':
  map_ = Map()

  
  simulation = simulation.Simulation(map_)
  simThread = threading.Thread(target = simulation.run_simulation, args = ())
  simThread.start()

  gui = GUI.GUI(drawing_ratio, map_)
  gui.draw()