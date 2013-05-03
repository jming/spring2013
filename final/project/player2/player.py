import common
image2 = []

def get_move(view):
  global image2
  (move, eat, image) = common.get_move(view)
  image2 = image
  return (move, eat)

# def get_image(image):
# 	return image