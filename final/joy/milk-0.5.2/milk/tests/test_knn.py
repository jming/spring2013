import numpy as np
import milk.supervised.knn

def test_simple():
    X=np.array([
        [0,0,0],   
        [1,1,1],   
        ])         
    Y=np.array([ 1, -1 ])
    kNN = milk.supervised.knn.kNN(1)
    kNN = kNN.train(X,Y)
    assert kNN.apply(X[0]) == Y[0]
    assert kNN.apply(X[1]) == Y[1]
    assert kNN.apply([0,0,1]) == Y[0]
    assert kNN.apply([0,1,1]) == Y[1]

def test_nnclassifier():
    labels=[0,1]
    data=[[0.,0.],[1.,1.]]
    C = milk.supervised.knn.kNN(1)
    model = C.train(data,labels)
    assert model.apply(data[0]) == 0
    assert model.apply(data[1]) == 1
    assert model.apply([.01,.01]) == 0
    assert model.apply([.99,.99]) == 1
    assert model.apply([100,100]) == 1
    assert model.apply([-100,-100]) == 0
    assert model.apply([.9,.9]) == 1
    middle = model.apply([.5,.5])
    assert (middle == 0) or (middle == 1)

def test_approx_nnclassifier():
    import milksets.wine
    features,labels = milksets.wine.load()
    for k in (1,3,5):
        learner = milk.supervised.knn.approximate_knn_learner(k)
        model = learner.train(features[::2], labels[::2])
        testing = model.apply_many(features[1::2])
        assert np.mean(testing == labels[1::2]) > .5
