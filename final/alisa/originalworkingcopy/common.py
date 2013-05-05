import game_interface
import random
import alllocs
import time

locs = alllocs.all()

def get_move(view):
  # Choose a random direction.
  # If there is a plant in this location, then try and eat it.
  hasPlant = view.GetPlantInfo() == game_interface.STATUS_UNKNOWN_PLANT
  # Choose a random direction
  if hasPlant:
    for i in xrange(5):
      print view.GetImage()
  time.sleep(0.1)
  dir = random.randint(0,4)
  if view.GetXPos() > 50:
    dir = game_interface.LEFT
  elif view.GetXPos() < -50:
    dir = game_interface.RIGHT
  if view.GetYPos() > 50:
    dir = game_interface.DOWN
  elif view.GetYPos() <-50:
    dir = game_interface.UP 
  return (dir, hasPlant)
  #return (random.randint(0, 4), hasPlant)
