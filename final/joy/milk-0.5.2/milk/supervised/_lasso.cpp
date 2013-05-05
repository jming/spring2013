// Copyright (C) 2012, Luis Pedro Coelho <luis@luispedro.org>
// License: MIT

#include <iostream>
#include <memory>
#include <cmath>
#include <random>
#include <cassert>
#include <queue>
#include "eigen3/Eigen/Dense"

using namespace Eigen;

extern "C" {
    #include <Python.h>
    #include <numpy/ndarrayobject.h>
}


namespace {

template <typename T>
int random_int(T& random, const int max) {
    std::uniform_int_distribution<int> dist(0, max - 1);
    return dist(random);
}
inline
float soft(const float val, const float lam) {
    return std::copysign(std::fdim(std::fabs(val), lam), val);
}
typedef Map<Matrix<float, Dynamic, Dynamic, RowMajor>, Aligned> MapXAf;
bool has_nans(const MapXAf& X) {
    for (int i = 0; i != X.rows(); ++i) {
        for (int j = 0; j != X.cols(); ++j) {
            if (std::isnan(X(i,j))) return true;
        }
    }
    return false;
}

struct lasso_solver {
    lasso_solver(const MapXAf& X, const MapXAf& Y, const MapXAf& W, MapXAf& B, const int max_iter, const float lam, const float eps)
        :X(X)
        ,Y(Y)
        ,W(W)
        ,B(B)
        ,max_iter(max_iter)
        ,lam(lam)
        ,eps(eps)
        { }

    void next_coords(int& i, int& j) {
        ++j;
        if (j == B.cols()) {
            j = 0;
            ++i;
            if (i == B.rows()) {
                i = 0;
            }
        }
    }



    int solve() {
        Matrix<float, Dynamic, Dynamic, RowMajor> residuals;
        int i = 0;
        int j = -1;
        // sweep is whether we are doing a whole-B sweep (i.e., even looking at
        // non-zero Bs)
        // changed is whether something has changed
        // We set this up to trigger computation of residuals and a sweep on
        // the first iteration
        bool sweep = false;
        bool changed = false;
        assert(!has_nans(X));
        assert(!has_nans(Y));
        assert(!has_nans(B));
        for (int it = 0; it != max_iter; ++it) {
            this->next_coords(i, j);
            if (i == 0 && j == 0) {
                if (sweep && !changed) {
                    return it;
                }
                if (!changed) {
                    sweep = true;
                    // Reset the residuals matrix to the best values to avoid
                    // drift due to successive rounding:
                    residuals = Y - B*X;
                } else {
                    sweep = false;
                }
                changed = false;
            }
            if (!sweep && B(i,j) == 0.0) continue;

            // We now set βᵢⱼ holding everything else fixed.  This comes down
            // to a very simple 1-dimensional problem.
            // We remember the current value in order to compute update below
            const float prev = B(i,j);
            assert(Y.cols() == W.cols());
            assert(Y.cols() == X.cols());
            assert(Y.cols() == residuals.cols());
            const float x2 = (W.row(i).array()*X.row(j).array() * X.row(j).array()).sum();
            const float xy = (W.row(i).array()*X.row(j).array() * residuals.row(i).array()).sum();
            const float raw_step = (x2 == 0.0 ? 0.0 : xy/x2);
            const float best = soft(prev + raw_step, lam);
            const float step = best - prev;
            if (std::fabs(step) > eps) {
                assert(!std::isnan(best));
                B(i,j) = best;
                residuals.row(i) -= step*X.row(j);
                changed = true;
            }
        }
        return max_iter;
    }
    std::mt19937 r;
    const MapXAf& X;
    const MapXAf& Y;
    const MapXAf& W;
    MapXAf& B;
    const int max_iter;
    const float lam;
    const float eps;
};


MapXAf as_eigen(PyArrayObject* arr) {
    assert(PyArray_EquivTypenums(PyArray_TYPE(arr), NPY_FLOAT32));
    assert(PyArray_ISCARRAY_RO(arr));
    return MapXAf(
                static_cast<float*>(PyArray_DATA(arr)),
                PyArray_DIM(arr, 0),
                PyArray_DIM(arr, 1));
}

const char* errmsg = "INTERNAL ERROR";
PyObject* py_lasso(PyObject* self, PyObject* args) {
    PyArrayObject* X;
    PyArrayObject* Y;
    PyArrayObject* W;
    PyArrayObject* B;
    int max_iter;
    float lam;
    float eps;
    if (!PyArg_ParseTuple(args, "OOOOiff", &X, &Y, &W, &B, &max_iter, &lam, &eps)) return NULL;
    if (!PyArray_Check(X) || !PyArray_ISCARRAY_RO(X) ||
        !PyArray_Check(Y) || !PyArray_ISCARRAY_RO(Y) ||
        !PyArray_Check(W) || !PyArray_ISCARRAY_RO(W) ||
        !PyArray_Check(B) || !PyArray_ISCARRAY(B) ||
        !PyArray_EquivTypenums(PyArray_TYPE(X), NPY_FLOAT32) ||
        !PyArray_EquivTypenums(PyArray_TYPE(Y), NPY_FLOAT32) ||
        !PyArray_EquivTypenums(PyArray_TYPE(W), NPY_FLOAT32) ||
        !PyArray_EquivTypenums(PyArray_TYPE(B), NPY_FLOAT32)) {
        PyErr_SetString(PyExc_RuntimeError,errmsg);
        return 0;
    }
    MapXAf mX = as_eigen(X);
    MapXAf mY = as_eigen(Y);
    MapXAf mW = as_eigen(W);
    MapXAf mB = as_eigen(B);
    max_iter *= mB.size();
    lasso_solver solver(mX, mY, mW, mB, max_iter, lam, eps);
    const int iters = solver.solve();

    return Py_BuildValue("i", iters);
}

PyMethodDef methods[] = {
  {"lasso", py_lasso, METH_VARARGS , "Do NOT call directly.\n" },
  {NULL, NULL,0,NULL},
};

const char  * module_doc =
    "Internal Module.\n"
    "\n"
    "Do NOT use directly!\n";

} // namespace

extern "C"
void init_lasso()
  {
    import_array();
    (void)Py_InitModule3("_lasso", methods, module_doc);
  }

