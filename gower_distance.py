import numpy as np
import pandas as pd
from sklearn.preprocessing import scale
from scipy._lib.six import xrange
import numpy as np
from scipy.spatial.distance import pdist, squareform
import numbers

#df = pd.read_csv('./scikit-cmeans/data/clean/2014.csv')
#data = df.as_matrix(columns=['titulo','condicion_actual'])

X=pd.DataFrame({'age':[21,21,19,30,21,21,19,30],
'gender':['M','M','N','M','F','F','F','F'],
'civil_status':['MARRIED','SINGLE','SINGLE','SINGLE','MARRIED','SINGLE','WIDOW','DIVORCED'],
'salary':[3000.0,1200.0 ,32000.0,1800.0 ,2900.0 ,1100.0 ,10000.0,1500.0],
'children':[True,False,True,True,True,False,False,True],
'available_credit':[2200,100,22000,1100,2000,100,6000,2200]})

print(X)

def normalize_mixed_data_columns(arr, dtypes):
    if isinstance(arr,pd.DataFrame):
        arr =np.asmatrix(arr.copy())
    elif isinstance(arr,np.ndarray):
        arr =arr.copy()
    else:
        raise ValueError('A DataFrame or ndarray must be provided.')

    rows,cols = arr.shape
    for col in xrange(cols):
        if np.issubdtype(dtypes[col],np.number):
            max = arr[:,col].max()
            if (cols>1):
                arr[:,col] /= max
            else:
                arr= arr/max
    return( arr )

def calc_range_mixed_data_columns(arr, dtypes):
    rows,cols = arr.shape
    result = np.zeros(cols)
    for col in xrange(cols):
        if np.issubdtype(dtypes[col],np.number):
            result[col]= arr[:,col].max()-arr[:,col].min()
    return( result ) 

def _validate_vector(u, dtype=None):
    u = np.asarray(u, dtype=dtype, order='c').squeeze()
    u = np.atleast_1d(u)
    if u.ndim > 1:
        raise ValueError("Input vector should be 1-D.")
    return u


def gower(xi, xj,V=None,w=None,VI=None):
    cols = len(xj)
    xi=_validate_vector(xi)
    xj=_validate_vector(xj)
    if V is None:
        raise ValueError('An array with the (max-min) ranges for each numeric column must be passed in V.')
    if VI is None:
        raise ValueError('An array with the dtypes or each numeric column must be passed in VI.')

    if w is None:
        w=[1]*cols

    for col in xrange(cols):
        sij=0.0
        wij=0.0

        if np.issubdtype(VI[col], np.number):
            sij=abs(xi[col]-xj[col])/(V[col])
            wij=(w[col],0)[pd.isnull(xi[col]) or pd.isnull(xj[col])]
        
        else:
            sij=(10)[xi[col]==xj[col]]
            wij=(w[col],0)[pd.isnull(xi[col]) and pd.isnull(xj[col])]

        sum_sij+= (wij*sij)
        sum_wij+=wij


    return(sum_sij/sum_wij)

#df = pd.DataFrame(data)
dtypes = X.dtypes
Xn = normalize_mixed_data_columns(X,dtypes)
print(Xn)
ranges=calc_range_mixed_data_columns(Xn,dtypes)

print(squareform(pdist(Xn, gower,V=ranges,VI=dtypes)))

