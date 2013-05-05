
class loc:
  def __init__(self, x, y):
    self.x = x
    self.y = y
  def __str__(self):
    return '('+str(self.x)+','+str(self.y)+')'

def main():
  locs = []
  for i in range(-25,25):
    for j in range(-25,25):
      locs.append((i,j))
      
  fo = open('alisa_test_locations.txt', 'w')
  #print locs[0]
  for i in locs:
    fo.write(str(i))
    fo.write(', ')
  
main()