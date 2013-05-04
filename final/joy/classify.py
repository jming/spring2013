import numpy as np
import milk
import milk.supervised
import milk.supervised.svm
import milk.measures.nfoldcrossvalidation

model = milk.defaultclassifier

#############################################


# build the classifer based on training data
def get_data():
    imagesn = []
    imagesp = []
    for f in ["nutritious.txt", "poisnous.txt"]:
        # ct = 0
        infile = open(f, 'r')
        image = []
        ct = 0
        while ct < 1000:
            line = infile.readline().strip()
            if not line:
                line = infile.readline().strip()
            if line.find('END') == 0:
                break
            # if image:
            #     images.append(image)
            #     ct += 1
            if f.find('nutritious') == 0:
                image = imagesn
            else:
                image = imagesp
            temp = [int(r) for r in line.strip().split(', ')]
            # for i in range(6):
            #     image.append(temp[i*6:i*6+6])
            image.append(temp)
            ct += 1
        # if image:
        #     images.append(image)
        features = imagesn+imagesp
        labels = [1 for i in range(len(imagesn))] + [0 for j in range(len(imagesp))]

    return (features, labels)


def build_model(mode):
    global model
    (features, labels) = get_data()
    if mode == "default":
        learner = milk.defaultclassifier()
    elif mode == "tree":
        learner = milk.supervised.tree.tree_learner()
    elif mode == "svm":
        learner = milk.supervised.svm.svm_raw(kernel=np.dot, C=12)
    model = learner.train(features, labels)


# def build_default():
#     global model
#     # 2d array of features: 100 examples of 10 features each
#     (features, labels) = get_data()
#     # print images
#     # nlen = len(images[0])
#     # plen = len(images[1])

#     # images = images[0] + images[1]

#     # print images

#     # features = images
#     # labels = [1 for i in range(nlen)] + [0 for j in range(plen)]
#     # # why are they doing this??
#     # # features[50:] += .5
#     # # labels[50:] = 1
#     # print features
#     # print labels

#     # create and train learner
#     learner = milk.defaultclassifier()
#     model = learner.train(features, labels)

#     # return model
#     # example = np.random.rand(10)
#     # print model.apply(example)
#     # example2 = np.random.rand(10)
#     # example2 += .5
#     # print model.apply(example2)


# def build_tree():
#     global model
#     (features, labels) = get_data()
#     learner = milk.supervised.tree.tree_learner()
#     model = learner.train()


# def use_tree(example):
#     global model
#     return model.apply(example)


# def build_svm():
#     global model
#     (features, labels) = get_data()
#     learner = milk.supervised.svm.svm_raw(kernel=np.dot, C=12)
#     model = learner.train(features, labels)


# def test_tree_manual():
#     pass


def test_model():
    global model
    (features, labels) = get_data()
    # learner = milk.defaultclassifier()
    # learner = milk.supervised.svm_simple(pow(10, -3), )
    # learner = milk.supervised.svm.svm_raw(kernel=milk.supervised.svm.rbf_kernel(1.), C=12)
    learner = milk.supervised.tree.tree_learner()
    # learner = milk.supervised.svm.svm_raw(kernel=np.dot, C=12)
    # model = learner.train(features, labels)

    confusion_matrix, names = milk.measures.nfoldcrossvalidation.nfoldcrossvalidation(features, labels, learner=learner)
    # confusion_matrix, names = milk.nfoldcrossvalidation(features, labels)
    # confusion_matrix, names = milk.measures.nfoldcrossvalidation.nfoldcrossvalidation(features, labels, learner=learner)
    print "Accuracy: ", confusion_matrix.trace()/float(confusion_matrix.sum())

#############################################


# run the classifer on the new data for the game
def run_classify(image):
    im = []
    for i in image:
        im.append(i)
    return model.apply(im)

#############################################

# build_tree()
# test_tree()
# print use_tree([1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0])
# print use_tree([1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0])
# print get_data()
# test_tree()
