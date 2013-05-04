import common
image2 = []

def get_move(view, network):
  global image2
  (move, eat) = common.get_move(view, network)
  # image2 = image
  return (move, eat)

# def get_image(image):
# 	return image