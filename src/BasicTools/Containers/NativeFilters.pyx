#distutils: language = c++
#cython: language_level = 3
#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.
#
from libcpp.vector cimport vector
from libcpp.string cimport string

import numpy as np
cimport numpy as cnp
cnp.import_array()

from eigency.core cimport *

from BasicTools.CythonDefs cimport CBasicIndexType, CBasicFloatType
from BasicTools.NumpyDefs import  PBasicFloatType, PBasicIndexType

cimport BasicTools.Containers.NativeFilters as cNF

cdef class CElementFilterEvaluated:
    #cdef cNF.ElementFilterEvaluated cpp_object

    cdef cNF.ElementFilterEvaluated* GetCppPointer(self) nogil:
        return &(self.cpp_object)

    def callnumpysure(self, elemtype, cnp.ndarray[CBasicIndexType, ndim=1, mode="c"] ids not None) :
        self.cpp_object.SetIdsToTreatFor(elemtype,
                                         FlattenedMap[Matrix, CBasicIndexType, Dynamic, _1](ids) )

    def SetIdsToTreat(self,mesh,elementFilter ):
        self.GetCppPointer()[0].Clear()
        if elementFilter is None:
           for elemtype, data in mesh.elements.items():
               self.callnumpysure(elemtype.encode(),np.arange(data.GetNumberOfElements()) )
        else:
            elementFilter.mesh = mesh
            for elemtype, data in   mesh.elements.items():
                ids= elementFilter.GetIdsToTreat(data)
                ids = np.asarray(ids, dtype=PBasicIndexType)
                self.callnumpysure(elemtype.encode(), ids )

    def __str__(self):
        res = self.cpp_object.ToStr().decode('UTF-8')
        res += "Done"
        return res
