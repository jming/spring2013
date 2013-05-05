import milk.supervised.featureselection
from milk.supervised.featureselection import select_n_best, rank_corr
import numpy as np
def test_sda():
    from milksets import wine
    features, labels = wine.load()
    selected = milk.supervised.featureselection.sda(features,labels)
    for sel in selected:
        assert sel <= features.shape[1]

def test_linear_independent_features():
    np.random.seed(122)
    X3 = np.random.rand(20,3)
    X = np.c_[X3,X3*2+np.random.rand(20,3)/20.,-X3*2+np.random.rand(20,3)/10.]
    X2 = np.c_[X3,X3*2,-X3*3e-3]
    assert len(milk.supervised.featureselection.linear_independent_features(X)) == 9
    assert len(milk.supervised.featureselection.linear_independent_features(X2)) == 3
    assert np.all (np.sort(milk.supervised.featureselection.linear_independent_features(X2) % 3) == np.arange(3))

def _rank(A,tol=1e-8):
    s = np.linalg.svd(A,compute_uv=0)
    return (s > tol).sum()

def _slow_linear_independent_features(featmatrix):
    '''
    Returns the indices of a set of linearly independent features (columns).

    indices = linear_independent_features(features)
    '''
    independent = [0,]
    rank = 1
    feat = [featmatrix[:,0]]
    for i,col in enumerate(featmatrix.T):
        feat.append(col)
        nrank = _rank(np.array(feat))
        if nrank == rank:
            del feat[-1]
        else:
            rank = nrank
            independent.append(i)
    return np.array(independent)


def test_select_n():
    from milksets.wine import load

    features,labels = load()
    for n in (1,2,4,8):
        select = select_n_best(n, rank_corr)
        model = select.train(features,labels)
        f = model.apply(features[3])
        assert len(f) == n

def test_select_n():
    from milksets.wine import load

    features,labels = load()
    for n in (1,2,4,8):
        select = select_n_best(n, rank_corr)
        model = select.train(features,labels)
        f = model.apply(features[3])
        assert len(f) == n

def slow_rank_corr(features, labels):
    features = np.asanyarray(features)
    labels = np.asanyarray(labels)
    binlabels = [(labels == ell) for ell in set(labels)]
    rs = []
    for feat in features.T:
        ranks = feat.argsort()
        corrcoefs = [np.corrcoef(ranks, labs)[0,1] for labs in binlabels]
        corrcoefs = np.array(corrcoefs)
        corrcoefs **= 2
        rs.append(np.max(corrcoefs))
    return np.array(rs)

def test_compare_rank_corr():
    from milksets.wine import load
    features,labels = load()
    r0 = rank_corr(features,labels)
    r1 = slow_rank_corr(features,labels)
    assert np.allclose(r0,r1)
