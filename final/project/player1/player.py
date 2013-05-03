import common
image1 = []

def get_move(view):
  global image1
  (move, eat, image) = common.get_move(view)
  image1 = image
  return (move, eat)