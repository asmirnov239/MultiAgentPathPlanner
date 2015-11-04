import init
import GUI
import map
import simulation
import threading

if __name__ == '__main__':
  map_ = map.Map()

  simulation = simulation.Simulation(map_)
  simThread = threading.Thread(target = simulation.run_simulation, args = ())
  simThread.start()

  gui = GUI.GUI(init.drawing_ratio, map_)
  gui.draw()
