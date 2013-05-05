
class Image:
  def __init__(self, label):
    self.pixels = []
    self.label = label

class DataReader:
  @staticmethod
  def GetImages(filename, limit):
    """Returns a list of image objects
    filename: The file to read in
    limit: The maximum number of images to read.  -1 = no limit
    """
    images = []
    infile = open(filename, 'r')
    ct = 0
    cur_row = 0
    image = None
    while True:
      line = infile.readline().strip()
      #print line, 'LINE'
      if not line:
        line = infile.readline().strip()
      if line.find('END') == 0:
        #print 'BREAK'
        break
      if image:
        images.append(image)
        ct += 1
        if ct > limit and limit != -1:
          break
      if(filename.find('nutritious')==0):
        image = Image(1)
      else:
        image = Image(0)
      temp =  [int(r) for r in line.strip().split(', ')]
      for i in range(6):
        image.pixels.append(temp[i*6:i*6 + 6])
      #print image.pixels
    if image:
      images.append(image)
    #print len(images)
    numavg = 5
    # This is assuming all of the images with the same label are next to each other
    images_avg = [Image(0) if image.label == 0 else Image(1) for image in images[0::numavg]]
    print len(images_avg), len(images)
    for image in images_avg:
      image.pixels = [[0. for i in range(len(images[0].pixels))] for j in range(len(images[0].pixels[0]))]
    for im in range(len(images)):
      for i in range(len(images[im].pixels)):
        for j in range(len(images[im].pixels[i])):
          # print images_avg[im/numavg].pixels[i], images[im].pixels[i], float(numavg) 
          images_avg[im / numavg].pixels[i][j] += images[im].pixels[i][j] / float(numavg)
    return images_avg 
    
    '''while True:
      line = infile.readline().strip()
      if not line:
        break
      if line.find('#') == 0:
        if image:
          images.append(image)
          ct += 1
          if ct > limit and limit != -1:
            break
        image = Image(int(line[1:]))
      else:
        image.pixels.append([int(r) for r in line.strip().split(', ')])
    if image:
      images.append(image)
    return images'''

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
