import common
image1 = []

def get_move(view, network):
  global image1
  (move, eat) = common.get_move(view, network)
  # image1 = image
  return (move, eat)