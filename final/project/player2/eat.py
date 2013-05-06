import game_interface
from history import History
import nn

poisonous_prior = 0.146
epsilon = 0.2

def shouldEatOrNot(view, history, prior):
  exist = True
  get_image = False
  test_result = False

  plant_info = view.GetPlantInfo()

  eat = False
  if plant_info == game_interface.STATUS_NO_PLANT:
    exist = False
  elif plant_info == game_interface.STATUS_UNKNOWN_PLANT:
    get_image = getImageOrNot(history, prior)
    if get_image:
      image = view.GetImage()
      eat = nn.is_nutritious(image)

  #eat = True # to deleted

  history.appendPlantInfo(exist, get_image, test_result, eat)

  return eat

def getImageOrNot(history, prior):
  """
  Test the plant if the prob(nutritious)/prob(poisonous) is above a pre-determined threshold
  """
  current_cell = history.getPositions()[-1]
  nutritious_prior = prior[current_cell]
  if nutritious_prior/(nutritious_prior+poisonous_prior) >= epsilon: return True
  return False


  """
  #if plant_info == game_interface.STATUS_NUTRITIOUS_PLANT:
    #print '.............HELLO! N'
    #eat = True
  #elif plant_info == game_interface.STATUS_POISONOUS_PLANT:
    #print '.............HELLO! P'
    #eat = False 
  """

