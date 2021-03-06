import numpy as np
from scipy import sparse
import pandas as pd
from nose.tools import assert_raises


def to_array(X):
    """Convert any matrix to an np.ndarray"""
    if sparse.issparse(X):
        X = X.toarray()
    elif isinstance(X, pd.SparseDataFrame):
        X = X.to_dense().values
    elif isinstance(X, pd.DataFrame):
        X = X.values
    return X


def assert_all_equal(X, Y):
    """Assert all values of two matrices are the same"""
    X = to_array(X)
    Y = to_array(Y)
    np.testing.assert_array_equal(X, Y)


def assert_all_close(X, Y, rtol=1e-05, atol=1e-08):
    """Assert all values of two matrices are similar

    Parameters
    ----------
    rtol : relative (multiplicative) tolerance of error
    atol : absolute (additive) tolerance of error
    """
    X = to_array(X)
    Y = to_array(Y)
    np.testing.assert_allclose(X, Y, rtol=rtol, atol=atol)


def assert_transform_equals(X, Y, transform, check=assert_all_equal, **kwargs):
    """Check that transform(X, **kwargs) == Y

    Parameters
    ----------
    X : input
    Y : output
    transform : function to apply to X
    check : function which asserts equivalence of X and Y
    **kwargs : additional arguments for transform

    Returns
    -------
    Y2 : returned value of transform(X, **kwargs)
    """
    try:
        Y2 = transform(X, **kwargs)
    except Exception as e:
        raise RuntimeError("{} with {} input to {}\n{}".format(
            type(e).__name__, type(X).__name__, transform,
            str(e)))
    check(Y, Y2), "{} failed on {}".format(
        transform,
        type(X).__name__)
    return Y2


def assert_transform_unchanged(X, transform, check=assert_all_equal, **kwargs):
    """Check that transform(X, **kwargs) == X

    Parameters
    ----------
    X : input
    transform : function to apply to X
    check : function which asserts equivalence of X and Y
    **kwargs : additional arguments for transform

    Returns
    -------
    Y2 : returned value of transform(X, **kwargs)
    """
    assert_transform_equals(X, X, transform, check=check, **kwargs)


def assert_transform_equivalent(X, Y, transform, check=assert_all_equal,
                                **kwargs):
    """Check the output of transform(X, **kwargs) == Y and transform(X, **kwargs) gives the same kind of matrix as X

    Parameters
    ----------
    X : input
    Y : output
    transform : function to apply to X
    check : function which asserts equivalence of X and Y

    **kwargs : additional arguments for transform

    Returns
    -------
    Y2 : returned value of transform(X, **kwargs)
    """
    Y2 = assert_transform_equals(X, Y, transform, check=check, **kwargs)
    assert assert_matrix_class_equivalent(X, Y2), \
        "{} produced inconsistent matrix output".format(
        type(X).__name__)


def assert_transform_raises(X, transform, exception=ValueError):
    """Check that transform(X) raises exception

    Parameters
    ----------
    X : input
    transform : function to apply to X
    exception : expected exception class
    """
    assert_raises(exception, transform, X)


def assert_matrix_class_equivalent(X, Y):
    """Check the format of X and Y are the same

    We expect:
        * shape hasn't changed
        * sparsity hasn't changed
        * class hasn't changed (except perhaps which kind of spmatrix)
        * column and index names haven't changed
    """
    assert X.shape == Y.shape
    if sparse.issparse(X):
        assert sparse.issparse(Y)
        assert X.tocoo().nnz == Y.tocoo().nnz
    else:
        assert type(X) == type(Y)
    if isinstance(X, pd.DataFrame):
        assert np.all(X.columns == Y.columns)
        assert np.all(X.index == Y.index)
    if isinstance(X, pd.SparseDataFrame) or isinstance(Y, pd.SparseDataFrame):
        assert X.density == Y.density
    return True
