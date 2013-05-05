import game_interface
import random
import time

def get_move(view):
  # Check if there is a plant in this location
  hasPlant = view.GetPlantInfo() == game_interface.STATUS_UNKNOWN_PLANT
  # if there is a plant,
  if hasPlant:
      # take five observations
    for i in xrange(5):
      # print these observations
      view.GetImage()
  # wait a few seconds
  time.sleep(0.1)
  # return a random direction and whether to eat it
  return (random.randint(0, 4), hasPlant)