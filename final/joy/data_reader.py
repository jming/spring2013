
class Image:
  def __init__(self, label):
    self.pixels = []
    self.label = label

class DataReader:
  @staticmethod
  def GetImages(filename, limit, avg=True):
    """Returns a list of image objects
    filename: The file to read in
    limit: The maximum number of images to read.  -1 = no limit
    """
    # images = []
    # infile = open(filename, 'r')
    # ct = 0
    # cur_row = 0
    # image = None
    # while True:
    #   line = infile.readline().strip()
    #   if not line:
    #     break
    #   if line.find('#') == 0:
    #     if image:
    #       images.append(image)
    #       ct += 1
    #       if ct > limit and limit != -1:
    #         break
    #     image = Image(int(line[1:]))
    #   else:
    #     image.pixels.append([float(r) for r in line.strip().split()])
    # if image:
    #   images.append(image)
    # return images

    # basic images function
    images = []
    infile = open(filename, 'r')
    image = None
    ct = 0
    while True:
      line = infile.readline().strip()
      if not line:
        line = infile.readline().strip()
      if line.find('END') == 0:
        break
      if image:
        images.append(image)
        ct += 1
        if ct > limit and limit != -1:
          break
      image = Image(1) if filename.find('nutritious')==0 else Image(0)
      temp = [int(r) for r in line.strip().split(', ')]
      for i in range(6):
        image.pixels.append(temp[i*6:(i+1)*6])
    if image:
      images.append(image)

    # average
    if avg:
      num_avg = 5
      images_avg = [Image(1) if filename.find('nutritious')==0 else Image(0) for x in range(len(images)/num_avg + 1)]
      for image in images_avg:
        image.pixels = [[0. for i in range(len(images[0].pixels))] for j in range(len(images[0].pixels[0]))]
      # print len(images_avg), len(images_avg[0].pixels), len(images_avg[0].pixels[0])
      for image in range(len(images)):
        for im in range(len(images[image].pixels)):
          for i in range(len(images[image].pixels[i])):
            # print image, image/num_avg, im, i
            images_avg[image/num_avg].pixels[im][i] += images[image].pixels[im][i] / float(num_avg)
      return images_avg
    else:
      return images
    # for image in images_avg:
      # print image.pixels
    # return images
    # return images_avg

  @staticmethod
  def DumpWeights(weights, filename):
    """Dump the weights vector to filename"""
    outfile = open(filename, 'w')
    for weight in weights:
      outfile.write('%r\n' % weight)

  @staticmethod
  def ReadWeights(filename):
    """Returns a weight vector retrieved by reading file filename"""
    infile = open(filename, 'r')
    weights = []
    for line in infile:
      weight = float(line.strip())
      weights.append(weight)
