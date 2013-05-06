
def main():
    weights = []
    fo = open('weights.txt','r')
    while True:
        line = fo.readline()
        if not line:
            break
        weights.append(float(line))
    
    f1 = open('weights_array.txt', 'w')
    f1.write(str(weights))
    
main()

