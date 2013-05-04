import game_interface
import random
import time
from neural_net import *
from neural_net_impl import *
from data_reader import *

# def get_move(view):
#   # Check if there is a plant in this location
#   hasPlant = view.GetPlantInfo() == game_interface.STATUS_UNKNOWN_PLANT
#   # if there is a plant,
#   if hasPlant:
#       # take five observations
#     for i in xrange(5):
#       # print these observations
#       print view.GetImage()
#   # wait a few seconds
#   time.sleep(0.1)
#   # return a random direction and whether to eat it
#   return (random.randint(0, 4), hasPlant)

# def get_move(view):

#   eat = 0

#   # 0. Land in square, check if there is a plant
#   hasPlant = view.GetPlantInfo() == game_interface.STATUS_UNKNOWN_PLANT

#   # If there is a plant,
#   if hasPlant:

#     # 1. Decide if observe/how many times
#     numobs = 5

#     # 2. Classify plant that many number of times
#     ispoisonous = 0
#     for i in xrange(numobs):
#       ispoisonous += classify(view.GetImage())

#     eat = ispoisonous / numobs > 0.5

#   # 3. Decide where to go
#   move = random.randint(0, 4)

#   # 4. Execute move
#   return (move, eat)


def classify(image):

    # run this classification through the neural network
    classification = neural_net_apply(image)
    # return the classification
    return classification

def get_move(view, network):

  images = []
  hasPlant = view.GetPlantInfo() == game_interface.STATUS_UNKNOWN_PLANT
  if hasPlant:
    for i in xrange(10):
      inew = Image(0)
      pix = view.GetImage()
      pix = list(pix)
      for i in range(6):
        inew.pixels.append(pix[i*6:i*6+6])
      # inew.pixels.append(view.GetImage())
      # print inew.pixels
      images.append(inew)
  time.sleep(0.1)
  k = 0.0
  for i in images:
    k += network.Classify(i)
  eat = k / 10.
  print eat
  return (random.randint(0,4), eat > 0.5)
# >>>>>>> 446141c5898c4c1aeb4195040a38993760036bd0

#     hasPlant = view.GetPlantInfo() == game_interface.STATUS_UNKNOWN_PLANT
#     if hasPlant:
#         for i in xrange(10):
#             images.append(view.GetImage())
#     time.sleep(0.1)
#     return (random.randint(0, 4), hasPlant, images)
