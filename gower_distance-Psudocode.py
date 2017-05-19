OUTPUT X
FUNCTION normalize_mixed_data_columns(arr, dtypes):
    IF isinstance(arr,pd.DataFrame):
        arr =np.asmatrix(arr.copy())
    ELSEIF isinstance(arr,np.ndarray):
        arr =arr.copy()
    ELSE:
        raise ValueError('A DataFrame or ndarray must be provided.')
    ENDIF
    rows,cols <- arr.shape
    for col in xrange(cols):
        IF np.issubdtype(dtypes[col],np.number):
            max <- arr[:,col].max()
            IF (cols>1):
                arr[:,col] /= max
            ELSE:
                arr= arr/max
        ENDIF
            ENDIF
    ENDFOR
    RETURN( arr )
ENDFUNCTION

FUNCTION calc_range_mixed_data_columns(arr, dtypes):
    rows,cols <- arr.shape
    result <- np.zeros(cols)
    for col in xrange(cols):
        IF np.issubdtype(dtypes[col],np.number):
            result[col]= arr[:,col].max()-arr[:,col].min()
        ENDIF
    ENDFOR
    RETURN( result ) 
ENDFUNCTION

FUNCTION _validate_vector(u, dtype=None):
    u <- np.asarray(u, dtype=dtype, order='c').squeeze()
    u <- np.atleast_1d(u)
    IF u.ndim > 1:
        raise ValueError("Input vector should be 1-D.")
    ENDIF
    RETURN u
ENDFUNCTION

FUNCTION gower(xi, xj,V=None,w=None,VI=None):
    cols <- len(xj)
    xi=_validate_vector(xi)
    xj=_validate_vector(xj)
    IF V is None:
        raise ValueError('An array with the (max-min) ranges for each numeric column must be passed in V.')
    ENDIF
                                                             ENDFOR
    IF VI is None:
        raise ValueError('An array with the dtypes or each numeric column must be passed in VI.')
    ENDIF
    IF w is None:
        w=[1]*cols
    ENDIF
    sum_sij=0.0
    sum_wij=0.0
    for col in xrange(cols):
        sij=0.0
        wij=0.0
        IF np.issubdtype(VI[col], np.number):
            sij=abs(xi[col]-xj[col])/(V[col])
            wij=(w[col],0)[pd.isnull(xi[col]) OR pd.isnull(xj[col])]
        ELSE:
            sij=(1,0)[xi[col]==xj[col]]
            wij=(w[col],0)[pd.isnull(xi[col]) AND pd.isnull(xj[col])]
        ENDIF
        sum_sij+= (wij*sij)
        sum_wij+=wij
    ENDFOR
    RETURN(sum_sij/sum_wij)
#df <- pd.DataFrame(data)
ENDFUNCTION

dtypes <- X.dtypes
Xn <- normalize_mixed_data_columns(X,dtypes)
OUTPUT Xn
ranges=calc_range_mixed_data_columns(Xn,dtypes)
OUTPUT "Dissimilarities :"
D=np.tril(squareform(pdist(Xn, gower,V=ranges,VI=dtypes)))
                ENDFOR
OUTPUT D
np.savetxt("/home/lain/Redes-Sociales-con-Enfoque-Difuso/distance_matrix.csv", D, delimiter=",")
