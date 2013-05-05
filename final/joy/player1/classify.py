from sklearn import svm
from sklearn import cross_validation

svc = svm.SVC(kernel='rbf')


def get_data():
    imagesn = []
    imagesp = []
    for f in ["nutritious.txt", "poisnous.txt"]:
        infile = open(f, 'r')
        image = []
        ct = 0
        while ct < 1000:
            line = infile.readline().strip()
            if not line:
                line = infile.readline().strip()
            if line.find('END') == 0:
                break
            if f.find('nutritious') == 0:
                image = imagesn
            else:
                image = imagesp
            temp = [int(r) for r in line.strip().split(', ')]
            image.append(temp)
            ct += 1
    features = imagesn + imagesp
    labels = [1 for i in range(len(imagesn))] + [0 for j in range(len(imagesp))]
    print (features, labels)


def avg_data():
    numavg = 5
    (features, labels) = get_data()
    features_res = [[0. for i in range(len(features[0]))] for j in range(len(features)/numavg)]
    labels_res = labels[0::numavg]
    for feat in range(len(features)):
        for f in range(len(features[feat])):
            features_res[feat/numavg][f] += features[feat][f] / float(numavg)
    return (features_res, labels_res)


def build_svm():
    global svc
    (features, labels) = avg_data()
    return svc.fit(features, labels)


def test_svm():
    global svc
    (features, labels) = avg_data()
    return cross_validation.cross_val_score(svc, features, labels, cv=5)
